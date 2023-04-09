<h1 align="center"> :house_with_garden: PropertyIQ</h1>

![homepage](https://user-images.githubusercontent.com/95838788/230757684-8aaebac0-a8f7-46a0-8e8f-27a224f03d34.png)

PropertyIQ is a web application that organises and makes accessible relevant market data and is the the go-to source for up-to-date information and trends in the Singapore housing rental market.

<h2 align = "center"> :open_book: Table Of Contents </h2>

- [Prerequisites](#prerequisites) <br/>
- [Setup](#setup) <br/>
- [FAQ](#faq) <br/>
- [Tech Stack](#tech-stack) <br/>
- [Contributors](#contributors) <br/>

<h2 align="center" id = "prerequisites"> :axe:	Prerequisites</h2>

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
    e. You should see your URA API key there which is required for PropertyIQ. **Do not lose this key!** <br/>
* Google Maps API
  + https://www.youtube.com/watch?v=OGTG1l7yin4 (Step-by-step tutorial on how to acquire API Key) <br/>
    a. Go to https://console.cloud.google.com. <br/>
    b. Create a new Project. Name it however you want. <br/>
    c. Open the sidebar, click **API & Services**, then click on **Library**. <br/>
    d. Search for or click on **Maps Javascript API**. <br/>
    e. Enable it. <br/>
    f. Open the sidebar again, click **API & Services**, then click on **Credentials**. <br/>
    g. Click on Create Credentials, then click on API Key. <br/>
    h. And you're done, that's the API key required for our Google Maps Services for PropertyIQ. **Do not lose this key!** <br/>
    
>Prerequsite (Others)
* Gmail App Password
  + https://myaccount.google.com/ <br/>
    a. Search for App Password on the search bar (Assumed that you have a valid gmail account.) <br/>
    b. Select the option App Passwords with the subscript security. <br/> 
    ![Picture1](https://user-images.githubusercontent.com/95838788/230461754-2f8d8904-8df0-4113-b295-534fe0b7f163.png) <br/>
    c. **If this option does not appear, ensure that you have set up your 2FA prior to this. Gmail only supports this if 2FA has been implemented.** <br/>
    d. Else, select App as mail. <br/>
    e. Select device as either Mac/Windows Computer depending on the OS you are using. <br/>
    f. And you're done, that's the Gmail App Password required to send emails to users whenever PropertyIQ has any new listings. **Do not lose this password!** <br/>
* Clone this project

<h2 align="center" id = "setup"> :hammer_and_wrench:	Setup</h2>

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

> For Mac Users:
```
1. If you face any error installing the library psycopg2, please delete the line 'psycopg2==2.9.5' from the requirements.txt.
2. Only install psycopg2-binary==2.9.5 by running 'pip install psycopg2-binary==2.9.5' in the terminal.
3. That should solve any errors you face.
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
<strong>Ensure that the names match exactly. e.g. 'POSTGRE_USER' must be stored exactly as POSTGRE_USER in the .env file without any typos. Also, the <> signs are not required. There are there only for illustrative purposes. e.g. POSTGRE_USER = 'postgres' is correct without the <> signs at the ends. Note: The default POSTGRE_USER if not set above is automatically 'postgres'. </strong>
  
```
POSTGRE_USER = '<YOUR POSTGRESQL USER>'
POSTGRE_PASSWORD = '<YOUR POSTGRESQL PASSWORD>'
```
6) Get URA API Key from URA Website & Add it to the .env file.
```
URA_API_KEY = '<YOUR URA API KEY>'
```
7) Get Google Maps API Key & Add it to the .env file.
```
GOOGLE_MAPS_KEY = '<YOUR GOOGLE MAPS KEY>'
```
8) Get Gmail App Password & add it to the .env file.
```
GMAIL_EMAIL = '<YOUR EMAIL>' 
GMAIL_APP_PASSWORD = '<ENTER 16 DIGIT CODE HERE>'
```
The final .env file should look like this: <br/>
![env](https://user-images.githubusercontent.com/95838788/230461214-3b7bdff1-9b87-4159-8c61-f064d0f7f8a5.png)

<h2 align="center"> :runner: Starting the server</h2>

> Create superuser
```
python manage.py createsuperuser
```
  
Example Super User Account:
```
Username: propertyIQ
Email: <Your valid gmail email which should be the same as the Gmail Email you used to get the Gmail App Password>
Password: sc2006_1234
```
**Note:** It is normal if you can't see the password appearing on the screen even when you are typing something. This is for **security reasons!**


> Setting up and running the server
```
python manage.py migrate
python manage.py runserver
```
**Note: During migrations, you should see all green for the migrations!**

> First-time setup

Within the website, head over to the login page and login as the superuser. Head to the dashboard and **click update property list.**
#### NOTE: THIS WILL TAKE A WHILE ~2-3MIN ON A FAST INTERNET CONNECTION and also depends on the number of users currently registered since it needs to send emails to each and every user everytime there is a new update for new properties.

Every registered user will receive an email like this by the website's superuser whenever the properties are updated:
![emailUpdate](https://user-images.githubusercontent.com/95838788/230758527-8b847c5c-28ed-4dc1-b304-3c9524cb3844.png)

After this, you should see some listings on the home page and the 'featured listings page'.
![updatedatabase](https://user-images.githubusercontent.com/95838788/230758071-dac450b4-6f22-4272-99cd-fc7ac440bc34.png)

> pgAdmin

The purpose of installing pgAdmin is to view the data stored in the database using a graphical interface which is much more user-friendly. **Note that pgAdmin is more for developers who want to implement some changes or see how the data is being stored. For the front-end users, pgAdmin may not be necessary.** <br/>

In pgAdmin , enter the same **password** from **PostgreSQL** and you should then see the following.
Click on server database icon top left and add the password which you entered in psql.

Then, click on 'Databases' and choose the database to examine. It should be 'propertyiq' if your setup process has been the same as proposed above. <br/>
![databasepgAdmin](https://user-images.githubusercontent.com/101249007/229968141-222fc0a4-7205-4476-ba8d-9bc805340bf8.png)

Then, click on 'Schemas'. <br/>
![table](https://user-images.githubusercontent.com/101249007/229976693-f58bd915-b883-4978-bdee-4881f6c2d63f.png)

Then, click on 'Tables'. Thereafter, choose the table you want to examine. <br/>
![image](https://user-images.githubusercontent.com/95838788/230758667-13a068c8-d35c-4b7f-9193-9e8011114178.png)

For example, if you want to examine the property tables, simply right click 'property_property' and click 'View/Edit Data'  and select 'All Rows'.  <br/>
![image](https://user-images.githubusercontent.com/95838788/230758694-a38aa2ae-1a70-459a-a50c-0363138ccd6c.png)

This will display all of the property listing in the database to you as shown below: <br/>
![image](https://user-images.githubusercontent.com/95838788/230758726-2974f99a-d93f-4801-928a-531de13f840f.png)

<h1 align="center"> :confetti_ball: Congratulations! :confetti_ball:</h1>

### Now, you can explore PropertyIQ locally on your machine!


<h2 align="center" id = "faq" > :question: FAQ</h2>

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

> <strong>6. I'm facing errors installing psycopg2 in the initial set up!! I'm a Mac User. </strong>
```
1. If you face any error installing the library psycopg2, please delete the line 'psycopg2==2.9.5' from the requirements.txt.
2. Only install psycopg2-binary==2.9.5. 
3. That should solve any errors you face.
```

<h2 align="center" id = "tech-stack"> 🛠 Tech Stack:</h2>

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

<h2 align="center" id = "contributors"> :family_man_man_boy_boy: Contributors:</h2>

- [Chong Wei Kang](https://github.com/weikangg): Frontend, Backend, SRS <br/>
- [Pugalia Aditya Kumar](https://github.com/AdityaPugalia): Frontend, Backend, SRS <br/> 
- [Andrada Angel John Bernardino](https://github.com/AAJB13): Diagrams, Testing, SRS, Final Powerpoint <br/>
- [Don Lim Zhan Chen](https://github.com/TheGreatReee): Diagrams, Testing, SRS, Final Powerpoint <br/>
- [Nicholas Lim Jan Tuck](https://github.com/NicholasLimJT): Diagrams, Testing, SRS, Final Powerpoint <br/>
  
| Profile                                                                                                                            | Name             | School                                 | Responsibilities
| ---------------------------------------------------------------------------------------------------------------------------------- | ---------------- | -------------------------------------- | ------------------------------ |
| <a href='https://github.com/weikangg' title='weikangg'> <img src='https://github.com/weikangg.png' height='50' width='50'/></a>       | Wei Kang           | Nanyang Technological University (NTU) | Frontend, Backend, SRS |
| <a href='https://github.com/AdityaPugalia' title='AdityaPugalia'> <img src='https://github.com/AdityaPugalia.png' height='50' width='50'/></a>    | Aditya Pugalia | Nanyang Technological University (NTU) | Frontend, Backend, SRS |
| <a href='https://github.com/AAJB13' title='AAJB13'> <img src='https://github.com/AAJB13.png' height='50' width='50'/></a> | John   | Nanyang Technological University (NTU) | Diagrams, Testing, SRS, Final Powerpoint |
| <a href='https://github.com/TheGreatReee' title='TheGreatReee'> <img src='https://github.com/TheGreatReee.png' height='50' width='50'/></a>       | John          | Nanyang Technological University (NTU) | Diagrams, Testing, SRS, Final Powerpoint |
| <a href='https://github.com/NicholasLimJT' title='NicholasLimJT'> <img src='https://github.com/NicholasLimJT.png' height='50' width='50'/></a>    | Nicholas             | Nanyang Technological University (NTU) | Diagrams, Testing, SRS, Final Powerpoint |

