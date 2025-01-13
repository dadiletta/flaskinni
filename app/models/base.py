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
    db.Column('user_id', db.UUID(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model):
    """Role model for user permissions."""
    __tablename__ = 'role'
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    @classmethod
    def get_or_create(cls, name, description=None):
        """
        Get an existing role or create it if it doesn't exist.
        
        Args:
            name (str): The name of the role
            description (str, optional): Description of the role
        
        Returns:
            tuple: (role, created) where role is the Role instance and 
                  created is a boolean indicating if a new role was created
        """
        role = cls.query.filter_by(name=name).first()
        if role is None:
            role = cls(name=name, description=description)
            db.session.add(role)
            db.session.commit()
            return role, True
        return role, False

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

    id = db.Column(db.UUID, primary_key=True)  # This matches Supabase's UUID
    email = db.Column(db.String(255), unique=True, nullable=False)
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
    posts = db.relationship('Post', backref='user', lazy='dynamic', 
                       primaryjoin="User.id == Post.user_id")
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        """Fetch user by email."""
        return db.session.scalar(
            sa.select(User).where(User.email == email)
        )

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
    user_id = db.Column(db.UUID(), db.ForeignKey('user.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    
    # Properties
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    event_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True), 
                          default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = db.relationship('User', backref=db.backref('buzzes', lazy='dynamic'))
    post = db.relationship('Post', backref=db.backref('buzzes', lazy='dynamic'))

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