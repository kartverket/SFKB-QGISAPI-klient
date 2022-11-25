import json
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
    QgsField
)
from PyQt5.QtCore import QVariant, QSettings, QTranslator, QCoreApplication, QTextCodec, QDate
from ngis_openapi_client_xsd_parser import Attribute

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


def xsd_to_fields(lyr, xsd_def):
    for field_idx, fieldName in enumerate(xsd_def):
        field_def : Attribute = xsd_def[fieldName]
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
        else:
            field = QgsField(fieldName, QVariant.String, comment = field_def.documentation)

        # MinOccurs
        if field_def.minOccurs == 1:
            constaints = QgsFieldConstraints()
            constaints.setConstraint(1)
            field.setConstraints(constaints)

        lyr.addAttribute(field)

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
            lyr.setDefaultValueDefinition(field_idx, QgsDefaultValue("'<autogenerert>'"))
            form_config = lyr.editFormConfig()
            form_config.setReadOnly(field_idx, True)
            lyr.setEditFormConfig(form_config)
        if fieldName == "navnerom":
            lyr.setDefaultValueDefinition(field_idx, QgsDefaultValue("'data.geonorge.no/havnedata/so'"))
            form_config = lyr.editFormConfig()
            form_config.setReadOnly(field_idx, True)
            lyr.setEditFormConfig(form_config)
        if fieldName == "versjonId":
            lyr.setDefaultValueDefinition(field_idx, QgsDefaultValue("'2020-11-25 09:22:03.599000'"))
            form_config = lyr.editFormConfig()
            form_config.setReadOnly(field_idx, True)
            lyr.setEditFormConfig(form_config)

def add_fields_to_layer(lyr, feature_type, xsd):

    xsd_def = xsd[feature_type]
    
    xsd_to_fields(lyr, xsd_def)
    
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
                'Key': 'Verdi',
                'NofColumns': 1,
                'OrderByValue': False,
                'UseCompleter': False,
                'Value': 'Verdi'
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

class AddFeaturesToMap(QgsTask):
    """This shows how to subclass QgsTask"""
    
    def __init__(self, description, parent, features_from_api, feature_type, features_list, crs_from_api, group, slds, xsd, selected_id):
        super().__init__(description, QgsTask.CanCancel)
        self.description = description
        self.parent = parent
        self.features_from_api = features_from_api
        self.feature_type = feature_type
        self.features_list = features_list
        self.crs_from_api = crs_from_api
        self.group = group
        self.slds = slds
        self.xsd = xsd
        self.selected_id = selected_id


    
    def run(self):
        """Here you implement your heavy lifting.
        Should periodically test for isCanceled() to gracefully
        abort.
        This method MUST return True or False.
        Raising exceptions will crash QGIS, so we handle them
        internally and raise them in self.finished
        """
        print(f"Started task {self.description}")

        # Create a new GeoJSON object containing a single featuretype
        features_dict = self.features_from_api.copy()
        features_dict['features'] =  self.features_list

        features_json = json.dumps(features_dict, ensure_ascii=False) 
        
        # Identify fields and features from GeoJSON
        codec = QTextCodec.codecForName("UTF-8")   
        fields = QgsJsonUtils.stringToFields(features_json, codec)
        newFeatures = QgsJsonUtils.stringToFeatureList(features_json, fields, codec)

        # If different geometry types are identified, separate them into individual layers
        geometry_dict = {}
        if newFeatures:   
            for feature in newFeatures:

                featuretype = feature.attribute('featuretype')
                geom_type = feature.geometry()
                geom_type = QgsWkbTypes.displayString(int(geom_type.wkbType()))
                if geom_type not in geometry_dict:
                    geometry_dict[geom_type] = {}
                if featuretype not in geometry_dict[geom_type]:
                    geometry_dict[geom_type][featuretype] = []
                
                geometry_dict[geom_type][featuretype].append(feature)

        for geom_type, feature_types in geometry_dict.items():
            for feature_type, features in feature_types.items():
                lyr = QgsVectorLayer(f'{geom_type}?crs={self.crs_from_api}', f'{feature_type}-{geom_type}', "memory")
                #lyr = QgsVectorLayer(f'{geom_type}?crs=EPSG:25832', f'{feature_type}-{geom_type}', "memory") #TODO Remove
                QgsProject.instance().addMapLayer(lyr, False)
                
                lyr.startEditing()
                
                add_fields_to_layer(lyr, fields, feature_type, self.xsd)
                print(f'{geom_type}?crs={self.crs_from_api}', f'{feature_type}-{geom_type}')   
                lyr.commitChanges()
                l_d = lyr.dataProvider()
                lyrfields = lyr.fields()

                for feature in features:
                    fet = QgsFeature()
                    fet.setGeometry(feature.geometry())

                    attributes = feature.attributes()
                    newDict = {}
                    for idx, attribute in enumerate(attributes):
                        try:
                            obj = json.loads(attribute)
                            for key, value in obj.items():
                                newDict[key] = value
                        except:
                            oldfield = fields.at(idx)
                            newDict[oldfield.name()] = feature.attributes()[idx]

                    fieldOrder = {}
                    fet.initAttributes(len(lyrfields))
                    for fieldName in newDict.keys():
                        newIdx = lyrfields.indexFromName(fieldName)
                        fieldOrder[fieldName] = newIdx
                        print(f'{newIdx} - {newDict[fieldName]}')
                        try:
                            fet.setAttribute(newIdx, newDict[fieldName])
                        except Exception as e:
                            print(e)
                    l_d.addFeature(fet)

                
                # update the extent of rev_lyr
                lyr.updateExtents()
                # save changes made in 'rev_lyr'
                lyr.commitChanges()
                self.group.addLayer(lyr)
                
                #lyr.committedFeaturesAdded.connect(self.handleCommitedAddedFeatures)
                #lyr.committedFeaturesRemoved.connect(self.handleCommittedFeaturesRemoved)
                #lyr.featuresDeleted.connect(self.handleDeletedFeatures)
                #lyr.committedGeometriesChanges(self.ee)
                
                lyr.beforeCommitChanges.connect(self.parent.handle_before_commitchanges)

                if feature_type in self.slds:
                    lyr.loadSldStyle(self.slds[feature_type])

                self.parent.dataset_dictionary[lyr.id()] = self.selected_id
                self.parent.feature_type_dictionary[lyr.id()] = feature_type
        return True

    def finished(self, result):
        """
        This function is automatically called when the task has
        completed (successfully or not).
        You implement finished() to do whatever follow-up stuff
        should happen after the task is complete.
        finished is always called from the main thread, so it's safe
        to do GUI operations and raise Python exceptions here.
        result is the return value from self.run.
        """

        print("FERDIG")

    def cancel(self):
        QgsMessageLog.logMessage(
            'Task "{name}" was canceled'.format(
                name=self.description()),
            MESSAGE_CATEGORY, Qgis.Info)
        super().cancel()