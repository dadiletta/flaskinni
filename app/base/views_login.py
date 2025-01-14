# app/base/views_login.py
"""
Authentication Routes
===================
Complete authentication system integrating Supabase auth with Flask-Login.
Includes all necessary routes for user authentication flows.
"""

from datetime import datetime, timezone
from flask import (
    render_template, redirect, flash, url_for, 
    session, request, current_app
    )
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse as url_parse

from . import base_blueprint as app
from .. import db
from .forms import (
    LoginForm, RegistrationForm, SubmitHelpForm,
    ResetPasswordForm, ChangePasswordForm
    )
from ..models import User, Buzz

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login with Supabase authentication."""
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # Authenticate with Supabase
            auth_response = current_app.supabase.auth.sign_in_with_password({
                "email": form.email.data,
                "password": form.password.data
            })
            
            # Get or create local user
            user = User.query.get(auth_response.user.id)
            if not user:
                user = User(
                    id=auth_response.user.id,
                    email=form.email.data,
                    created_at=datetime.now(timezone.utc)
                )
                db.session.add(user)
            
            # Update last login time
            user.last_seen = datetime.now(timezone.utc)
            db.session.commit()
            
            # Log the login event
            buzz = Buzz(
                user_id=user.id,
                event_type='user_login',
                title=f"User login: {user.email}",
                body=f"User logged in from {request.remote_addr}"
            )
            db.session.add(buzz)
            db.session.commit()
            
            # Set up session
            login_user(user, remember=form.remember_me.data)
            session['supabase_access_token'] = auth_response.session.access_token
            
            # Redirect to requested page or default
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('base.index')
            return redirect(next_page)
            
        except Exception as e:
            current_app.logger.error(f"Login error: {e}")
            flash('Invalid email or password', 'danger')
            
    return render_template('base/login/login_user.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    """Handle user logout from both Supabase and Flask-Login."""
    try:
        if 'supabase_access_token' in session:
            current_app.supabase.auth.sign_out()
            session.pop('supabase_access_token')
    except Exception as e:
        current_app.logger.error(f"Supabase logout error: {e}")
    
    if current_user.is_authenticated:
        buzz = Buzz(
            user_id=current_user.id,
            event_type='user_logout',
            title=f"User logout: {current_user.email}",
            body=f"User logged out from {request.remote_addr}"
        )
        db.session.add(buzz)
        db.session.commit()
    
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('base.login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle new user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Create user in Supabase
            auth_response = current_app.supabase.auth.sign_up({
                "email": form.email.data,
                "password": form.password.data
            })
            
            # Create local user
            user = User(
                id=auth_response.user.id,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(user)
            
            # Log the registration
            buzz = Buzz(
                user_id=user.id,
                event_type='user_signup',
                title=f"New user registration: {user.email}",
                body=f"User registered from {request.remote_addr}"
            )
            db.session.add(buzz)
            db.session.commit()
            
            flash('Registration successful! Please check your email to verify your account.', 'success')
            return redirect(url_for('base.login'))
            
        except Exception as e:
            current_app.logger.error(f"Registration failed: {e}")
            flash('Registration failed. This email may already be registered.', 'danger')
            db.session.rollback()
            
    return render_template('base/login/register_user.html', title='Register', form=form)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle password reset requests."""
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))
        
    form = SubmitHelpForm()
    if form.validate_on_submit():
        try:
            # Request password reset through Supabase
            current_app.supabase.auth.reset_password_email(form.email.data)
            flash('Check your email for password reset instructions.', 'info')
            return redirect(url_for('base.login'))
            
        except Exception as e:
            current_app.logger.error(f"Password reset request failed: {e}")
            flash('Error sending reset instructions. Please try again.', 'danger')
            
    return render_template('base/login/forgot_password.html', 
                         title='Reset Password', form=form)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset with token."""
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))
        
    form = ResetPasswordForm()
    if form.validate_on_submit():
        try:
            # Verify token and update password in Supabase
            current_app.supabase.auth.verify_password_reset(
                token, 
                form.password.data
            )
            
            flash('Your password has been reset.', 'success')
            return redirect(url_for('base.login'))
            
        except Exception as e:
            current_app.logger.error(f"Password reset failed: {e}")
            flash('Invalid or expired reset link. Please try again.', 'danger')
            
    return render_template('base/login/reset_password.html', 
                         title='Reset Password', form=form)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Handle password changes for logged-in users."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        try:
            # First verify current password
            current_app.supabase.auth.sign_in_with_password({
                "email": current_user.email,
                "password": form.password.data
            })
            
            # Update password in Supabase
            current_app.supabase.auth.update_user({
                "password": form.new_password.data
            })
            
            # Log the change
            buzz = Buzz(
                user_id=current_user.id,
                event_type='password_change',
                title=f"Password changed: {current_user.email}",
                body=f"Password changed from {request.remote_addr}"
            )
            db.session.add(buzz)
            db.session.commit()
            
            flash('Your password has been updated.', 'success')
            return redirect(url_for('base.settings'))
            
        except Exception as e:
            current_app.logger.error(f"Password change failed: {e}")
            flash('Current password is incorrect or new password is invalid.', 'danger')
            
    return render_template('base/login/change_password.html', 
                         title='Change Password', form=form)

@app.route('/resend-confirmation', methods=['GET', 'POST'])
def resend_confirmation():
    """Resend email confirmation link."""
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))
        
    form = SubmitHelpForm()
    if form.validate_on_submit():
        try:
            # Resend verification email through Supabase
            current_app.supabase.auth.resend_confirmation_email({
                "email": form.email.data
            })
            
            flash('Confirmation instructions have been sent to your email.', 'info')
            return redirect(url_for('base.login'))
            
        except Exception as e:
            current_app.logger.error(f"Resend confirmation failed: {e}")
            flash('Error sending confirmation email. Please try again.', 'danger')
            
    return render_template('base/login/send_confirmation.html', 
                         title='Resend Confirmation', form=form)