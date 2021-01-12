# infolica
Fork and clone Infolica.  

## Production
### back
Open a cmd window and move to back folder.
```
cd back
```
Create a Python virtual environment with venv 
```
python -m venv env
```
Launch the virtual environment  
```
env/Scripts/activate
```
Install requirements  
```
pip install -r requirements.txt
```

Make your changes in config files.
Rename `production.ini.template` to `production.ini`.
Open the file and adapt `sqlalchemy.url`, `ldap_url`, `ldap_passwd` and all the config according to your needs.

> :warning: Infolica is based on PG Database and depends on some geographical components. Make sure to add the `postgis` extension to your database schema.

Install the project in editable mode
```
pip install -e .
```

To test if the backend is responding, type the following in your virtual env. It will serve your api.
```
pserve --reload development.ini
```
In a web browser, check this url:
```
localhost:6543/infolica/api/test
```
If you can read "Yeah, your api is working!", your installation is running correctly.


### front
Move to front.
```
cd ../front
```

Duplicate the `.env` file to `env.development.local` for development or `env.production.local` for production and adapt urls and config. Files ending with `*.local` are ignored by git.

Install dependencies.
```
npm install
```

Then build with:
```
npm run build [-- --mode production]
```

### Development

When developping and to avoid getting cross-origin issues with the application cookie, one should proxy the whole application through Apache.

To do so, you need Apache installed on your computer and add the following configuration:

```
<location /infolica_api>
    Require all granted
</location>
<location /infolica/>
    Require all granted
</location>

SSLProxyEngine on
SSLProxyVerify none
SSLProxyCheckPeerCN off
ProxyPass "/infolica_api/" "http://localhost:6543/"
ProxyPassReverse "/infolica_api/"  "http://localhost:6543/"
ProxyPass "/infolica/" "http://localhost:8080/infolica/"
ProxyPassReverse "/infolica/"  "http://localhost:8080/infolica/"

ProxyPreserveHost On
RequestHeader set X-Forwarded-Proto "https"
RequestHeader set X-Forwarded-Port "443"
ProxyRequests Off

```

Then in your local `.env.development.local` file:

```
VUE_APP_API_URL = "http://localhost/infolica_api/infolica/api"
```

### Install and configure Apache
If you already have an Apache with mod_wsgi enabled, switch to Apache configuration step.

You'll need to have an Apache 32bits if your python is 32bits or Apache 64bits if your python is 64bits. Download a pre-compiled wheel of mod_wsgi for python: https://www.lfd.uci.edu/~gohlke/pythonlibs/ in the root folder of your project. Make sure to choose the right version.

1. Install the wheel with pip install. Make sure you have Microsoft Visual C++ installed on your machine. 
For an Apache 2.4, 64bits with Python 3.7 and Microsoft Visual C++ 15, download file mod_wsgi‑4.7.1+ap24vc15‑cp37‑cp37m‑win_amd64.whl on (https://www.lfd.uci.edu/~gohlke/pythonlibs/)[https://www.lfd.uci.edu/~gohlke/pythonlibs/
```
pip install .\mod_wsgi-4.6.4+ap24vc15-cp37-cp37m-win_amd64.whl
mod_wsgi-express module-config
```
2. You'll have an output showing the path of the generated wsgi module. Copy the module to your Apache modules folder (replace c:\Apache with your installation folder) and rename it with .so extension:

```
cp .\env\Lib\site-packages\mod_wsgi\server\mod_*.pyd C:\Apache24\modules\mod_wsgi.so
```

3. In the conf\httpd.conf file of your Apache installation directory, add this line to enable mod_wsgi:
```
LoadModule wsgi_module modules/mod_wsgi.so
```

### Apache configuration

1. Rename the apache/wsgi.conf.sample file to wsgi.conf and adapt the paths according to your setup.

2. Finally, make your apache aware of your app by adding to the end of your httpd.conf file:
```
Include path\to\your\project\apache\*.conf
```
3. Restart apache



