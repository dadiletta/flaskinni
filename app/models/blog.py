"""
Blog Object Schema
====================
Blog posts, tags, and the association table between them. 
"""

from flask import url_for
from datetime import datetime
import humanize

from ..extensions import db

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
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(80))
    subtitle = db.Column(db.String(80))
    body = db.Column(db.Text) 
    image = db.Column(db.String(125))
    """The name of the file that will be placed in `static/uploads/blog/`"""
    slug = db.Column(db.String(125), unique=True)
    publish_date = db.Column(db.DateTime(), default=datetime.utcnow)
    live = db.Column(db.Boolean)
    tags = db.relationship(
        'Tag',
        secondary=tags_posts,
        backref=db.backref('posts', lazy='dynamic')
    )

    @property
    def img(self):
        """Builds the whole image's path

        Returns:
            str: The URL for the associated image.
        """
        if self.image:
            return url_for('static', filename=f"uploads/blog/{self.image}")
        else:
            return None
      
    @property
    def pubdate(self):
        """Return the date in readable English """
        return humanize.naturaltime(self.publish_date)

    def __repr__(self):
        if self.title:
            return f'<Post {self.title}>'
        else: return super().__repr__()


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return self.name