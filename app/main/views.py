# library imports
from flask import render_template, redirect, flash, url_for, session, request, current_app, send_from_directory
from flask_security import login_required, roles_required, current_user
from flask_uploads import UploadNotAllowed
from flask_mail import Message
from slugify import slugify
import os

# our objects
from . import main as app
from .. import db, uploaded_images, mail
from .forms import PostForm, ContactForm, SettingsForm
from ..models import Post, Tag, User

# Displays the home page.
@app.route('/')
@app.route('/index')
@app.route('/index.html')
# Users must be authenticated to view the home page, but they don't have to have any particular role.
# Flask-Security will display a login form if the user isn't already authenticated.
def index():
    posts = Post.query.order_by(Post.publish_date.desc())
    return render_template('main/index.html', posts=posts)

@app.route('/settings', methods=('GET', 'POST'))
@app.route('/settings.html', methods=('GET', 'POST'))
def settings():
    form = SettingsForm(obj=current_user)
    if form.validate_on_submit():
        # check out this cool new Python ternary operator: https://book.pythontips.com/en/latest/ternary_operators.html
        original_image = None if not current_user.image else current_user.image        
        form.populate_obj(current_user)  # this only works if the form property is the same name as the User property    
        current_user.image = original_image   
        if form.image.has_file() and form.image.data != original_image:
            # TODO: delete old image if a new one is added
            image = request.files.get('image')
            try:
                user_upload(current_user, image)
                current_user.image = str(image.filename)
                # delete the previous image if there was one
                try:                        
                    if original_image:
                        old_image_path = f"{current_app.config['UPLOADED_IMAGES_DEST']}/{ current_user.id }/{original_image}"
                        os.remove(old_image_path)
                except Exception as e:
                    flash(f"Failed to delete previous image: {e}", 'danger')
            except Exception as e:
                flash(f"The image was not uploaded: {e}", 'danger')
        else:
            flash(f"{form.image.has_file()}")
        db.session.add(current_user)
        db.session.commit()
        flash("User updated", "success")
    return render_template('main/settings.html', form=form)

@app.route('/user/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    if current_user == user or user.public_profile:
        return render_template('main/profile.html', user=user)
    else:
        flash("UNAUTHORIZED ACCESS", "danger")
        return redirect(url_for('main.index'))

@app.route('/components')
@app.route('/components/')
@app.route('/components.html')
def components():
    return render_template('main/components.html')
  
@app.route('/superadmin')
@roles_required('admin')
def superadmin():
    data = {}
    data['users'] = User.query.all()
    return render_template('main/superadmin.html', data=data)
  
@app.route('/blankpage')
def blank_page():
    return render_template('main/blank_page.html')

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
    return render_template('main/contact.html', form=form)

@app.route('/blog')
@app.route('/blog/')
def blog_index():
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc())
    return render_template('main/blog.html', posts=posts)

@app.route('/blog/new', methods=('GET', 'POST'))
@login_required
@roles_required('admin')
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        image = request.files.get('image')
        filename = None
        try:
            filename = uploaded_images.save(image)
        except:
            flash("The image was not uploaded", 'danger')
        '''
        # tags have been disabled
        if form.new_tag.data:
            new_tag = Tag(form.new_tag.data)
            db.session.add(new_tag)
            db.session.flush()
            tag = new_tag
        else:
            tag = form.tag.data
        '''
        title = form.title.data
        subtitle = form.subtitle.data
        body = form.body.data
        slug = slugify(title)
        post = Post(current_user, title, subtitle, body, slug, image=filename)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('read', slug=slug))
    return render_template('main/post.html', form=form, action="new")
    
@app.route('/article/<slug>')
def read(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('main/article.html', post=post)
    
@app.route('/blog/edit/<int:post_id>', methods=('GET', 'POST'))
@roles_required('admin')
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm(obj=post)
    filename = None
    if form.validate_on_submit():
        original_image = post.image
        form.populate_obj(post)
        if form.image.has_file():
            image = request.files.get('image')
            try:
                filename = uploaded_images.save(image)
            except:
                flash("The image was not uploaded")
            if filename:
                post.image = filename
        else:
            post.image = original_image
        '''
        if form.new_tag.data:
            new_tag = Tag(form.new_tag.data)
            db.session.add(new_tag)
            db.session.flush()
            post.tag = new_tag
        '''
        db.session.commit()
        return redirect(url_for('read', slug=post.slug))
    return render_template('main/post.html', form=form, post=post, action="edit")

@app.route('/blog/delete/<int:post_id>')
@roles_required('admin')
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.live = False
    db.session.commit()
    flash("Article deleted", 'success')
    return redirect(url_for('blog_index'))



#################
## HELPER METHODS

@app.route('/files/<int:user_id>/<path:filename>')
def uploaded_files(user_id, filename):
    """Function to serve up files"""
    path = current_app.config['UPLOADED_IMAGES_DEST'] + f"/{user_id}" # USER-BASED FOLDER SYSTEM so we can delete contents based on user
    return send_from_directory(path, filename)

def user_upload(user, file):
    """upload's a file to a user's folder"""
    path = f"{current_app.config['UPLOADED_IMAGES_DEST']}/{ current_user.id }" # notice how I pass the user ID? That's cause we need the right folder
    if not os.path.exists(path):
        os.mkdir(path)
    file.save(os.path.join(f"{current_app.config['UPLOADED_IMAGES_DEST']}/{ current_user.id }/", file.filename))
    return url_for('main.uploaded_files', user_id=user.id, filename=file.filename) 