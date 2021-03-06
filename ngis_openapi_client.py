# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NgisOpenApiClient
                                 A QGIS plugin
 Plugin for nedlasting av data fra NGIS OpenAPI
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-10-26
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Norconsult Informasjonssystemer AS
        email                : post@nois.no
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QTextCodec, QDate, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QPushButton, QMessageBox
from qgis.utils import plugins
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
    QgsFeatureRequest
)

import json
import uuid
from .login import NgisOpenApiClientAuthentication
from .http_client import NgisHttpClient
from .ngis_openapi_client_aux import *
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .ngis_openapi_client_dialog import NgisOpenApiClientDialog
from xml.dom import minidom
import os.path


class NgisOpenApiClient:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'NgisOpenApiClient_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&NGIS-OpenAPI')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        self.dataset_dictionary = {}
        self.feature_type_dictionary = {}
        self.layer_dictionary = {}
        self.client = None
    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('NgisOpenApiClient', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ngis_openapi_client/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'NGIS-OpenAPI Klient'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&NGIS-OpenAPI Klient'),
                action)
            self.iface.removeToolBarIcon(action)

    def handle_login(self):
        auth = NgisOpenApiClientAuthentication()
        configId = self.dlg.mAuthConfigSelect.configId()
        url, username, password = auth.getConfig(configId)
        if not username:
            self.dlg.statusLabel.setText("Autentisering mislyktes")
            return
        self.client = NgisHttpClient(url, username, password) 

        try:
            datasets = self.client.getAvailableDatasets()
        except Exception as e:
            error = ApiError("Kunne ikke hente datasett", "Utlisting av datasett resulterte i en feil", e)  
            self.iface.messageBar().pushMessage(error.title, error.detail, error.show_more, level=2, duration=10)
            return 
        
        if len(datasets) == 0:
            self.dlg.statusLabel.setText("Ingen datasett tilgjengelig")
            return
        
        self.dataset_dictionary = {dataset["name"]:dataset["id"] for dataset in datasets}
        
        names = [dataset['name'] for dataset in datasets]
        self.dlg.mComboBox.addItems(names)

        self.dlg.mComboBox.setEnabled(True)
        self.dlg.logInButton.setEnabled(False)
        self.dlg.logOutButton.setEnabled(True)
        self.dlg.addLayerButton.setEnabled(True)
        self.dlg.mAuthConfigSelect.setEnabled(False)
        self.dlg.statusLabel.setText("")
        # Remember login method
        s = QgsSettings()
        s.setValue("ngisopenapi/auth_method_id", configId)
        return

    def handle_logout(self):
        self.dlg.mComboBox.clear()
        self.dlg.logInButton.setEnabled(True)
        self.dlg.logOutButton.setEnabled(False)
        self.dlg.addLayerButton.setEnabled(False)
        self.dlg.mAuthConfigSelect.setEnabled(True)
        self.dlg.mComboBox.setEnabled(False)
        self.client = None

    def create_group(self, name):
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup(name)
        if not group:
            group = root.insertGroup(0, name)
        return group

    def handle_add_layer(self):
        """Create a new layer by name (rev_lyr)"""

        slds = self.get_sld()

        selected_name = self.dlg.mComboBox.currentText()
        selected_id = self.dataset_dictionary[selected_name]
        
        # Group name equals selected dataset name
        group = self.create_group(selected_name)

        # Get metadata and features from NgisOpenAPI
        try:
            metadata_from_api = self.client.getDatasetMetadata(selected_id)
            epsg = metadata_from_api.crs_epsg
            features_from_api = self.client.getDatasetFeatures(metadata_from_api.id, metadata_from_api.bbox, epsg)
        except Exception as e:
            error = ApiError("Nedlasting av data mislyktes", "Kunne ikke laste ned datasett", e)  
            self.iface.messageBar().pushMessage(error.title, error.detail, error.show_more, level=2, duration=10)
            return 
        crs_from_api = features_from_api['crs']['properties']['name']
        features_by_type = {}
        
        # Extract features from GeoJSON into dictionary
        for feature in features_from_api['features']:
            feature_type = feature['properties']['featuretype']
            features_by_type.setdefault(feature_type, []).append(feature)
        
        features_from_api['features'] = None

        for feature_type, features_list in features_by_type.items():
            # Create a new GeoJSON object containing a single featuretype
            features_dict = features_from_api.copy()
            features_dict['features'] = features_list

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
                    lyr = QgsVectorLayer(f'{geom_type}?crs={crs_from_api}', f'{feature_type}-{geom_type}', "memory")
                    #lyr = QgsVectorLayer(f'{geom_type}?crs=EPSG:25832', f'{feature_type}-{geom_type}', "memory") #TODO Remove
                    QgsProject.instance().addMapLayer(lyr, False)
                    
                    lyr.startEditing()
                    
                    add_fields_to_layer(lyr, fields, feature_type)

                    lyr.commitChanges()
                    l_d = lyr.dataProvider()
                    l_d.addFeatures(features)
                    # update the extent of rev_lyr
                    lyr.updateExtents()
                    # save changes made in 'rev_lyr'
                    lyr.commitChanges()
                    group.addLayer(lyr)
                   
                    #lyr.committedFeaturesAdded.connect(self.handleCommitedAddedFeatures)
                    #lyr.committedFeaturesRemoved.connect(self.handleCommittedFeaturesRemoved)
                    #lyr.featuresDeleted.connect(self.handleDeletedFeatures)
                    #lyr.committedGeometriesChanges(self.ee)
                    
                    lyr.beforeCommitChanges.connect(self.handle_before_commitchanges)

                    if feature_type in slds:
                        lyr.loadSldStyle(slds[feature_type])

                    self.dataset_dictionary[lyr.id()] = selected_id
                    self.feature_type_dictionary[lyr.id()] = feature_type
    
    def get_sld(self):
        sld_dict = {}
        folder_name = f"{os.path.dirname(__file__)}/styles"
        for filename in os.listdir(folder_name):
            full_path = f"{folder_name}/{filename}"
            sld = minidom.parse(full_path)
            styled_layer_descriptor = sld.getElementsByTagName('StyledLayerDescriptor')
            if len(styled_layer_descriptor) == 1:
                named_layers = styled_layer_descriptor[0].getElementsByTagName('NamedLayer')
                for named_layer in named_layers:
                    for child in named_layer.childNodes:
                        if child.localName == "Name":
                            name = child.firstChild.nodeValue
                            sld_dict[name] = full_path
                            break
        return sld_dict

    def handle_before_commitchanges(self):
        
        layer = self.iface.activeLayer()

        if layer.editBuffer():
            ids_deleted = layer.editBuffer().deletedFeatureIds()
            features_deleted = layer.dataProvider().getFeatures(QgsFeatureRequest().setFilterFids(ids_deleted))
            features_added = layer.editBuffer().addedFeatures()
            changed_geometries = layer.editBuffer().changedGeometries()
            changed_attribute_values = layer.editBuffer().changedAttributeValues()

            try:
                features = []
                features = features + self.handle_committed_features_removed(layer, features_deleted)
                features = features + self.handle_committed_features_added(layer, features_added)
                features = features + self.handle_changed_values(layer, changed_attribute_values, changed_geometries, ids_deleted)
                
                self.handle_altered_features(layer, features)
            except Exception as e:
                self.iface.messageBar().pushMessage("Lagring mislyktes", "" , str(e), level=2, duration=10)

    def lock_feature(self, lyr, changed_feature, references='none'):
        lokalid = json.loads(changed_feature.attribute('identifikasjon'))["lokalId"]
        datasetid = self.dataset_dictionary[lyr.id()]
        crs = lyr.crs().authid()
        crs_epsg = authid_to_code(crs)
        try:
            feature_with_lock = self.client.getDatasetFeatureWithLock(datasetid, lokalid, crs_epsg, references)
            return feature_with_lock
        except Exception as e:
            error = ApiError("Låsing mislyktes", "Kunne ikke låse feature", e)  
            raise Exception(f'{error.title}: {error.show_more}')

    def handle_changed_values(self, lyr, changed_attribute_values, changed_geometries, ids_deleted):
        
        features = []
        for fid, attributes in changed_attribute_values.items():
            
            if fid in ids_deleted: continue

            changed_feature = lyr.getFeature(fid)
            lokalid = json.loads(changed_feature.attribute('identifikasjon'))["lokalId"]
            if lyr.geometryType() == QgsWkbTypes.PolygonGeometry or lyr.geometryType() == QgsWkbTypes.LineGeometry:
                feature_with_lock = self.lock_feature(lyr, changed_feature, 'direct')
            else:
                feature_with_lock = self.lock_feature(lyr, changed_feature)

            for idx, feature in enumerate(feature_with_lock["features"]):
                if feature["properties"]["identifikasjon"]["lokalId"] == lokalid:

                    for attribute_idx, attribute in attributes.items():
                        attribute_name = lyr.dataProvider().fields().field(attribute_idx).name()
                        if type(attribute) == QDate:
                            attribute_value = attribute.toString("yyyy-MM-dd")
                        else:
                            attribute_value = try_parse_json(attribute)
                        
                        updated = {attribute_name : attribute_value}
                        feature_with_lock["features"][idx]["properties"].update(updated)
                
                    if fid in changed_geometries:
                        geometry = changed_geometries[fid]
                        feature_with_lock['features'][idx]['geometry'] = json.loads(geometry.asJson())
                        changed_geometries.pop(fid)

                    feature_with_lock["features"][idx]['update'] = {'action': 'Replace'}
                # If editing line attribute, and there is a feature with geometry_properties set, replace it also (should be polygon)
                elif "geometry_properties" in feature_with_lock["features"][idx]:
                    feature_with_lock["features"][idx]['update'] = {'action': 'Replace'}
                features = features + [feature_with_lock["features"][idx]]
        
        for fid, geometry in changed_geometries.items():
            
            if fid in ids_deleted: continue

            changed_feature = lyr.getFeature(fid)

            # TODO support for delt geometri
            feature_with_lock = self.lock_feature(lyr, changed_feature)

            feature_with_lock['features'][0]['geometry'] = json.loads(geometry.asJson())
            
            feature_with_lock['features'][0]['update'] = {'action': 'Replace'}
            features = features + feature_with_lock["features"]
        
        return features

    def handle_committed_features_removed(self, lyr, deleted_features):
        
        features = []
        for deleted_feature in deleted_features:
            
            feature_with_lock = self.lock_feature(lyr, deleted_feature)

            feature_with_lock['features'][0]['update'] = {'action': 'Erase'}
            features = features + feature_with_lock["features"]
        return features

    def handle_committed_features_added(self, lyr, added_features):
        features = []
        for fid, feature in added_features.items():
            
            export = QgsJsonExporter(lyr)
            export.setSourceCrs(QgsCoordinateReferenceSystem())
            
            identifikasjon_idx = feature.fieldNameIndex('identifikasjon')
            
            try:
                identifikasjon_value = json.loads(feature.attribute('identifikasjon'))
            except Exception:
                raise Exception("Kunne ikke tolke identifikasjonsattributtet")

            identifikasjon_value["lokalId"] = str(uuid.uuid4())
            feature.setAttribute('identifikasjon', identifikasjon_value)

            feature.setAttribute('featuretype', self.feature_type_dictionary[lyr.id()])
            feature_json = json.loads(export.exportFeature(feature))
            
            # Don't include null values in json, Ngis open API doesn't like it
            prop_for_deletion = []
            for property_name, property_value in feature_json['properties'].items():
                if not property_value:
                    prop_for_deletion.append(property_name)
                else:
                    feature_json['properties'][property_name] = try_parse_json(property_value)
            for prop in prop_for_deletion:
                del feature_json['properties'][prop]
            
            feature_json['update'] = {"action":"Create"}
            features.append(feature_json)

            # Update QGIS layer with new uuid, must be string (not json)
            feature.setAttribute('identifikasjon', json.dumps(identifikasjon_value))
            lyr.updateFeature(feature)

        return features

    def handle_altered_features(self, lyr, features):
       
        try:

            if len(features) == 0:
                self.iface.messageBar().pushMessage("Success", "Ingen endringer ble sjekket inn i NGIS-OpenAPI", level=3, duration=3)
                return

            json_dict = {"type": "FeatureCollection", "features" : None, "crs" : None}
            
            crs = lyr.crs().authid()
            crs_epsg = authid_to_code(crs)
            json_dict.update(create_crs_entry(crs))
            json_dict['features'] = features

            datasetid = self.dataset_dictionary[lyr.id()]
            return_data = self.client.updateDatasetFeature(datasetid, crs_epsg, json_dict)
            self.iface.messageBar().pushMessage("Success", "Endringene er lagret", str(return_data), level=3, duration=10)
            
        except Exception as e:
            error = ApiError("Lagring mislyktes", "Kunne ikke lagre endringene", e)
            self.iface.messageBar().pushMessage(error.title, error.detail, error.show_more, level=2, duration=10)
            return

    def run(self):
        """Run method that performs all the real work"""
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started

        if self.first_start == True:
            self.first_start = False
            # Get previous login method if any
            s = QgsSettings()
            auth_method_id = s.value("ngisopenapi/auth_method_id", "")
            #keep a modeless dialog window on top of the main QGIS window.
            self.dlg = NgisOpenApiClientDialog(self.iface.mainWindow())
            self.dlg.mAuthConfigSelect.setConfigId(auth_method_id)
            self.dlg.logInButton.clicked.connect(self.handle_login)
            self.dlg.logOutButton.clicked.connect(self.handle_logout)
            self.dlg.addLayerButton.clicked.connect(self.handle_add_layer)
            
        # show the dialog
        self.dlg.show()