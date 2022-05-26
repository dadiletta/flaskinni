    |--------------------------------------------------------------------------|
    |--------------------------Co/\/\p|_|T3R----$c13nc3------------------------|
    |--------------------------------------------------------------------------| 
    |     _________                    AAA                                     |
    |    mmmmmmmmmmmm   _____         AAAAA                      @LancerTechGA |
    |   mm    mm    mm  rrrrr        AA   AA                                   |
    |   mm    mm    mm  rr          AAAAAAAAA                                  |
    |   mm    mm    mm  rr   _._   AAA     AAA (and his much smarter students!)|
    |--------------------------------------------------------------------------|
    |--------------------------------------------------------------------------|

# Flaskinni

### [Documentation](https://gilmour.gitbook.io/compsci/web-development)
This is meant to be an open-source starter kit for Flask applications. Flask is an amazing framework because it's so simple and minimal. It's a great way learn web development as can see all the scaffolding that Rails and other frameworks build for you. However, assembling the many helpful Flask modules can be a real chore. Flaskinni helps by bundling these resources. It's intended to serve as a starting point for students who have been studying Flask and are now ready to start a larger project.

### Install

Please see the [guide](https://gilmour.gitbook.io/compsci/web-development) for detailed installation instructions. Or just wing it and figure it out. Look out for all the `settings.py` varibles you'll have to load in through a `.env` file.

#### Sample `.env` file
```
###################
##  FLASK 
###################
FLASK_ENV=development # change before publishing
FLASK_APP=flaskinni
DEBUG=True # change before publishing
SECRET_KEY='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # change before publishing

###################
##  FLASKINNI  
###################
STARTING_ADMIN_PASS = 'flaskinni'
ADMIN_EMAIL='flaskinni@gmail.com'
MAX_CONTENT_LENGTH = 2048 * 2048
UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']

###################
##  SQLAlchemy 
###################
# Windows: 127.0.0.1 
# Docker: db
DB_HOST=0.0.0.0 
DB_USERNAME='postgres' # change before publishing
DB_PASSWORD='postgres' # change before publishing
DB_PORT='5432'
DATABASE_NAME='db-flaskinni' # change before publishing
SQLALCHEMY_TRACK_MODIFICATIONS=False

###################
##  FLASK-SECURITY 
###################
SECURITY_REGISTERABLE=True
SECURITY_CONFIRMABLE=True
SECURITY_RECOVERABLE=True  
SECURITY_POST_LOGIN_VIEW='/'   # controls what page you see after login
SECURITY_EMAIL_SENDER='flaskinni@gmail.com'
SECURITY_PASSWORD_HASH ='pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # change before publishing

###################
##  FLASK-MAIL 
###################
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USE_TLS=False
MAIL_USERNAME='flaskinni@gmail.com'
MAIL_PASSWORD='xxxxxxxxxxx'
MAIL_DEFAULT_SENDER='flaskinni@gmail.com'

###################
##  JWT 
###################
PROPAGATE_EXCEPTIONS = True # change before publishing
JWT_BLOCKLIST_TOKEN_CHECKS = ['access', 'refresh']
```

### Credits

Thank you to the many contributors to this project. Together we're learning about full-stack development including an enthusasim for mandated attribution.


- [Bootstrap Template](https://startbootstrap.com/themes/sb-admin-2/)
- [Flask](https://flask.pocoo.org/)
- [Flask-Admin](https://flask-admin.readthedocs.io/en/latest/)
- [Flask-Security-Too](https://flask-security-too.readthedocs.io/en/stable/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Flask-Moment](https://github.com/miguelgrinberg/Flask-Moment)
