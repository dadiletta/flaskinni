    |--------------------------------------------------------------------------|
    |--------------------------Co/\/\p|_|T3R----$c13nc3------------------------|
    |--------------------------------------------------------------------------| 
    |     _________                    AAA                      @GilmourAcademy|
    |    mmmmmmmmmmmm   _____         AAAAA                    @AresDevelopment|
    |   mm    mm    mm  rrrrr        AA   AA                                   |
    |   mm    mm    mm  rr          AAAAAAAAA                                  |
    |   mm    mm    mm  rr   _._   AAA     AAA (and his much smarter students!)|
    |--------------------------------------------------------------------------|
    |--------------------------------------------------------------------------|
# Flaskinni
This is meant to be an open-source template for Flask applications. Flask is an amazing framework because it 's so simple and minimal. It's a great way learn web development as you have to build all the scaffolding that Rails and other frameworks build for you. However, assembling the many helpful Flask modules can be a real chore. Flaskinni helps by bundling many of these resources. It's intended to serve as a starting point for students who have been studying Flask and are now ready to start a larger project.
https://docs.google.com/document/d/1goCM1waUqJzR1s_0fq49jf3EEELUjyftqo3SXLQ0XPQ/

## Your Steps 
1. Clone the c9 workspace
2. Change flaskinni to your project name by right clicking on top folder and searching for flaskinni (also change the folder)
3. Work on your readme's description and start taking notes on the steps you take
4. Create a `private.py` file if you don't have one in your project folder
5. Follow along in the Web Dev Guide: https://docs.google.com/document/d/1goCM1waUqJzR1s_0fq49jf3EEELUjyftqo3SXLQ0XPQ/

### Flaskinni To-Do List
- Docker implementation (in progress... it's fun!)
- Blog
    - Add pagination to homepage blog listing
    - Search blog posts by tag using ajax
    - Search blog posts by author
    - Implement select2 on tags: https://select2.github.io/examples.html
- Add a my_account page
- Stylize
    - Cursor effect when hovering over logo
    - Favicon
    - Paralax effect
- Unit tests


#### Feature Ideas
- Create a color pallet JS object that stores students' colors and accents 
- SEO support like adding metadata fields to blog form
- Learn about Flask signals for real-time messaging 
- Better app factories including database drop & creation
- Implement Flask-Social
- Add example content that also doubles as instructional material
- Add a dynamic, unique ID to each main body container 

------------
## Learning Resources
Any programming job is a commitment to be constantly learning. Don't isolate yourself to one language or framework because it feels more comfortable. Accept that you will be forever learning new extensions and learn peace and patience with the process. 
- http://learnpythonthehardway.org/book/
- [Fromzero](https://www.udemy.com/python-flask-course/) course.

### Some of My Old Notes While Creating Flaskinni
1. Setup c9 and flask-security starter
    - [Installing Python 3.6](http://stackoverflow.com/a/43814732/2184623)
        - (`sudo apt-get install python3.6` wasn't buildin't binaries correctly)
    - `python3.6 -m venv /home/ubuntu/workspace/venv`
    - `source venv/bin/activate`
    - `git clone https://github.com/sasaporta/flask-security-admin-example.git`
    - pip install for days
    - Change configuration and launched app for the first time - example app works!
2. Modifying user registration 
    - Add additional forms to the register_user template
    - Wondering if I should combine render_field(s) from _macros and _formhelpers
    - Struggled with Flask-Social. Testing Google OAuth2 in c9 is a struggle. Putting on hold
3. Contact form
    - General site marketing content like homepage and contact falls under "blog"
    - Adding contact form to `/blog/forms.py`
    - Why doesn't my cPanel mailhost work? https://stackoverflow.com/questions/12145536/how-can-i-debug-what-is-causing-a-connection-refused-or-a-connection-time-out
    - Reluctantly resigned to Gmail for now
4. Unit Testing
    - Using the "with" command important: https://stackoverflow.com/questions/21506326/testing-flask-login-and-authentication
    - https://pythonhosted.org/Flask-Testing/
5. Blog
    - Added `|markdown|striptags` to remove markdown from the blog preview
    - Used `humanize.naturaltime(self.publish_date)`

#### Credits
- Example of combining Flask-Security and Flask-Admin by Steve Saporta  - April 15, 2014
- Minimal template: https://startbootstrap.com/template-overviews/clean-blog/

