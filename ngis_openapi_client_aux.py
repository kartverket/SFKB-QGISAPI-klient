import json
from qgis.core import (
    QgsEditorWidgetSetup,
    QgsDefaultValue,
    QgsFieldConstraints
)

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

schema_definition = {
    "Vanntilkobling" : 
        {
        "featuretype":{
            "read_only" : True
        },
        "datafangstdato": {
            "type" : "datetime"
        },
        "havneident": {
            "not_null" : True,
            "default" : "havn"
        },
        "kaiident": {
            "not_null" : True,
            "default" : "kai"
        },
        "oppdateringsdato": {
            "type" : "datetime"
        },
        "informasjon": {
            "not_null" : False,
        },
        "UNLOCODE": {
            "not_null" : True,
            "default" : "NOIS"
        },
        "vanntilkobling": {
            "enum" : ["ferskvann", "saltvann"],
            "not_null" : True,
            "default" : "ferskvann"
        },
        "identifikasjon": {
            "read_only" : True,
            "default" : f'{{ "navnerom": "data.geonorge.no/havnedata/so", "lokalId": "", "versjonId": "2020-10-26 11:10:36.246000" }}'
        },
        "kvalitet": {
            "not_null" : True,
            "default" : '{ "målemetode": "10", "nøyaktighet": 10, "synbarhet": "1", "målemetodeHøyde": "10", "nøyaktighetHøyde": 10 }'
        },
        "høydereferanse": {
            "not_null" : True,
            "default" : 'ukjent'
        },
        "link": {
            "not_null" : True,
            "default" : 'x'
        },
        "kumnummer": {
            "not_null" : True,
            "default" : 2,
            "type" : "numeric"
        },
    },
    "Havnegjerde" : {
        "featuretype":{
            "read_only" : True
        },
        "datafangstdato": {
            "type" : "datetime"
        },
        "havneident": {
            "not_null" : True,
            "default" : "havn"
        },
        "oppdateringsdato": {
            "type" : "datetime"
        },
        "informasjon": {
            "not_null" : False,
        },
        "identifikasjon": {
            "read_only" : True,
            "default" : f'{{ "navnerom": "data.geonorge.no/havnedata/so", "lokalId": "", "versjonId": "2020-10-26 11:10:36.246000" }}'
        },
        "kvalitet": {
            "not_null" : True,
            "default" : '{ "målemetode": "10", "nøyaktighet": 10, "synbarhet": "1", "målemetodeHøyde": "10", "nøyaktighetHøyde": 10 }'
        },
            "UNLOCODE": {
            "not_null" : True,
            "default" : "NOIS"
        },
        "høydereferanse": {
            "not_null" : True,
            "default" : 'ukjent'
        },
        "link": {
            "not_null" : True,
            "default" : 'x'
        }
    }
}

def add_fields_to_layer(lyr, fields, feature_type):
    for field_idx, field in enumerate(fields):
        if feature_type in schema_definition:
            if field.name() in schema_definition[feature_type]:
                not_null = schema_definition[feature_type][field.name()]['not_null'] if 'not_null' in schema_definition[feature_type][field.name()] else False
                if not_null:
                    constaints = QgsFieldConstraints()
                    constaints.setConstraint(1)
                    field.setConstraints(constaints)
        addAttribute = lyr.addAttribute(field)
        if feature_type in schema_definition:
            if field.name() in schema_definition[feature_type]:
                field_type = schema_definition[feature_type][field.name()]['type'] if 'type' in schema_definition[feature_type][field.name()] else False
                if field_type == "datetime":
                    field_to_datetime(lyr, field_idx)
                default_text = schema_definition[feature_type][field.name()]['default'] if 'default' in schema_definition[feature_type][field.name()] else None
                if default_text:
                    field_to_default_text(lyr, field_idx, field_type, default_text)
                enum = schema_definition[feature_type][field.name()]['enum'] if 'enum' in schema_definition[feature_type][field.name()] else None
                if enum:
                    field_to_enum(lyr, field_idx, enum)
                read_only = schema_definition[feature_type][field.name()]['read_only'] if 'read_only' in schema_definition[feature_type][field.name()] else None
                if read_only:
                    form_config = lyr.editFormConfig()
                    form_config.setReadOnly(field_idx, True)
                    lyr.setEditFormConfig(form_config)
                
    featuretype_idx = fields.indexOf("featuretype")
    if featuretype_idx >= 0:
        lyr.setDefaultValueDefinition(featuretype_idx, QgsDefaultValue(f'\'{feature_type}\''))

def field_to_enum(layer, field_idx, enum):
    
    enum = {key: key for key in enum}
    field_type = 'ValueMap'
    config = {'map' : enum}
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