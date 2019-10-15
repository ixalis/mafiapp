# mafiapp
A web application to make running live-action mafia games easier. Currently intended for use alongside mafia.mit.edu.

## Installation
Runs with Python 2.7.15, and Django 1.5
To run, clone the directory, and run 'python manage.py syncdb'
Clone 'example_settings.py' to 'settings.py' and change appropriate settings for production.

## Game
To run a Vanilla mafia game, you can run 'i.py' to import preset abilities and items. 'i.py' also has methods to run example games for testing purposes 

Automated functions should be written in method.py according to the specifications there, and can be linked to items that can be generated using the admin console
