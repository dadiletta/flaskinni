from extensions import db, uploaded_images
from datetime import datetime
import humanize

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
    publish_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)
    # tags have been disabled
    tags = db.relationship(
        'Tag',
        secondary=tags_posts,
        backref=db.backref('posts', lazy='dynamic')
    )

    # get the whole image path
    @property
    def imgsrc(self):
        if self.image:
            return uploaded_images.url(self.image)
        else:
            return None
    
    # return the date in readable English    
    @property
    def pubdate(self):
        return humanize.naturaltime(self.publish_date)

    def __init__(self, user, title, subtitle, body, slug, image=None, publish_date=None, live=True):
            self.user_id = user.id
            self.title = title
            self.subtitle = subtitle
            self.body = body
            self.image = image
            self.slug = slug
            if publish_date is None:
                self.publish_date = datetime.utcnow()
            self.live = live

    def __repr__(self):
        return '<Post %r>' % self.title


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name, user_id=None):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return self.name