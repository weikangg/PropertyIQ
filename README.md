<h1 align="center"> :house_with_garden: PropertyIQ</h1>

![homepage](https://user-images.githubusercontent.com/95838788/222974513-96d5ad6a-55ca-4d5b-b0d1-1ba060eaee57.png)
PropertyIQ is a web application that organises and makes accessible relevant market data and is the the go-to source for up-to-date information and trends in the Singapore housing rental market.

<h2 align="center"> :axe:	Prerequsite</h2>

#### Internet Connectivity Required
> Prerequsite software/hardware
* Operating System: Windows 10/11, macOS Catalina above
* Visual Studio Code
  + https://code.visualstudio.com/
* Pgadmin 4 (Graphical User Interface to interact with the database)
  + https://www.pgadmin.org/download/
* PostgreSQL 15
  + https://www.postgresql.org/download/ (Windows)
  + https://postgresapp.com/ (Mac)
* Python 3.9 above
  + https://www.python.org/downloads/

> Prerequsite API Keys Required
* URA API 
  + https://www.ura.gov.sg/maps/api/#introduction <br/>
    a. Register for an account. Fill in NA for Company Name, and put in arbitrary URL (e.g. https://www.google.com) <br/>
    b. Go to your email and open the confirmation email titled 'URA Data Request - Approved'. <br/>
    c. Click on the link and the button to generate access key. <br/>
    d. Go back to your email and open the email titled 'URA Data Request - Access key'.  <br/>
    e. You should see your URA API key there which is required for PropertyIQ. <br/>
* Google Maps API
  + https://www.youtube.com/watch?v=OGTG1l7yin4 (Step-by-step tutorial on how to acquire API Key) <br/>
    a. Go to https://console.cloud.google.com. <br/>
    b. Create a new Project. Name it however you want. <br/>
    c. Open the sidebar, click **API & Services**, then click on **Library**. <br/>
    d. Search for or click on **Maps Javascript API**. <br/>
    e. Enable it. <br/>
    f. Open the sidebar again, click **API & Services**, then click on **Credentials**. <br/>
    g. Click on Create Credentials, then click on API Key. <br/>
    h. And you're done, that's the API key required for our Google Maps Services for PropertyIQ. <br/>
    
>Prerequsite (Others)
* Clone this project

<h2 align="center"> :hammer_and_wrench:	Setup</h2>

>Setup

Please follow carefully during the setup process. 

The following was done using a window 11 system, macOS should be relatively similar. Your mileage may vary. 
1) Create a Python virtual environment in VS Code.
2) Start the virtual environment.
3) Install dependencies.

https://code.visualstudio.com/docs/python/environments#_using-the-create-environment-command
```
Opening the Command Palette (Ctrl+Shift+P), start typing the Python: Create Environment 
Creating an environment using Venv
Select interpreter path i.e. python
Checked to also install dependencies
```

![Venv](https://user-images.githubusercontent.com/101249007/229971014-ef4fa6a1-12f2-4912-8f42-12f0b04175e7.png)
![dependencies](https://user-images.githubusercontent.com/101249007/229971506-ed8eaace-682c-471a-b52d-dc5f2dea6a59.png)

Note: You can also manually install dependencies using the following command in the terminal.
```
pip install -r requirements.txt
```

4) Setup of PostgreSQL and database

Download and install both pgAdmin and PostgreSQL.

Install Postgres without changing anything, except entering of master **password**.

Open the SQL shell by entering ```psql``` in your Windows search menu.

![sqlshell](https://user-images.githubusercontent.com/101249007/229972618-3caca049-d343-4fb1-a578-e0759adc9ff5.png)

Inside SQL shell, keep pressing enter until it prompts you for your **password** which you created during the installation. Type your password here even though it doesn't look like it is being keyed in. Press enter once done.

It should look like this.
Note: If you receive a warning on console code page, you can safety ignore.
![sqlconsole](https://user-images.githubusercontent.com/101249007/229973960-a0ecce39-b44d-45ff-b6eb-9e1fb0a4a942.png)

Follow the below commands in the PSQL shell:

To create the database of propertyiq

To list the databases 
```
postgres=# CREATE DATABASE propertyIQ OWNER postgres;
postgres=# \l 
```
It should look like this.

![databaseConsole](https://user-images.githubusercontent.com/101249007/229973874-c69fc3fe-d975-405c-8e41-3f9c2187d87c.png)

5) Create a .env file in the root directory & store relevant information. 
<strong>Ensure that the names match exactly. e.g. 'POSTGRE_USER' must be stored exactly as POSTGRE_USER in the .env file without any typos. </strong>
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
It should look like this:
![env](https://user-images.githubusercontent.com/101249007/229975509-258a53f7-6b9e-48f2-b9a9-523626318586.png)

> pgAdmin

In the event you want to view the database you can use pgAdmin.
In pgAdmin , enter the same **password** from **PostgreSQL** and you should then see the following.
Click on server database icon top left and add the password which you entered in psql.

![databasepgAdmin](https://user-images.githubusercontent.com/101249007/229968141-222fc0a4-7205-4476-ba8d-9bc805340bf8.png)
![table](https://user-images.githubusercontent.com/101249007/229976693-f58bd915-b883-4978-bdee-4881f6c2d63f.png)


<h2 align="center"> :runner: Starting the server</h2>

> Create superuser
```
python manage.py createsuperuser
```
Eg:

Username: propertyIQ

Password: sc2006_1234

>setting up and running the server
```
python manage.py migrate
python manage.py runserver
```
Note: duirng migrations it should be all green!
![runserver](https://user-images.githubusercontent.com/101249007/229977063-187fcaac-ba1e-4b4c-8e98-83f9d89295b6.png)

>first-time setup

In the website, login as the superuser. In your dashboard and click update property list.
#### NOTE: THIS WILL TAKE A WHILE ~5MIN ON A FAST INTERNET CONNECTION.

![updatedatabase](https://user-images.githubusercontent.com/101249007/229977806-d0e7a831-7f37-4916-80fe-cc86bf740bf4.jpeg)


<h1 align="center"> :confetti_ball: Congratulations! :confetti_ball:</h1>

### Now, you can explore PropertyIQ locally on your machine!


<h2 align="center"> :question: FAQ</h2>

> <strong>1. How do I start the production server?</strong>
```
Run python manage.py runserver in the console.
```

> <strong>2. How do I create a super user?</strong>

Run this in the console and follow the instructions. Type your password even though it doesn't look like it is being keyed in. Press enter once done.
```
python manage.py createsuperuser
```

> <strong>3. How do I delete the properties in VS code?</strong>
```
python manage.py shell
from property.models import Property
Property.objects.all().delete()
```

> <strong>4. How do I delete the database? I can't do it from the Pgadmin GUI.</strong>

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

RUN THESE COMMANDS and replace the database name i.e.```propertyiq``` appropriately to your own database name. This should work.

```
update pg_database set datallowconn = 'false' where datname = 'propertyiq';
select pg_terminate_backend(pg_stat_activity.pid) from pg_stat_activity where pg_stat_activity.datname = 'propertyiq';
drop database propertyiq;
```

Note: Should you need to uninstall/re-install you will need to manually delete the folder where you have installed Postgres and pgadmin. This is even after uninstalling from system settings. For some reason, Postgres folder's don't remove entirely even though you select the option.

> <strong>5. I don't see any properties after I set everything up. Why is that so?</strong>
```
1. Create a super user by typing python manage.py createsuperuser in the console.
2. Login on the web page with that super user account.
3. Go to the Dashboard.
4. Press Update Listings Button.
5. Wait for about 1-2 minutes patiently and grab a cup of coffee.
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
