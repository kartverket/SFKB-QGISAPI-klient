from qgis.core import QgsSettings, QgsApplication, QgsAuthMethodConfig, QgsOgcUtils

class NgisOpenApiClientAuthentication:

    def getUser(self, auth_method_id):
        
        auth_cfg = QgsAuthMethodConfig()
        auth_mgr = QgsApplication.authManager()
        auth_mgr.loadAuthenticationConfig(auth_method_id, auth_cfg, True)

        if auth_cfg.id():
            username = auth_cfg.config('username', '')
            password = auth_cfg.config('password', '')
            return username, password
        else:
           return None, None