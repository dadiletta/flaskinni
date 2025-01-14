"""
Base Routes
============
The basic routes at the core of the app, including: 
 - Homepage 
 - Settings page
 - Profile page
 - Blog pages
"""

# library imports
from flask import render_template, redirect, flash, url_for, session, request, current_app, send_from_directory, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from flask_mail import Message
from slugify import slugify
from jinja2 import TemplateNotFound
import os, imghdr

# our objects
from . import base_blueprint as app # renamed to "app" so the blueprint layer fades to the background
from .. import db, mail, comms
from .forms import PostForm, ContactForm, SettingsForm, BuzzForm
from .decorators import roles_required
from ..models import Post, Tag, User, Buzz


@app.route('/')
@app.route('/index')
def index():
    """ Renders and returns the home page """
    data = {} 
    data['posts'] = Post.query.order_by(Post.published_at.desc()).all()
    return render_template('base/index.html', data=data)

@app.route('/settings', methods=('GET', 'POST'))
@app.route('/settings.html', methods=('GET', 'POST'))
@login_required
def settings():
    form = SettingsForm(obj=current_user)
    if form.validate_on_submit():
        # check out this cool new Python ternary operator: https://book.pythontips.com/en/latest/ternary_operators.html
        original_image = None if not current_user.image else current_user.image        
        form.populate_obj(current_user)  # this only works if the form property is the same name as the User property 
        current_user.image = original_image # avoid erasing any image properties just yet
        if form.image.has_file():
            image = request.files.get('image')
            filename = secure_filename(image.filename)
            try:
                # https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
                path = f"{current_app.root_path}/static/uploads/{current_user.id}" # notice how I pass the user ID? That's cause we need the right folder
                if not os.path.exists(path):
                    os.mkdir(path)
                if filename != '':
                    file_ext = os.path.splitext(filename)[1]
                    if file_ext not in ['.jpg', '.png', '.gif'] or \
                            file_ext != validate_image(image.stream):
                        abort(400)
                image.save(os.path.join(f"{path}/", filename))
                current_user.image = str(filename)
                # delete the previous image if there was one
                try:                        
                    if original_image:
                        old_image_path = f"{current_app.root_path}/static/uploads/{current_user.id}/{original_image}"
                        os.remove(old_image_path)
                except Exception as e:
                    flash(f"Failed to delete previous image: {e}", 'danger')
            except Exception as e:
                flash(f"The image was not uploaded: {e}", 'danger')
        db.session.add(current_user)
        db.session.commit()
        flash("User updated", "success")
    return render_template('base/settings.html', form=form)

@app.route('/user/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    if current_user == user or user.public_profile:
        return render_template('base/profile.html', user=user)
    else:
        flash("UNAUTHORIZED ACCESS", "danger")
        return redirect(url_for('base.index'))
  
@app.route('/contact', methods=('GET', 'POST'))
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # send email
        msg = Message("Message from your visitor" + form.name.data,
                          sender='noreply@flaskinni-dadiletta.c9users.io',
                          recipients=[app.config['ADMIN_EMAIL']])
        msg.body = """
        From: %s <%s>,
        %s
        """ % (form.name.data, form.email.data, form.message.data)
        with app.app_context():
            mail.send(msg)
        flash("Message sent", 'success')
        return redirect(url_for('index'))
    return render_template('base/contact.html', form=form)


@app.route('/admin', methods=('GET', 'POST'))
@roles_required('admin')
def admin():
    data = {}
    return render_template('base/admin.html', data=data)   

###################
####  POST
###################
@app.route('/blog/new', methods=('GET', 'POST'))
@login_required
@roles_required('admin')
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        image = request.files.get('image')
        filename = secure_filename(image.filename)
        try:
            # https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
            path = f"{current_app.root_path}/static/uploads/blog" 
            if not os.path.exists(path):
                os.mkdir(path)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in ['.jpg', '.png', '.gif'] or \
                        file_ext != validate_image(image.stream):
                    abort(400)
            # TODO: check if file already exists with that name
            image.save(os.path.join(f"{path}/", filename))
            current_user.image = str(filename)
        except Exception as e:
            flash(f"The image was not uploaded: {e}", 'danger')
        # tags have been disabled
        if form.new_tag.data:
            new_tag = Tag(form.new_tag.data)
            db.session.add(new_tag)
            db.session.flush()
            tag = new_tag
        else:
            tag = form.tag.data
        title = form.title.data
        subtitle = form.subtitle.data
        body = form.body.data
        slug = slugify(title)
        post = Post(user_id=current_user.id, title=title, subtitle=subtitle, body=body, slug=slug, image=filename)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('base.read', slug=slug))
    return render_template('base/post.html', form=form, action="new")
    
@app.route('/article/<slug>')
def read(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('base/article.html', post=post)
    
@app.route('/blog/edit/<int:post_id>', methods=('GET', 'POST'))
@roles_required('admin')
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm(obj=post)

    if form.validate_on_submit():
        original_image = None if not post.image else post.image    
        form.populate_obj(post)
        form.image = original_image # avoid accidentally overwriting image
        if form.image.has_file():
            image = request.files.get('image')
            filename = secure_filename(image.filename)
            try:
                # https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
                path = f"{current_app.root_path}/static/uploads/blog"
                if not os.path.exists(path):
                    os.mkdir(path)
                if filename != '':
                    file_ext = os.path.splitext(filename)[1]
                    if file_ext not in ['.jpg', '.png', '.gif'] or \
                            file_ext != validate_image(image.stream):
                        abort(400)
                image.save(os.path.join(f"{path}/", filename))
                post.image = str(filename)
                # delete the previous image if there was one
                try:                        
                    if original_image:
                        old_image_path = f"{current_app.root_path}/static/uploads/blog/{original_image}"
                        os.remove(old_image_path)
                except Exception as e:
                    flash(f"Failed to delete previous image: {e}", 'danger')
            except Exception as e:
                flash(f"The image was not uploaded: {e}", 'danger')

        # TODO: restore tags
        if form.new_tag.data:
            new_tag = Tag(form.new_tag.data)
            db.session.add(new_tag)
            db.session.flush()
            post.tag = new_tag
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('base.read', slug=post.slug))
    return render_template('base/post.html', form=form, post=post, action="edit")

@app.route('/blog/delete/<int:post_id>')
@roles_required('admin')
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.live = False
    db.session.commit()
    flash("Article deleted", 'success')
    return redirect(url_for('base.index'))

#################
## HELPER METHODS
#################
@app.route('/view/<template>')
def route_template(template):
    """
    This is a pretty boss way to flexibly render any simple HTML file
    https://github.com/app-generator/boilerplate-code-flask-dashboard/blob/master/app/home/routes.py
    """
    try:
        if not template.endswith( '.html' ):
            template += '.html'

        if 'reset_instructions' in template:
            return render_template( f"base/email/{template}" )
        return render_template( f"base/{template}" )

    except TemplateNotFound:
        return render_template('base/404.html'), 404
    
    except Exception as e:
        current_app.logger.error(f'Failed to render template: {e}')
        return render_template('base/500.html'), 500

@app.route('/files/<int:user_id>/<path:filename>')
def uploaded_files(user_id, filename):
    """Function to serve up files"""
    path = current_app.config['UPLOADED_IMAGES_DEST'] + f"/{user_id}" # USER-BASED FOLDER SYSTEM so we can delete contents based on user
    return send_from_directory(path, filename)

def validate_image(stream):
    """ Checks image validity using Python's imghdr """
    # https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        flash("Error validating image.", "danger")
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

# TODO: move this to a CDN service like Cloudinary
def avatar_upload(user, file, **kwargs):
    """upload's a file to a user's folder"""
    path = f"{current_app.root_path}/static/uploads/avatars/{ current_user.id }" # notice how I pass the user ID? That's cause we need the right folder
    if not os.path.exists(path):
        os.mkdir(path)
    file.save(os.path.join(f"{path}/", file.filename))
    return url_for('static', filename=f"uploads/avatars/{user.id}/{file.filename}") 

