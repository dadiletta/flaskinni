"""
Base Database Schema
=====================
User model with Supabase integration for auth and data operations.
"""

from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from flask import url_for, current_app
from flask_login import UserMixin
import sqlalchemy as sa
from .. import db
import humanize

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model):
    """Role model for user permissions."""
    __tablename__ = 'role'
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


class User(db.Model, UserMixin):
    """
    User model that maps to both local database and Supabase auth.
    Handles synchronization between Flask-Login sessions and Supabase auth state.
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    supabase_uid = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True)
    first_name = db.Column(db.String(155))
    last_name = db.Column(db.String(155))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    about = db.Column(db.Text)
    image = db.Column(db.String(125))
    
    # Toggles
    active = db.Column(db.Boolean(), default=True)
    public_profile = db.Column(db.Boolean(), default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), 
                          default=lambda: datetime.now(timezone.utc))
    last_seen = db.Column(db.DateTime(timezone=True))

    # Relationships
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    @classmethod
    def create(cls, supabase, email: str, password: str, **kwargs) -> 'User':
        """Create new user in both Supabase and local DB."""
        try:
            # Create user in Supabase
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            # Create local user
            user = cls(
                supabase_uid=auth_response.user.id,
                email=email,
                username=kwargs.get('username', email.split('@')[0]),
                **kwargs
            )
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"User creation failed: {str(e)}")
            raise

    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        """Fetch user by email."""
        return db.session.scalar(
            sa.select(User).where(User.email == email)
        )

    @classmethod
    def get_by_supabase_uid(cls, supabase_uid: str) -> Optional['User']:
        """Fetch user by Supabase UID."""
        return db.session.scalar(
            sa.select(User).where(User.supabase_uid == supabase_uid)
        )

    @classmethod
    def sync_from_supabase(cls, supabase, user_data: Dict[str, Any]) -> 'User':
        """Sync user data from Supabase to local DB."""
        user = cls.get_by_supabase_uid(user_data['id'])
        if not user:
            user = cls(
                supabase_uid=user_data['id'],
                email=user_data['email'],
                username=user_data.get('user_metadata', {}).get('username'),
                first_name=user_data.get('user_metadata', {}).get('first_name'),
                last_name=user_data.get('user_metadata', {}).get('last_name')
            )
            db.session.add(user)
        db.session.commit()
        return user

    def update(self, supabase, **kwargs) -> 'User':
        """Update user in both Supabase and local DB."""
        try:
            # Update Supabase user metadata
            supabase.auth.update_user({
                "data": {
                    "first_name": kwargs.get('first_name', self.first_name),
                    "last_name": kwargs.get('last_name', self.last_name),
                    "username": kwargs.get('username', self.username)
                }
            })
            
            # Update local user
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"User update failed: {str(e)}")
            raise

    def delete(self, supabase) -> bool:
        """Delete user from both Supabase and local DB."""
        try:
            supabase.auth.admin.delete_user(self.supabase_uid)
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"User deletion failed: {str(e)}")
            raise

    @property
    def img(self) -> Optional[str]:
        """Get user's profile image URL."""
        if self.image:
            return url_for('static', filename=f"uploads/{self.id}/{self.image}")
        return None

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username or self.email

    def has_role(self, role_name: str) -> bool:
        """Check if user has specific role."""
        return any(role.name == role_name for role in self.roles)

    def __repr__(self):
        return f'<User {self.email}>'

class Buzz(db.Model):
    """
    Event logging system for admin monitoring.
    Tracks significant actions and changes within the application.
    """
    __tablename__ = 'buzz'

    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    
    # Properties
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    event_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True), 
                          default=lambda: datetime.now(timezone.utc))
    
    # Additional metadata stored as JSON
    metadata = db.Column(db.JSON)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('buzzes', lazy='dynamic'))
    post = db.relationship('Post', backref=db.backref('buzzes', lazy='dynamic'))

    @classmethod
    def create(cls, supabase, title: str, body: str, event_type: str, 
               user_id: Optional[int] = None, post_id: Optional[int] = None, 
               metadata: Optional[Dict] = None) -> 'Buzz':
        """Create new event log in both Supabase and local DB."""
        try:
            # Create in Supabase
            buzz_data = {
                "title": title,
                "body": body,
                "event_type": event_type,
                "user_id": user_id,
                "post_id": post_id,
                "metadata": metadata or {},
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            supabase.table("buzzes").insert(buzz_data).execute()
            
            # Create local record
            buzz = cls(
                title=title,
                body=body,
                event_type=event_type,
                user_id=user_id,
                post_id=post_id,
                metadata=metadata
            )
            db.session.add(buzz)
            db.session.commit()
            
            return buzz
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Buzz creation failed: {str(e)}")
            raise

    @classmethod
    def get_recent(cls, limit: int = 50) -> List['Buzz']:
        """Get recent events with pagination."""
        return db.session.scalars(
            sa.select(Buzz)
            .order_by(Buzz.created_at.desc())
            .limit(limit)
        ).all()

    @classmethod
    def get_by_type(cls, event_type: str, limit: int = 50) -> List['Buzz']:
        """Get events of a specific type."""
        return db.session.scalars(
            sa.select(Buzz)
            .where(Buzz.event_type == event_type)
            .order_by(Buzz.created_at.desc())
            .limit(limit)
        ).all()

    @classmethod
    def get_user_events(cls, user_id: int, limit: int = 50) -> List['Buzz']:
        """Get events related to a specific user."""
        return db.session.scalars(
            sa.select(Buzz)
            .where(Buzz.user_id == user_id)
            .order_by(Buzz.created_at.desc())
            .limit(limit)
        ).all()

    def generate_link(self) -> str:
        """Generate relevant link based on event type and associated objects."""
        if self.event_type == 'user_event' and self.user_id:
            return url_for('base.profile', user_id=self.user_id)
        elif self.event_type == 'post_event' and self.post_id:
            return url_for('base.post', post_id=self.post_id)
        return "#"

    @property
    def when(self) -> str:
        """Get human-readable timestamp."""
        return humanize.naturaltime(self.created_at)

    @property
    def icon(self) -> str:
        """Get appropriate icon based on event type."""
        icons = {
            'user_signup': 'user-plus',
            'user_login': 'log-in',
            'post_created': 'file-text',
            'post_updated': 'edit',
            'post_deleted': 'trash-2',
            'error': 'alert-triangle',
            'warning': 'alert-circle',
            'info': 'info'
        }
        return icons.get(self.event_type, 'bell')

    def __repr__(self):
        return f'<Buzz {self.event_type}: {self.title}>'