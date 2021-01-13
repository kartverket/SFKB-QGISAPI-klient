from qgis.core import QgsSettings, QgsApplication, QgsAuthMethodConfig, QgsOgcUtils

class NgisOpenApiClientAuthentication:

    def getConfig(self, auth_method_id):
        
        auth_cfg = QgsAuthMethodConfig()
        auth_mgr = QgsApplication.authManager()
        auth_mgr.loadAuthenticationConfig(auth_method_id, auth_cfg, True)

        # Default values
        username = None,
        password = None,
        url = "https://openapi-test.kartverket.no/v1/"

        if auth_cfg.id():
            username = auth_cfg.config('username', '')
            password = auth_cfg.config('password', '')
        
        if auth_cfg.uri():
            url = auth_cfg.uri()

        return url, username, password