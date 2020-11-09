import os.path,  sys
# Set up current path.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import swagger_client
from swagger_client.rest import ApiException
from swagger_client.api_client import ApiClient
import custom_modules
import re


class NgisHttpClient: 

    configuration = None
    x_client_product_version = 'ExampleApp 10.0.0 (Build 54321)'
    metadata_api_instance = None
    features_api_instance = None
    custom_api_instance = None
    
    def __init__(self, host, username, password): 
        self.configuration = swagger_client.Configuration()
        self.configuration.host=host
        self.configuration.username=username
        self.configuration.password=password
        # DEBUG FIDDLER
        #self.configuration.proxy = "https://127.0.0.1:8888"
        #self.configuration.verify_ssl = False
        
        self.metadata_api_instance = swagger_client.MetadataApi(swagger_client.ApiClient(self.configuration))
        self.features_api_instance = swagger_client.FeaturesApi(swagger_client.ApiClient(self.configuration))
        self.custom_api_instance = custom_modules.CustomApi(swagger_client.ApiClient(self.configuration))

    def getAvailableDatasets(self):
        try:
            datasets = self.metadata_api_instance.get_datasets(self.x_client_product_version)
            return datasets
        except ApiException as e:
            print("Exception when calling FeaturesApi->get_dataset_feature: %s\n" % e)
    
    def getDatasetMetadata(self, dataset_id):
        try:
            dataset_metadata = self.metadata_api_instance.get_dataset_metadata(self.x_client_product_version, dataset_id)
            return dataset_metadata
        except ApiException as e:
            print("Exception when calling FeaturesApi->get_dataset_feature: %s\n" % e)

    def createDatasetFeatures(self, dataset_id, body):
        return_data, status, headers = self.features_api_instance.update_dataset_features_with_http_info(body, self.x_client_product_version, dataset_id)

    def getDatasetFeatures(self, dataset_id, bbox, crs_epsg, limit=None):
        try:
            bbox = bbox['ll']+bbox['ur']
            bbox = ','.join(map(str, bbox))
            if limit:
                return_data, status, headers = self.features_api_instance.get_dataset_features_with_http_info(self.x_client_product_version, dataset_id, references='none', locking='', limit=limit, bbox=bbox, crs_epsg=crs_epsg)
            else:
                return_data, status, headers = self.features_api_instance.get_dataset_features_with_http_info(self.x_client_product_version, dataset_id, references='none', locking='', bbox=bbox, crs_epsg=crs_epsg)
            if 'Link' in headers:
                pass
                # Paging required
                # url = re.search('<(.*)>;', headers['Link'])
                # url = url.group(1)
                # return_data, status, headers = self.custom_api_instance.get_url_with_http_info(self.x_client_product_version, url)
            return return_data
        except ApiException as e:
            print("Exception when calling FeaturesApi->get_dataset_feature: %s\n" % e)
