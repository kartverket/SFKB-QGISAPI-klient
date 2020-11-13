import os.path,  sys

# Set up current path.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import swagger_client
from swagger_client.rest import ApiException
from swagger_client.api_client import ApiClient
import re


class NgisHttpClient: 

    configuration = None
    x_client_product_version = 'ExampleApp 10.0.0 (Build 54321)'
    metadata_api_instance = None
    features_api_instance = None
    
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

    def updateDatasetFeature(self, dataset_id, body):
        self.features_api_instance.api_client.set_default_header("Content-Type", "application/vnd.kartverket.sosi+json;crs_EPSG=25832")
        return_data, status, headers = self.features_api_instance.update_dataset_features_with_http_info(body, self.x_client_product_version, dataset_id)
        return return_data, status, headers

    def getDatasetFeature(self, dataset_id, local_id):
        self.features_api_instance.api_client.set_default_header("Accept", "application/vnd.kartverket.sosi+json;crs_EPSG=25832")
        locking = swagger_client.Locking(type="user_lock")
        feature = self.features_api_instance.get_dataset_feature(self.x_client_product_version, dataset_id, local_id, references='none', locking=locking)
        return feature

    def getDatasetFeatureWithLock(self, dataset_id, lokal_id):

        path_params = {
                "datasetId": dataset_id,
                "lokalId" : lokal_id
        }
        query_params = [("locking[type]", "user_lock"), ("references", "none")]
        header_params = {
            "X-Client-Product-Version" : "ExampleApp 10.0.0 (Build 54321)",
            "Accept" : "application/vnd.kartverket.sosi+json;crs_EPSG=25832"
        }

        feature = self.features_api_instance.api_client.call_api(
            '/datasets/{datasetId}/features/{lokalId}',
            'GET',
            path_params,
            query_params,
            header_params,
            response_type='object',
            auth_settings=["basicAuth"],
            _return_http_data_only=True
        )

        return feature


    def getDatasetFeatures(self, dataset_id, bbox, crs_epsg, limit=None):
        try:
            bbox = bbox['ll']+bbox['ur']
            #bbox = [299669,6531760,336409,6578591] # Stavanger
            bbox = ','.join(map(str, bbox))

            self.features_api_instance.api_client.set_default_header("Accept", "application/vnd.kartverket.sosi+json;crs_EPSG=25832")

            if limit:
                return_data, status, headers = self.features_api_instance.get_dataset_features_with_http_info(self.x_client_product_version, dataset_id, references='none', locking='', limit=limit, bbox=bbox, crs_epsg=crs_epsg)
            else:
                return_data, status, headers = self.features_api_instance.get_dataset_features_with_http_info(self.x_client_product_version, dataset_id, references='none', locking='', bbox=bbox, crs_epsg=crs_epsg)
            if 'Link' in headers:
                pass
                # Paging required
                # url = re.search('<(.*)>;', headers['Link'])
                # url = url.group(1)
            return return_data
        except ApiException as e:
            print("Exception when calling FeaturesApi->get_dataset_feature: %s\n" % e)
