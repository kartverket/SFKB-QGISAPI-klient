import os.path,  sys
# Set up current path.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import openapi_client
from openapi_client.rest import ApiException

class NgisHttpClient: 

    configuration = None
    x_client_product_version = 'ExampleApp 10.0.0 (Build 54321)'
    
    def __init__(self, host, username, password): 
        self.configuration = openapi_client.Configuration(
            host=host,
            username=username,
            password=password)

    def getAvailableDatasets(self):
        with openapi_client.ApiClient(self.configuration) as api_client:
            try:
                metadata_api_instance = openapi_client.MetadataApi(api_client)
                datasets = metadata_api_instance.get_datasets(self.x_client_product_version)
                return datasets
            except ApiException as e:
                print("Exception when calling FeaturesApi->get_dataset_feature: %s\n" % e)
    
    def getDatasetMetadata(self, dataset_id):
        with openapi_client.ApiClient(self.configuration) as api_client:
            try:
                metadata_api_instance = openapi_client.MetadataApi(api_client)
                dataset_metadata = metadata_api_instance.get_dataset_metadata(self.x_client_product_version, dataset_id)
                return dataset_metadata
            except ApiException as e:
                print("Exception when calling FeaturesApi->get_dataset_feature: %s\n" % e)

    def getDatasetFeatures(self, dataset_id, bbox, crs_epsg, limit=None):
        with openapi_client.ApiClient(self.configuration) as api_client:
            try:
                bbox = bbox['ll']+bbox['ur']
                bbox = [413681,6407221,462775,6470601] # TODO Remove 
                bbox = ','.join(map(str, bbox))
                features_api_instance = openapi_client.FeaturesApi(api_client)
                if limit:
                    api_response = features_api_instance.get_dataset_features(self.x_client_product_version, dataset_id, references='none', locking='', limit=limit, bbox=bbox, crs_epsg=crs_epsg)
                else:
                    api_response = features_api_instance.get_dataset_features(self.x_client_product_version, dataset_id, references='none', locking='', bbox=bbox, crs_epsg=crs_epsg)
                return api_response
            except ApiException as e:
                print("Exception when calling FeaturesApi->get_dataset_feature: %s\n" % e)
