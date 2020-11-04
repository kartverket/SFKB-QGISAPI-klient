import os.path,  sys
# Set up current path.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import swagger_client
from swagger_client.rest import ApiException

class NgisHttpClient: 

    configuration = None
    x_client_product_version = 'ExampleApp 10.0.0 (Build 54321)'
    
    def __init__(self, host, username, password): 
        self.configuration = swagger_client.Configuration()
        self.configuration.host=host
        self.configuration.username=username
        self.configuration.password=password
        # DEBUG FIDDLER
        #self.configuration.proxy = "https://127.0.0.1:8888"
        #self.configuration.verify_ssl = False

    def getAvailableDatasets(self):
        try:
            metadata_api_instance = swagger_client.MetadataApi(swagger_client.ApiClient(self.configuration))
            datasets = metadata_api_instance.get_datasets(self.x_client_product_version)
            return datasets
        except ApiException as e:
            print("Exception when calling FeaturesApi->get_dataset_feature: %s\n" % e)
    
    def getDatasetMetadata(self, dataset_id):
        try:
            metadata_api_instance = swagger_client.MetadataApi(swagger_client.ApiClient(self.configuration))
            dataset_metadata = metadata_api_instance.get_dataset_metadata(self.x_client_product_version, dataset_id)
            return dataset_metadata
        except ApiException as e:
            print("Exception when calling FeaturesApi->get_dataset_feature: %s\n" % e)

    def getDatasetFeatures(self, dataset_id, bbox, crs_epsg, limit=None):
        try:
            bbox = bbox['ll']+bbox['ur']
            bbox = [413681,6407221,462775,6470601] # TODO Remove 
            bbox = ','.join(map(str, bbox))
            features_api_instance = swagger_client.FeaturesApi(swagger_client.ApiClient(self.configuration))
            if limit:
                api_response = features_api_instance.get_dataset_features(self.x_client_product_version, dataset_id, references='none', locking='', limit=limit, bbox=bbox, crs_epsg=crs_epsg)
            else:
                api_response = features_api_instance.get_dataset_features(self.x_client_product_version, dataset_id, references='none', locking='', bbox=bbox, crs_epsg=crs_epsg)
            return api_response
        except ApiException as e:
            print("Exception when calling FeaturesApi->get_dataset_feature: %s\n" % e)
