import os.path,  sys

# Set up current path.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import swagger_client
from swagger_client.rest import ApiException
from swagger_client.api_client import ApiClient
import re
from urllib import parse

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
        datasets = self.metadata_api_instance.get_datasets(self.x_client_product_version)
        return datasets
    
    def getDatasetMetadata(self, dataset_id):
        dataset_metadata = self.metadata_api_instance.get_dataset_metadata(self.x_client_product_version, dataset_id)
        return dataset_metadata


    def updateDatasetFeature(self, dataset_id, crs_epsg, body):
        self.features_api_instance.api_client.set_default_header("Accept", "application/vnd.kartverket.ngis.edit_features_summary+json")
        self.features_api_instance.api_client.set_default_header("Content-Type", "application/vnd.kartverket.sosi+json")

        feature = self.features_api_instance.update_dataset_features(body, self.x_client_product_version, dataset_id, locking_type='user_lock', crs_epsg=crs_epsg)
        return feature

    def getDatasetFeatureWithLock(self, dataset_id, lokal_id, crs_epsg, references='none'):
        self.features_api_instance.api_client.set_default_header("Accept", "application/vnd.kartverket.sosi+json")
        feature = self.features_api_instance.get_dataset_feature(self.x_client_product_version, dataset_id, lokal_id, references=references, locking_type='user_lock', crs_epsg=crs_epsg)
        return feature
    
    def getDatasetFeatureWithoutLock(self, dataset_id, lokal_id, crs_epsg, references='none'):
        self.features_api_instance.api_client.set_default_header("Accept", "application/vnd.kartverket.sosi+json")
        feature = self.features_api_instance.get_dataset_feature(self.x_client_product_version, dataset_id, lokal_id, references=references, crs_epsg=crs_epsg)
        return feature

    def getDatasetFeatures(self, dataset_id, bbox, crs_epsg, limit=None, references='none'):
        
        bbox = bbox['ll']+bbox['ur']
        bbox = ','.join(map(str, bbox))

        self.features_api_instance.api_client.set_default_header("Accept", "application/vnd.kartverket.sosi+json")

        # Preconfigured limit
        if limit:
            return_data, _, headers = self.features_api_instance.get_dataset_features_with_http_info(self.x_client_product_version, dataset_id, references=references, limit=limit, bbox=bbox, crs_epsg=crs_epsg)
        # Use max limit provided by API
        else:
            return_data, _, headers = self.features_api_instance.get_dataset_features_with_http_info(self.x_client_product_version, dataset_id, references=references, bbox=bbox, crs_epsg=crs_epsg)
        # Paging required
        while 'Link' in headers:
            m = re.search('<(.+?)>', headers['Link'])
            if m:
                url = m.group(1)
                queryparams = dict(parse.parse_qsl(parse.urlsplit(url).query))
                cursor = queryparams['cursor']
                limit = queryparams['limit']
                paged_features, _, headers = self.features_api_instance.get_dataset_features_with_http_info(self.x_client_product_version, dataset_id, references=references, limit=limit, cursor=cursor, bbox=bbox, crs_epsg=crs_epsg)
                return_data['features'] = return_data['features'] + paged_features['features']
        return return_data
