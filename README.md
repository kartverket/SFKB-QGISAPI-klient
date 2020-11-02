***In Progress***



### Plugin Builder Results

Congratulations! You just built a plugin for QGIS!  

Your plugin **NgisOpenApiClient** was created in:  
  **C:\Projects\Kartverket\NGIS Open API Client\ngis_openapi_client**

Your QGIS plugin directory is located at:  
  **C:/Users/*<username\>*/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins**

### What's Next

1.  If resources.py is not present in your plugin directory, compile the resources file using pyrcc5 (simply use **pb_tool** or **make** if you have automake)
2.  Optionally, test the generated sources using **make test** (or run tests from your IDE)
3.  Copy the entire directory containing your new plugin to the QGIS plugin directory (see Notes below)
4.  Test the plugin by enabling it in the QGIS plugin manager
5.  Customize it by editing the implementation file **ngis_openapi_client.py**
6.  Create your own custom icon, replacing the default **icon.png**
7.  Modify your user interface by opening **ngis_openapi_client_dialog_base.ui** in Qt Designer

Notes:

*   You can use **pb_tool** to compile, deploy, and manage your plugin. Tweak the _pb_tool.cfg_ file included with your plugin as you add files. Install **pb_tool** using _pip_ or _easy_install_. See **http://loc8.cc/pb_tool** for more information.
*   You can also use the **Makefile** to compile and deploy when you make changes. This requires GNU make (gmake). The Makefile is ready to use, however you will have to edit it to add addional Python source files, dialogs, and translations.

</div>

<div style="font-size:.9em;">

For information on writing PyQGIS code, see **http://loc8.cc/pyqgis_resources** for a list of resources.

</div>

©2011-2019 GeoApt LLC - geoapt.com
