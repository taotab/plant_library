from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import time
import logging
import sqlite3
import os
import re
from db.helpers import insert_suggestion, get_db_connection
print("👀 Current working dir:", os.getcwd())

# when you allow more users later, or faster uploads, or multiple users at once), uuid is better for more uniqueness
# to avoid same time collisions, and overwriting files... for now time() is enough


app = Flask(__name__)


# Set up logging to log messages to a file and console.
# I can see them in flask terminal, in log files,, better for debugging
logging.basicConfig(level=logging.DEBUG,  # Log everything DEBUG and above
                    # Format log entries
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()])

# Set the upload folder and allowed file extensions

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# If all are true, return true, else return false (readablitly improves)
def is_strong_password(password):

    if (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    ):
        return True
    else:
        return False

# Check if the file extension valid, is allowed


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/welcome')
def welcome_page():

    return render_template('welcome_page.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            app.logger.error("No file part in the request")
            flash('No file part')
            # reload the same page (instead of going elsewhere)
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            app.logger.warning("User did not select a file")
            return redirect(request.url)

         # Proceed with uploading the file
        app.logger.info(f"Uploading file: {file.filename}")
        # Your upload logic...

        if file and allowed_file(file.filename):
            # filename original name is saved "file.filename", and secure_filename
            # makes sure the filename is secure, and not malicious, keeps only safe chars like _ or .
            filename = secure_filename(file.filename)
            # to avoid overwriting files with the same name, we can add a timestamp
            unique_filename = f"{int(time.time())}_{filename}"
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], unique_filename))
            # Log the successful file upload
            app.logger.info(f"File uploaded successfully: {unique_filename}")

            flash('File uploaded successfully!')
            return redirect(request.url)
        else:
            # If the file is not allowed, show an error
            app.logger.warning(f"Invalid file type attempted: {file.filename}")
            flash('Invalid file type!')
            return redirect(request.url)

    return render_template('upload.html')


# redirect(url_for('upload'))


@app.route('/')
def index():
    if 'username' in session:   # check inside session dictionary, if there's 'username' data store
        logged_msg = f'You are logged in... {session["username"]}.'

        return render_template('index.html', logged_msg=logged_msg)
    else:
        # redirect to login page if not logged in
        return redirect(url_for('login'))

# Route for all pages instead of hardcoding : dynamic routing...


# Loop over all images in the static folder, and show them in the index.html page
@app.route('/index2')
def index2():
    image_folder = os.path.join('static', 'plants_img')
    # List all image filenames
    images = os.listdir(image_folder)
    images = [img for img in images if img.endswith(
        ('png', 'jpg', 'jpeg', 'gif', 'webp'))]

    return render_template('index2.html', images=images)


@app.route('/plants/<plant_name>')
def plant_page(plant_name):
    try:
        return render_template(f'{plant_name}.html')
    except:
        return render_template('404.html')


# Pending uploads dashboard page route

@app.route('/dashboard')
def dashboard():

    conn = get_db_connection()
    suggestions = conn.execute('SELECT * FROM suggestions').fetchall()
    conn.close()
    return render_template('dashboard.html', suggestions=suggestions)

#  Route for viewers suggestion plant box


@app.route('/suggestion', methods=['GET', 'POST'])
def suggestion():

    if request.method == 'POST':
        # Get form fields
        # look for max length characters, (already in html5 done, its on quick ui/ux)
        # check in backend more secure, can't bypass (but only works if submitted form, and need flash msg codes extra)
        # .strip() removes leading and trailing spaces
        plant_name = request.form['plant_name'].strip()
        description = request.form['description'].strip()
        location = request.form['location'].strip()
        plant_type = request.form['plant_type'].strip()
        uploader_name = request.form['uploader_name'].strip()

        if len(plant_name) > 100 or len(location) > 200 or len(uploader_name) > 80:
            app.logger.warning("Characters exceed the allowed length")
            flash("One or more fields exceed the allowed length.")
            return redirect(request.url)

        # Validate file
        # check if the post request has the file part
        if 'file' not in request.files:
            app.logger.error("No file part in the request")
            flash('No file part')
            # reload the same page (instead of going elsewhere)
            return redirect(request.url)

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            app.logger.warning("User did not select a file")
            return redirect(request.url)

         # Proceed with uploading the file
        app.logger.info(f"Uploading file: {file.filename}")
        # Your upload logic...

        if file and allowed_file(file.filename):
            # filename original name is saved "file.filename", and secure_filename
            # makes sure the filename is secure, and not malicious, keeps only safe chars like _ or .
            filename = secure_filename(file.filename)
            # to avoid overwriting files with the same name, we can add a timestamp
            unique_filename = f"{int(time.time())}_{filename}"

            try:
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], unique_filename))
            except Exception as e:
                app.logger.error(f"File save error: {e}")
                flash("Failed to save file. Please try again.")
                return redirect(request.url)

            # Log the successful file upload
            app.logger.info(f"File uploaded successfully: {unique_filename}")

            flash('Suggestion uploaded successfully!')

            # Replace with actual filename after file upload
            image_path = unique_filename

            # Insert into the database
            # Call the helper function to insert suggestion into DB
            try:
                insert_suggestion(plant_name, description, location,
                                  plant_type, uploader_name, image_path)
                flash("Plant suggestion submitted successfully!", 'success')
                # Redirect to a thanks page after successful submission
                return redirect(url_for('thanks'))
            except Exception as e:
                flash(f"An error occurred: {e}", 'error')
                return redirect(request.url)

        else:
            # If the file is not allowed, show an error
            app.logger.warning(
                f"Invalid file type attempted: {file.filename}")
            flash('Invalid file type!')
            return redirect(request.url)

    return render_template('suggest_plant.html')


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


# for login page:

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the passwords match
        if password != confirm_password:
            error = 'Passwords do not match.'
            return render_template('register.html', error=error)

        # Check if the password is strong
        if not is_strong_password(password):
            error = 'Password must be at least 8 characters long and contain uppercase, lowercase, digits, and special characters.'
            return render_template('register.html', error=error)

        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        # Handle the case where the username already exists
        # username TEXT UNIQUE.. see this code in schema.sql, That UNIQUE makes sure no two rows can have the same username.
        except sqlite3.IntegrityError:
            error = 'Username already exists.'

    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    # app.run(debug=True)   # for self hosted self machine only. loop back for others...
    # for hosting on local network, 0000 means all can access, and can listen.. if same network shared devices
    app.run(host='0.0.0.0', port=5000, debug=True)
