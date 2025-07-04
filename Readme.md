# INSTALLATION

# `WINDOWS`

Install Python if you dont have. Project uses `3.13.5` version

Install Git if you dont have. 

Clone Git repository

    git clone https://github.com/DowranRowshenow/SocialMediaApp/SocialMediaApp.git

Create virtual environment and activate

    py -m venv .venv
    .venv/Scripts/Activate

Get new `Secret key` from django

    py manage.py
    

Create `.env` and enter your keys

    SECRET_KEY=
    EMAIL_HOST=
    EMAIL_PASSWORD=
    EMAIL_PORT=587

Finally run project

    py manage.py makemigrations accounts
    py manage.py makemigrations rooms
    py manage.py makemigrations friends
    py manage.py makemigrations notifications
    py manage.py makemigrations main
    py manage.py makemigrations
    py manage.py migrate

    py manage.py collectstatic
    py manage.py compilemessages
    py manage.py runserver

Additionally create super user after `migrate`

    py manage.py createsuperuser
