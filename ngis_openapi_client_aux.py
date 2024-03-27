import json
import uuid
from qgis.core import (
    QgsProject,
    QgsPathResolver,
    QgsVectorLayer,
    QgsOgcUtils,
    QgsFeature,
    QgsJsonUtils,
    QgsJsonExporter,
    QgsAuthManager,
    QgsWkbTypes,
    QgsSettings,
    QgsDefaultValue,
    QgsFieldConstraints,
    QgsEditorWidgetSetup,
    QgsCoordinateReferenceSystem,
    QgsMessageLog,
    QgsFeatureRequest,
    QgsProcessingContext,
    QgsTaskManager,
    QgsTask,
    QgsProcessingAlgRunnerTask,
    Qgis,
    QgsProcessingFeedback,
    QgsApplication,
    QgsMessageLog,
    QgsFields,
    QgsField,
    QgsRelation
)
from PyQt5.QtCore import QVariant, QSettings, QTranslator, QCoreApplication, QTextCodec, QDate

from xsd_parser.models.xsd_parser_models import (Attribute, Avgrensing, Geometry)

#Attribute = __import__("SFKB-QGISAPI-klient.ngis_openapi_client_xsd_parser").ngis_openapi_client_xsd_parser.Attribute
#Avgrensing = __import__("SFKB-QGISAPI-klient.ngis_openapi_client_xsd_parser").ngis_openapi_client_xsd_parser.Avgrensing
#Geometry = __import__("SFKB-QGISAPI-klient.ngis_openapi_client_xsd_parser").ngis_openapi_client_xsd_parser.Geometry


def utledAvgrensinger(xsd):
    
    avgrenser = {}
    avgrensesAv = {}

    for subkey, sublist in xsd.items():
        for k, v in sublist.items():
            if isinstance(v, Avgrensing):
                if v.avgrensesAv not in avgrenser:
                    avgrenser[v.avgrensesAv] = []
                avgrenser[v.avgrensesAv].append(subkey)

                if subkey not in avgrensesAv:
                    avgrensesAv[subkey] = []
                avgrensesAv[subkey].append(v.avgrensesAv)
    
    return avgrenser, avgrensesAv


def create_crs_entry(epsg):
    return {
        "crs": {
            "type": "name",
            "properties": {
                "name": f"{epsg}"
            }
        }
    }

def authid_to_code(authid):
    epsg_tag_idx = authid.lower().find("epsg:")
    if epsg_tag_idx > -1:
        code = authid[epsg_tag_idx+5:]
        return code

def try_parse_json(myjson):
    try:
        json_object = json.loads(myjson)
        return json_object
    except Exception:
        return myjson

def of_type(iterable, target_type):
        return [i for i in iterable if isinstance(i, target_type)]

def xsd_to_fields(lyr, xsd_def, complex_multiple_lyr = {}):
    

    for fieldName, field_def in xsd_def.items():
        
        #todo andreas (handle geometry og avgrensingslinjer, ignoreR?)
        if not isinstance(xsd_def[fieldName], Attribute): continue

        field_type = field_def.type

        field = None

        if field_type == "date":
            field = QgsField(fieldName, QVariant.Date, comment = field_def.documentation)
        elif field_type == "dateTime":
            field = QgsField(fieldName, QVariant.DateTime, comment = field_def.documentation)
        elif field_type == "enum":
            field = QgsField(fieldName, QVariant.String, comment = field_def.documentation)
        elif field_type == "integer":
            field = QgsField(fieldName, QVariant.Int, comment = field_def.documentation)
        elif field_type == "double":
            field = QgsField(fieldName, QVariant.Double, comment = field_def.documentation)
        elif field_type == "boolean":
            field = QgsField(fieldName, QVariant.Bool, comment = field_def.documentation)
        elif  "PropertyType" in field_type:
            xsdChildName = field_type.split("PropertyType")[0]
            relation_layer = complex_multiple_lyr.get(xsdChildName, None)
            if relation_layer is None:
                raise Exception(f"Relation layer not found for {xsdChildName}")
            relation = QgsRelation()
            relation_id = str(uuid.uuid4())
            relation.setId(relation_id) 
            relation.setName(fieldName)
            relation.setReferencingLayer(relation_layer.id())  # Child layer
            relation.setReferencedLayer(lyr.id())  # Parent layer
            relation.addFieldPair('lokalId', 'lokalId')
            QgsProject.instance().relationManager().addRelation(relation)
            if not relation.isValid(): 
                raise Exception(f"Relation not valid for {xsdChildName}")     
            continue            
        
        else:
            field = QgsField(fieldName, QVariant.String, comment = field_def.documentation)

        # MinOccurs
        if field_def.minOccurs == 1:
            constaints = QgsFieldConstraints()
            constaints.setConstraint(1)
            field.setConstraints(constaints)

        lyr.addAttribute(field)
        field_idx = lyr.fields().indexFromName(fieldName)

        if field_type == "date":
            field_to_date(lyr, field_idx)
        if field_type == "dateTime":
            field_to_datetime(lyr, field_idx)
        if field_type == "string":
            lyr.setDefaultValueDefinition(field_idx, QgsDefaultValue("''"))
        if field_type == "enum":
            enum = field_def.values
            if enum:
                if field_def.maxOccurs > 1:
                    field_to_valuerelation(lyr, field_idx, field_def.minOccurs == 0)
                else:
                    field_to_valuemap(lyr, field_idx, enum)
        
        # Some default values
        if fieldName == "lokalId":
            lyr.setDefaultValueDefinition(field_idx, QgsDefaultValue("replace(replace(uuid(), '{', ''), '}', '')"))
            form_config = lyr.editFormConfig()
            form_config.setReadOnly(field_idx, True)
            lyr.setEditFormConfig(form_config)
        if fieldName == "navnerom":
            lyr.setDefaultValueDefinition(field_idx, QgsDefaultValue("'data.geonorge.no/havnedata/so'"))
            form_config = lyr.editFormConfig()
            form_config.setReadOnly(field_idx, False)
            lyr.setEditFormConfig(form_config)
        if fieldName == "versjonId":
            lyr.setDefaultValueDefinition(field_idx, QgsDefaultValue("now()", True))
            form_config = lyr.editFormConfig()
            form_config.setReadOnly(field_idx, False)
            lyr.setEditFormConfig(form_config)

def add_featuretype_field_to_layer(lyr, feature_type):

    # Featuretype should not be writable
    lyr.addAttribute(QgsField("featuretype", QVariant.String))
    featuretype_idx = lyr.fields().indexOf("featuretype")
    if featuretype_idx >= 0:
        lyr.setDefaultValueDefinition(featuretype_idx, QgsDefaultValue(f'\'{feature_type}\''))
        form_config = lyr.editFormConfig()
        form_config.setReadOnly(featuretype_idx, True)
        lyr.setEditFormConfig(form_config)
    
    return

def field_to_valuerelation(layer, field_idx, allow_null):
    
    target_layer = QgsProject.instance().mapLayersByName(layer.fields()[field_idx].name())[0]
    field_type = 'ValueRelation'
    config = {
                'Layer' : target_layer.id(),
                'AllowMulti': True,
                'AllowNull': allow_null,
                'FilterExpression': '',
                'Key': 'Kodeverdi',
                'NofColumns': 1,
                'OrderByValue': False,
                'UseCompleter': False,
                'Value': 'Navn',
                'Description' : 'Beskrivelse'
            }
    widget_setup = QgsEditorWidgetSetup(field_type, config)
    layer.setEditorWidgetSetup(field_idx, widget_setup)

def field_to_valuemap(layer, field_idx, enum):
    
    valueMap = {}
    for elm in list(enum):
        valueMap[elm['type']] = elm['value']
    field_type = 'ValueMap'
    config = {'map' : valueMap}
    widget_setup = QgsEditorWidgetSetup(field_type, config)
    layer.setEditorWidgetSetup(field_idx, widget_setup)

def field_to_default_text(layer, field_idx, field_type, default_text):
    if field_type == "numeric":
        layer.setDefaultValueDefinition(field_idx, QgsDefaultValue(f'{default_text}'))
    else:
        layer.setDefaultValueDefinition(field_idx, QgsDefaultValue(f'\'{default_text}\''))

def field_to_datetime(layer, field_idx):
    config = {
            'allow_null': False,
            'calendar_popup': True,
            'display_format': 'yyyy-MM-dd',
            'field_format': 'yyyy-MM-dd',
            'field_iso_format': True
            }
    field_type = 'DateTime'
    widget_setup = QgsEditorWidgetSetup(field_type, config)
    layer.setEditorWidgetSetup(field_idx, widget_setup)

def field_to_date(layer, field_idx):
    config = {
            'allow_null': False,
            'calendar_popup': True,
            'display_format': 'yyyy-MM-dd',
            'field_format': 'yyyy-MM-dd',
            'field_iso_format': True
            }
    field_type = 'DateTime'
    widget_setup = QgsEditorWidgetSetup(field_type, config)
    layer.setEditorWidgetSetup(field_idx, widget_setup)


class ApiError(object):
    def __init__(self, title, detail, e):
        self.title = title
        self.detail = detail
        self.show_more = str(e)

        try:
            error_object = json.loads(e.body)
            self.title = error_object['title'] if 'title' in error_object else None
            self.detail = error_object["detail"] if 'detail' in error_object else None
            self.show_more = str(error_object["errors"]) if 'errors' in error_object else None
        except:
            pass

