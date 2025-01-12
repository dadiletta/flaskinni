"""
Extensions Container
=====================
Instantiates and contains Flask extensions to avoid circular imports.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_principal import Principal
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from supabase import create_client, Client

# Database ORM
db = SQLAlchemy()
"""SQLAlchemy database connection"""

# User Session Management
login_manager = LoginManager()
"""Flask-Login session manager"""

# User Permissions
principal = Principal()
"""Flask-Principal permissions manager"""

# Database Migrations
migrate = Migrate()
"""Flask-Migrate's alembic tracker for database changes"""

# Date/Time Handling
moment = Moment()
"""Flask-Moment timezone and datetime humanizer"""

# Email
mail = Mail()
"""Flask-Mail SMTP mailer"""

# Supabase Client (initialized in factory)
supabase: Client = None
"""Supabase client instance"""

def init_supabase(url: str, key: str) -> None:
   """Initialize Supabase client globally."""
   global supabase
   supabase = create_client(url, key)