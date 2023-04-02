<h1 align="center"> :house_with_garden: PropertyIQ</h1>

![Screenshot 2023-03-01 193840](https://user-images.githubusercontent.com/95838788/222974513-96d5ad6a-55ca-4d5b-b0d1-1ba060eaee57.png)

PropertyIQ is a web application that organises and makes accessible relevant market data and is the the go-to source for up-to-date information and trends in the Singapore housing rental market.

<h2 align="center"> :hammer_and_wrench:	Setup</h2>

1) Create Python virtual environment in VS Code 
2) Start virtual environment
3) Install dependencies 

https://code.visualstudio.com/docs/python/environments#_using-the-create-environment-command
```
Opening the Command Palette (Ctrl+Shift+P), start typing the Python: Create Environment 

Creating an environment using Venv

pip install -r requirements.txt
```

4) Setup [PostgreSQL](#postgresql-setup).

5) Create a .env file & store relevant information. <strong>Ensure that the names match exactly. e.g. 'POSTGRE_USER' must be stored exactly as POSTGRE_USER in the .env file without any typos. </strong>
```
POSTGRE_USER = <YOUR POSTGRESQL USER>
POSTGRE_PASSWORD = <YOUR POSTGRESQL PASSWORD>
```

6) Get URA API Key from URA Website & Add it to the .env file.
```
URA_API_KEY = <YOUR URA API KEY>
```

7) Get Google Maps API Key & Add it to the .env file.
```
GOOGLE_MAPS_KEY = <YOUR GOOGLE MAPS KEY>
```

<h2 align="center">
	<code><img height="50" src="https://user-images.githubusercontent.com/25181517/117208740-bfb78400-adf5-11eb-97bb-09072b6bedfc.png" alt="PostgreSQL" title="PostgreSQL" /></code> PostgreSQL Setup
</h2>

- Download and install both pgAdmin and PostgreSQL.

Install Postgres without changing anything, except entering of master **password**.

Open the SQL shell by entering ```psql``` in your Windows search menu.

Inside SQL shell, keep pressing enter until it prompts you for your **password** which you created during the installation. Type your password here even though it doesn't look like it is being keyed in. Press enter once done.

It should look like...
```
Server [localhost]:
Database [postgres]:
Port [5432]:
Username [postgres]:
Password for user postgres:

postgres=# 
```

Install pgAdmin , enter the password from psql and you should then see the following...

Click on server database icon top left and add the password which you entered in psql.

Follow the below commands in the PSQL shell.
```
postgres=# CREATE DATABASE propertyIQ OWNER postgres;
//To create the database of propertyiq
postgres=# \l 
//To list the databases 
```
Finally, go to pgAdmin, and refresh the page.

Note: Should you need to uninstall/re-install you will need to manually delete the folder where you have installed Postgres and pgadmin. This is even after uninstalling from system settings. For some reason, Postgres folder's don't remove entirely even though you select the option.

## Super-user for Django-admin
```python manage.py createsuperuser```

Type your password here even though it doesn't look like it is being keyed in. Press enter once done.

Username: propertyIQ    
Password: sc2006_1234

<h2 align="center"> :question:	 FAQ:</h2>

> <strong>1. How do I start the production server?</strong>
```
Run python manage.py runserver in the console.
```

> <strong>2. How do I create a super user?</strong>
```
Run python manage.py createsuperuser in the console and follow the instructions.
```
> <strong>3. How do I delete the properties from my database?</strong>
```
python manage.py shell
from property.models import Property
Property.objects.all().delete()
```
> <strong>4. How do I drop the database? I can't do it from the Pgadmin GUI.

Open the SQL shell by entering ```psql``` in your Windows search menu.

Inside SQL shell, keep pressing enter until it prompts you for your **password** which you created during the installation. Type your password here even though it doesn't look like it is being keyed in. Press enter once done.

It should look like...
```
Server [localhost]:
Database [postgres]:
Port [5432]:
Username [postgres]:
Password for user postgres:

postgres=# 
```
RUN THESE COMMANDS and change the database name appropriately to your own database name. This should work.
```
update pg_database set datallowconn = 'false' where datname = 'propertyiq';
select pg_terminate_backend(pg_stat_activity.pid) from pg_stat_activity where pg_stat_activity.datname = 'propertyiq';
drop database propertyiq;
```

<h2 align="center"> 🛠 Tech Stack:</h2>

<div align="center">
  <h3>Frontend</h3>
  <p>
    <a href="https://skillicons.dev">
      <img src="https://skillicons.dev/icons?i=html,css,js,bootstrap,django" />
    </a>
  </p>
  <h3>Backend</h3>
  <p>
    <a href="https://skillicons.dev">
      <img src="https://skillicons.dev/icons?i=django,postgresql,py" />
    </a>
  </p>
  <br />
</div>
