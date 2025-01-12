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
   """Blog post model with Supabase sync capabilities."""
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

   @classmethod
   def create(cls, supabase, user_id: int, title: str, body: str, **kwargs) -> 'Post':
       """Create new post in both Supabase and local DB."""
       try:
           # Generate slug
           base_slug = slugify(title)
           slug = base_slug
           counter = 1
           while db.session.scalar(sa.select(Post).where(Post.slug == slug)):
               slug = f"{base_slug}-{counter}"
               counter += 1

           # Create in Supabase
           post_data = {
               "user_id": user_id,
               "title": title,
               "body": body,
               "slug": slug,
               "status": kwargs.get('status', 'draft'),
               "created_at": datetime.now(timezone.utc).isoformat(),
               **kwargs
           }
           
           supabase.table("posts").insert(post_data).execute()
           
           # Create local post
           post = cls(
               user_id=user_id,
               title=title,
               body=body,
               slug=slug,
               subtitle=kwargs.get('subtitle'),
               image=kwargs.get('image'),
               status=kwargs.get('status', 'draft'),
               published_at=kwargs.get('published_at')
           )
           
           # Handle tags
           if 'tags' in kwargs:
               post.tags = [Tag.get_or_create(name) for name in kwargs['tags']]
           
           db.session.add(post)
           db.session.commit()
           
           return post
       except Exception as e:
           db.session.rollback()
           current_app.logger.error(f"Post creation failed: {str(e)}")
           raise

   def update(self, supabase, **kwargs) -> 'Post':
       """Update post in both Supabase and local DB."""
       try:
           # Update Supabase
           update_data = {k: v for k, v in kwargs.items() if hasattr(self, k)}
           supabase.table("posts").update(update_data).eq("id", self.id).execute()
           
           # Update local post
           for key, value in kwargs.items():
               if hasattr(self, key):
                   if key == 'tags':
                       self.tags = [Tag.get_or_create(name) for name in value]
                   else:
                       setattr(self, key, value)
           
           db.session.commit()
           return self
       except Exception as e:
           db.session.rollback()
           current_app.logger.error(f"Post update failed: {str(e)}")
           raise

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

   def delete(self, supabase) -> bool:
       """Delete post from both Supabase and local DB."""
       try:
           supabase.table("posts").delete().eq("id", self.id).execute()
           db.session.delete(self)
           db.session.commit()
           return True
       except Exception as e:
           db.session.rollback()
           current_app.logger.error(f"Post deletion failed: {str(e)}")
           raise

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

   @classmethod
   def sync_from_supabase(cls, supabase) -> List['Tag']:
       """Sync all tags from Supabase."""
       try:
           response = supabase.table("tags").select("*").execute()
           for tag_data in response.data:
               tag = cls.query.filter_by(name=tag_data['name']).first()
               if not tag:
                   tag = cls(
                       name=tag_data['name'],
                       slug=tag_data['slug'],
                       description=tag_data.get('description')
                   )
                   db.session.add(tag)
           db.session.commit()
           return cls.query.all()
       except Exception as e:
           db.session.rollback()
           current_app.logger.error(f"Tag sync failed: {str(e)}")
           raise

   def __repr__(self):
       return self.name