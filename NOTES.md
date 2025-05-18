# 🧠 Dev Notes & Observations

## Purpose: Personal explanations, tips, observations, just for understanding

### 🧭 Data Flow Summary (How it all works)

- Public users submit plant suggestions via a form (with image upload).
- The image is compressed using Pillow (PIL) and saved to /static/uploads.
- Suggestions are stored in the suggestions table.
- Admin logs in via the dashboard to view, edit, approve, or delete suggestions.
- Upon approval, the suggestion (with any edits) is copied into the plants table and displayed on the public Index page.
- Deleting a suggestion or approved plant also removes the image from disk for cleanup.

---

### 🔐 Flask Sessions

- Flask is stateless; it forgets everything going to other pages. 
- Use `session` for login persistence. *(add in whichever routes)*
- Stores data safely and securely encrypted (using `app.secret_key`) in browser cookies
- Avoid global variables across routes for tracking across pages, its unreliable. (seeing who logged in).

---

### 🗃️ SQLite Integration

- **Why sqlite3 chosed?** - Easy use, light, and pre-installed with python, portability.
- Login and register use secure database queries. *(stored in users table of database.db)*
- Keep database file in root for easy access.

---

### 📁 Directory uploads usage

- **Note-** Use absolute path of files in python and flask in same code directory by default to save headache and errors and robustness of code consistency. 
- Issues occur with vscode working directory and script local directory.

    1. This can check current working directory, add this above app.py to see where flask is running from
        ``` python
        import os
        print("👀 Current working dir:", os.getcwd())
        ```
    2. For uploads: use `url_for('static', filename=...)` for absolute current templates and static files.
    3. Use `os.path.join()` for functions and database join with absolute path.

---

### 🔍 Notes on Regex for Passwords

- **Why only use in flask?** - Safer than front-end-only validation.
- Javascript and html can be quick and ui/ux design.. but can be bypassed, flask check backend is better and secure.
- Password check includes a must inclusion of capital, special, numbers characters.
- Backend password check uses regex instead of multiple `if` loops.
- **Why use regex?** - Regex ensures strength, match, and format compliance. For character comparisions, its better, simple and less code..
- **What's the logic? idk, must do research. REGEX vs FOR LOOPs**
    1. for more info on regex use: https://www.w3schools.com/python/python_regex.asp
    2. (regular expression), like a pattern searching regex engine, to search in a given string.

---


### 🧪 Lessons & Tips

- Always test uploads with different file types and sizes.
- Use `os.getcwd()` when debugging file paths.
- Use Flask's `debug=True` for helpful error messages during dev.
- Redirect with `url_for('dashboard', view='approved')` to retain view state.
- Log actions (`app.logger`) for debugging (e.g., image delete), catch success and error messages printed in flask terminal logs.
- Used dynamic routing using flask jinja2 arguments and such *for example:* `(route/<int: value>)` for individual plant pages, same format, just values changed. Makes code cleaner.
- Use flash() messges, using bootstrap floating message features for better design.
- `db/helpers.py` has CRUD operations of database, involving table entries deltion, addition, etc. Also has image compression function. Its imported in app.py as `from db.helpers import <function_name>`

---

### 🧩 Next Steps (Optional)

- Add password hashing (e.g., `werkzeug.security.generate_password_hash()`).
- Add more detailed plant information (scientific name, benefits, usage).
- Support multiple users or admins.
- Better error pages (custom 404/500).