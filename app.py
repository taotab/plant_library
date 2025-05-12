from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.utils import secure_filename
import time
from datetime import datetime
import logging
import sqlite3
import os
import re
from db.helpers import insert_suggestion, get_db_connection, update_suggestion, delete_suggestion_by_id, get_suggestion_by_id, insert_plant_from_suggestion, compress_and_save_image
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
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
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

# 2025-04-30 19:50:25 to 30 Apr 2025, 07:50 PM convert format
# used in jinja2 template, to format datetime in dashboard.html


@app.template_filter('datetime_format')
def datetime_format(value, format='%d %b %Y, %I:%M %p'):
    try:
        dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return dt.strftime(format)
    except Exception as e:
        return value  # fallback


@app.route('/')
def welcome_page():

    return render_template('welcome_page.html')


@app.route('/about')
def about():

    # return render_template('about.html')
    return render_template('about.html')


# Route for all pages instead of hardcoding : dynamic routing...


# Loop over all images in the static folder, and show them in the index.html page
@app.route('/index')
def index():
    # image_folder = os.path.join('static', 'plants_img')
    # List all image filenames
    # images = os.listdir(image_folder)
    # images = [img for img in images if img.endswith(
    #     ('png', 'jpg', 'jpeg', 'gif', 'webp'))]

    # return render_template('index2.html', images=images)

    conn = get_db_connection()
    plants = conn.execute('SELECT * FROM plants').fetchall()
    conn.close()
    return render_template('index.html', plants=plants)


# route for dynamic plant detail pages (experimental).......................

@app.route('/plant/<int:plant_id>')
def plant_detail(plant_id):
    conn = get_db_connection()
    plant = conn.execute(
        'SELECT * FROM plants WHERE id = ?', (plant_id,)).fetchone()
    conn.close()
    if plant is None:
        abort(404)
    return render_template('plant_detail.html', plant=plant)


#  end of dynamic plant detail pages (experimental).......................


@app.route('/plants/<plant_name>')
def plant_page(plant_name):
    try:
        return render_template(f'{plant_name}.html')
    except:
        return render_template('404.html')


# Pending uploads dashboard page route

@app.route('/dashboard')
def dashboard():

    if not 'username' in session:
        return redirect(url_for('login'))

    # admin logic
    conn = get_db_connection()
    suggestions = conn.execute(
        'SELECT * FROM suggestions ORDER BY id DESC').fetchall()
    plants = conn.execute('SELECT * FROM plants ORDER BY id DESC').fetchall()
    conn.close()
    # Read view from query param
    view = request.args.get('view', 'pending')
    return render_template('dashboard.html', suggestions=suggestions, plants=plants, current_view=view)


# suggestion updates codes:...........................


@app.route('/delete_suggestion/<int:id>', methods=['POST'])
def delete_suggestion(id):
    suggestion = get_suggestion_by_id(id)
    if suggestion is None:
        flash("Suggestion not found.", "danger")
        return redirect(url_for('dashboard'))

    image_filename = suggestion['image_filename']
    plant_name = suggestion['plant_name']

    try:
        # Delete image file if it exists
        if image_filename:
            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'], image_filename)
            if os.path.exists(image_path):
                os.remove(image_path)
                app.logger.info(f"Deleted image file: {image_filename}")

        # Delete DB entry
        delete_suggestion_by_id(id)
        app.logger.info(
            f"Suggestion ID: '{id}', '{plant_name}' deleted successfully.")
        flash(f"Deleted suggestion for '{plant_name}'.", "success")

    except Exception as e:
        app.logger.error(f"Error deleting suggestion ID {id}: {e}")
        flash("Failed to delete the suggestion.", "danger")

    return redirect(url_for('dashboard'))


@app.route('/edit_suggestion/<int:id>', methods=['POST'])
def edit_suggestion(id):
    plant_name = request.form['plant_name'].strip()
    description = request.form['description'].strip()
    plant_type = request.form['plant_type'].strip()
    location = request.form['location'].strip()
    # benefits = request.form['benefits'].strip()
    benefits = request.form.get('benefits', '').strip()
    if not benefits:
        benefits = ''

    image_file = request.files.get('image')

    new_filename = None  # Default: no image change

    # Validate input lengths

    if len(plant_name) > 100 or len(location) > 200:
        app.logger.warning("Characters exceed the allowed length")
        flash("One or more fields exceed the allowed length.")
        return redirect(url_for('dashboard'))

    if image_file and image_file.filename:
        if allowed_file(image_file.filename):
            try:
                # Prepare new filename
                original_name = secure_filename(image_file.filename)
                timestamp = int(time.time())
                new_filename = f"{timestamp}_{original_name}"

                # Save the new image
                upload_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], new_filename)
                image_file.save(upload_path)
                app.logger.info(
                    f"New image saved in directory: {new_filename}")

                # Optional: delete old image if needed
                # Fetch current filename from DB to delete the old file
                conn = get_db_connection()
                old = conn.execute(
                    'SELECT image_filename FROM suggestions WHERE id = ?', (id,)).fetchone()
                conn.close()

                if old and old['image_filename']:
                    old_path = os.path.join(
                        app.config['UPLOAD_FOLDER'], old['image_filename'])
                    if os.path.exists(old_path):
                        os.remove(old_path)

                        app.logger.info(
                            f"Old image deleted: {old['image_filename']}")

                flash("Image updated.", "info")

            except Exception as e:
                app.logger.exception("Failed to save new image")
                flash("Image upload failed. Please try again.", "error")
                return redirect(url_for('dashboard'))
        else:
            app.logger.warning(
                f"Invalid file type attempted: {image_file.filename}")
            flash("Invalid file type for image.", "error")
            return redirect(url_for('dashboard'))

    try:
        # Call your helper update function
        update_suggestion(id, plant_name, description,
                          plant_type, location, new_filename, benefits)

        app.logger.info(f"Suggestion updated successfully: {plant_name}")
        flash('Suggestion updated successfully.', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        app.logger.exception("Error updating suggestion")
        flash(f"Error updating suggestion: {e}", 'error')
        return redirect(url_for('dashboard'))


@app.route('/approve_suggestion/<int:id>', methods=['POST'])
def approve_suggestion(id):
    conn = get_db_connection()
    try:
        suggestion = conn.execute(
            'SELECT * FROM suggestions WHERE id = ?', (id,)).fetchone()

        if not suggestion:
            flash("Suggestion not found.", "warning")
            return redirect(url_for('dashboard'))

        # Insert into plants using helper
        insert_plant_from_suggestion(suggestion)

        # Delete from suggestions
        conn.execute('DELETE FROM suggestions WHERE id = ?', (id,))
        conn.commit()

        flash(
            f"'{suggestion['plant_name']}' approved and added to public database!", "success")
    except Exception as e:
        app.logger.error(f"Error approving suggestion ID {id}: {e}")
        flash("Failed to approve suggestion.", "danger")
    finally:
        conn.close()

    return redirect(url_for('dashboard'))


# end of suggestion updates codes:.......................


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

            # try:
            #     file.save(os.path.join(
            #         app.config['UPLOAD_FOLDER'], unique_filename))
            # except Exception as e:
            #     app.logger.error(f"File save error: {e}")
            #     flash("Failed to save file. Please try again.")
            #     return redirect(request.url)

            # image compression using PIL and save it to the upload folder
            save_path = os.path.join(
                app.config['UPLOAD_FOLDER'], unique_filename)

            try:
                # Compress and save image
                compress_and_save_image(file, save_path)
            except Exception as e:
                app.logger.error(f"Image compression error: {e}")
                flash("Image upload failed during compression. Please try again.")
                return redirect(request.url)

            # Log the successful file upload
            app.logger.info(
                f"File compressed & uploaded successfully: {unique_filename}")

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


# Routes for deleting plants from the database (approved ones public)..............

@app.route('/delete_plant/<int:id>', methods=['POST'])
def delete_plant(id):
    conn = get_db_connection()
    plant = conn.execute('SELECT * FROM plants WHERE id = ?', (id,)).fetchone()

    if plant is None:
        flash("Plant not found.", "danger")
        return redirect(url_for('dashboard'))

    image_filename = plant['image_filename']
    plant_name = plant['plant_name']

    try:
        if image_filename:
            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'], image_filename)
            if os.path.exists(image_path):
                os.remove(image_path)
                app.logger.info(f"Deleted plant image: {image_filename}")

        conn.execute('DELETE FROM plants WHERE id = ?', (id,))
        conn.commit()
        flash(f"Deleted plant: '{plant_name}'", "success")
    except Exception as e:
        app.logger.error(f"Error deleting plant ID {id}: {e}")
        flash("Failed to delete the plant.", "danger")
    finally:
        conn.close()

    # return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard', view='approved'))


# end of routes for deleting plants from the database (approved ones public)..............


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
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        # Check if the password is strong
        if not is_strong_password(password):
            flash('Password must be at least 8 characters and include uppercase, lowercase, digits, and special characters.', 'danger')
            return render_template('register.html')

        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)
            )
            conn.commit()
            conn.close()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        # Handle the case where the username already exists
        # username TEXT UNIQUE.. see this code in schema.sql, That UNIQUE makes sure no two rows can have the same username.
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'warning')

    return render_template('register.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    # app.run(debug=True)   # for self hosted self machine only. loop back for others...
    # for hosting on local network, 0000 means all can access, and can listen.. if same network shared devices
    app.run(host='0.0.0.0', port=5000, debug=True)
