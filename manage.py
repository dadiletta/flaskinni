'''
BEFORE THE APP STARTS

NginX runs on the server - virtual server hosted by digital ocean
Gunicorn serves as the an alternative gateway between server and app?
wsgi handles incoming requests instead of us using runserver 
this file launches our app (in development we can use runserver)

Digital Ocean --(hosts)--> NginX ---(gateway)--> wsgi --(requests)---> Flask app

'''
# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# This file is a flask-script, it gives controls and options as our app starts
from flask_script import Manager, Server
# flask migrate is a toolkit that helps us change the database without nuking it
from flask_migrate import MigrateCommand
# duh, this is the application framework. the big cheese
from flask import Flask
# this will load the __init__ file where all our goodies get launched
from flaskinni import app
from demo_scripts import BlogDemo

# create a manager object as imported from the flask_script module
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = os.getenv('IP', '0.0.0.0'),
    port = int(os.getenv('PORT', 5000)))
)

manager.add_command("blogdemo", BlogDemo()) 

if __name__ == "__main__":
    manager.run()
