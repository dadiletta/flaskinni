from .. import db
from flask import flash, url_for
from flask_admin.contrib import sqla
from flask_security import UserMixin, RoleMixin, current_user, utils
from wtforms import validators, StringField, PasswordField
from datetime import datetime
import humanize

####################
#####  BLOG  
####################
# Create a table to support a many-to-many relationship between Users and Roles
tags_posts = db.Table(
    'tags_posts',
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(80))
    subtitle = db.Column(db.String(80))
    body = db.Column(db.Text)
    image = db.Column(db.String(125))
    slug = db.Column(db.String(125), unique=True)
    publish_date = db.Column(db.DateTime(), default=datetime.utcnow)
    live = db.Column(db.Boolean)
    tags = db.relationship(
        'Tag',
        secondary=tags_posts,
        backref=db.backref('posts', lazy='dynamic')
    )

    # get the whole image path
    @property
    def img(self):
        if self.image:
            return url_for('static', filename=f"uploads/blog/{self.image}")
        else:
            return None
    
    # return the date in readable English    
    @property
    def pubdate(self):
        return humanize.naturaltime(self.publish_date)

    def __repr__(self):
        return '<Post %r>' % self.title


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return self.name