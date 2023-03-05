# PropertyIQ

PropertyIQ is a web application that organises and makes accessible relevant market data and is the the go-to source for up-to-date information and trends in the Singapore housing rental market.

## Setup

1) Create Python virtual environment in VS Code 
2) Start virtual environment
3) Install dependencies 


https://code.visualstudio.com/docs/python/environments#_using-the-create-environment-command
```
opening the Command Palette (Ctrl+Shift+P), start typing the Python: Create Environment 

Creating an environment using Venv

pip install -r requirements.txt
```

4) Setup [PostgreSQL](##-PostgreSQL-Setup).

5) Create a .env file & store relevant information.
```
POSTGRE_USER: <YOUR POSTGRESQL USER>
POSTGRE_PASSWORD: <YOUR POSTGRESQL PASSWORD>
```

6) Get URA API Key from URA Website & Add it to the .env file.
```
URA_API_KEY = <YOUR URA API KEY>
```

7) Get Google Maps API Key & Add it to the .env file
```
GOOGLE_MAPS_KEY = <YOUR GOOGLE MAPS KEY>
```

8) Setup Gmail Sending
https://stackoverflow.com/questions/6914687/django-sending-email
```
Follow this link and create an application specific password, then store the relevant information in he same .env file.

GMAIL_EMAIL : <YOUR EMAIL> (e.g. test@test.com)
GMAIL_APP_PASSWORD: <YOUR GMAIL APP PASSWORD> (e.g. asdadadadsada [16 characters long])
```

## PostgreSQL Setup

- Download and install both pgadmin and PostgreSQL.

Install Postgres without changing anything, except entering a new password and open the SQL shell by entering 'psql' in your Windows search menu.
Inside SQL shell, keep pressing enter until it prompts you for your password which you created on the installer
Type your password here, even though it doesn't look like it is being keyed in and press enter once done.

It should look like...
```
Server [localhost]:
Database [postgres]:
Port [5432]:
Username [postgres]:
Password for user postgres:
psql (12.2)
 
WARNING: Console code page (850) differs from Windows code page (1252)
8-bit characters might not work correctly. See psql reference
page "Notes for Windows users" for details.
Type "help" for help.

postgres=# 
```

Install pgadmin , enter the password from psql and you should then see the following...

Click on server database icon top left and add the password which you entered in psql.

Follow the below commands in the PSQL shell.

postgres=# CREATE DATABASE propertyIQ OWNER postgres; #Click enter here
CREATE DATABASE #result
postgres=# \l #to get the below datbase list

Finally, go to pg admin, and refresh the page.

Note: Should you need to uninstall/re-install you will need to manually delete the folder where you have installed Postgres and pgadmin. This is even after uninstalling from system settings. For some reason, Postgres folder's don't remove entirely even though you select the option.

## Super-user for Django-admin
Username: propertyIQ    
Password: sc2006_1234

## Testing URA API 
- Go to test folder and run Main.py
- Data received should be outputted to propertyData.json

## Testing Google Maps API
- Go to test.html and run it on live server (VSCode Extension)
