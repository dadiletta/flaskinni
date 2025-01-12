"""
Blog Object Schema
====================
Blog posts, tags, and the association table between them with Supabase integration.
"""

from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from flask import url_for, current_app
import sqlalchemy as sa
from slugify import slugify
import humanize

from ..extensions import db

tags_posts = db.Table(
   'tags_posts',
   db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
   db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'))
)

class Post(db.Model):
   """Blog post model with tags and image upload."""
   __tablename__ = 'post'
   
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   title = db.Column(db.String(80), nullable=False)
   subtitle = db.Column(db.String(80))
   body = db.Column(db.Text, nullable=False)
   image = db.Column(db.String(125))
   slug = db.Column(db.String(125), unique=True)
   
   # Timestamps
   created_at = db.Column(db.DateTime(timezone=True), 
                         default=lambda: datetime.now(timezone.utc))
   updated_at = db.Column(db.DateTime(timezone=True),
                        onupdate=lambda: datetime.now(timezone.utc))
   published_at = db.Column(db.DateTime(timezone=True))
   
   # Status flags
   status = db.Column(db.String(20), default='draft')  # draft, published, archived
   
   # Relationships
   tags = db.relationship(
       'Tag',
       secondary=tags_posts,
       backref=db.backref('posts', lazy='dynamic')
   )

   def publish(self, supabase) -> 'Post':
       """Publish post."""
       now = datetime.now(timezone.utc)
       return self.update(
           supabase,
           status='published',
           published_at=now
       )

   def archive(self, supabase) -> 'Post':
       """Archive post."""
       return self.update(
           supabase,
           status='archived'
       )

   @property
   def img(self) -> Optional[str]:
       """Get post image URL."""
       if self.image:
           return url_for('static', filename=f"uploads/blog/{self.image}")
       return None

   @property
   def pubdate(self) -> str:
       """Get human-readable publish date."""
       return humanize.naturaltime(self.published_at or self.created_at)

   @property
   def reading_time(self) -> int:
       """Estimate reading time in minutes."""
       words_per_minute = 200
       word_count = len(self.body.split())
       return max(1, round(word_count / words_per_minute))

   def __repr__(self):
       return f'<Post {self.title}>'


class Tag(db.Model):
   """Tag model for categorizing blog posts."""
   __tablename__ = 'tag'
   
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(50), unique=True)
   description = db.Column(db.String(200))
   slug = db.Column(db.String(60), unique=True)
   created_at = db.Column(db.DateTime(timezone=True), 
                         default=lambda: datetime.now(timezone.utc))

   @classmethod
   def get_or_create(cls, name: str) -> 'Tag':
       """Get existing tag or create new one."""
       tag = cls.query.filter_by(name=name).first()
       if not tag:
           tag = cls(
               name=name,
               slug=slugify(name)
           )
           db.session.add(tag)
           db.session.commit()
       return tag

   def __repr__(self):
       return self.name