"""
Login Routes
============
Authentication routes integrating Supabase auth with Flask-Login session management.
Includes: 
 - Login
 - Logout
 - Register
 - Password Management
"""

from datetime import datetime, timezone
from flask import (
    render_template, redirect, flash, url_for, 
    session, request, current_app, jsonify
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse

from . import base_blueprint as app
from .. import db
from .forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, ChangePasswordForm
from ..models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
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
            
            # Get or create local user - using Supabase's UUID
            user = User.query.get(auth_response.user.id)
            if not user:
                user = User(
                    id=auth_response.user.id,  # Use Supabase's UUID directly
                    email=form.email.data,
                    created_at=datetime.now(timezone.utc)
                )
                db.session.add(user)
                db.session.commit()
            
            login_user(user)
            session['supabase_access_token'] = auth_response.session.access_token
            
            return redirect(url_for('base.index'))
            
        except Exception as e:
            flash('Invalid email or password', 'danger')

@app.route('/logout')
def logout():
    try:
        # Sign out from Supabase
        if 'supabase_access_token' in session:
            current_app.supabase.auth.sign_out()
            session.pop('supabase_access_token')
    except Exception as e:
        current_app.logger.error(f"Supabase logout error: {e}")
    
    logout_user()  # Flask-Login logout
    flash('You have been logged out.', 'info')
    return redirect(url_for('base.login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
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
                email=form.email.data,
                supabase_uid=auth_response.user.id,
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please check your email to verify your account.', 'success')
            return redirect(url_for('base.login'))
            
        except Exception as e:
            current_app.logger.error(f"Registration failed: {e}")
            flash('Registration failed. This email may already be registered.', 'danger')
            db.session.rollback()
            
    return render_template('security/register.html', title='Register', form=form)

@app.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))
        
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        try:
            # Use Supabase password reset
            current_app.supabase.auth.reset_password_email(form.email.data)
            flash('Check your email for password reset instructions.', 'info')
            return redirect(url_for('base.login'))
        except Exception as e:
            current_app.logger.error(f"Password reset request failed: {e}")
            flash('Error sending reset instructions. Please try again.', 'danger')
            
    return render_template('security/reset_password_request.html', 
                         title='Reset Password', form=form)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
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
            
    return render_template('security/reset_password.html', form=form)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        try:
            # Update password in Supabase
            current_app.supabase.auth.update_user(
                session['supabase_access_token'],
                {"password": form.password.data}
            )
            flash('Your password has been updated.', 'success')
            return redirect(url_for('base.settings'))
        except Exception as e:
            current_app.logger.error(f"Password change failed: {e}")
            flash('Failed to update password. Please try again.', 'danger')
            
    return render_template('security/change_password.html', form=form)