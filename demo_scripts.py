from flask_script import Command
from user.models import *
from inni.models import *
from extensions import db
from datetime import datetime as dt
from slugify import slugify

class BlogDemo(Command):
    """
    Populates the database with example blog data
    """

    def run(self):
        
        user = User.query.first() # this assumes you already have a user in the database
        title = "For He is an Englishman"
        subtitle = "Gilbert and Sullivan"
        slug = slugify(title)
        blog = "I am the very model of a modern major general. I know the kings of England and I quote the fights historical."
        image = None
        p = Post(user, title, subtitle, blog, slug, image=image, publish_date=dt.utcnow())
        db.session.add(p)
        db.session.commit()