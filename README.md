# 🌿 Plant Library – Ayurvedic Plant Portal

## 📖 Project Overview

A virtual portal to explore and manage information about Ayurvedic plants.  
Users can submit new plant suggestions, while admins can review, edit, and approve them into a permanent library.


Taken 5 plants. *(default experimental)*

- Tulsi
- Aloe vera
- Chamomile
- Stevia
- Fenugreek/methi

---


## ✨ Features

- 🖼️ Suggestion box for crowd public, a plant with name, location, and image.
- 🛠️ Admin dashboard to approve, delete, or edit suggestions.
- 🔐 Login & registration with session management.
- 📁 Approved plants shown in dedicated section.
- 📷 Image upload and auto-deletion upon plant removal, along with image compression using `PIL` (pillow library).
- 🎛️ Clean, toggle-based UI for pending vs approved plants.

---

## 🧰 Tech Stack

- **Frontend**: HTML, Bootstrap, JS
- **Backend**: Python, Flask
- **Database**: SQLite3
- **File Uploads**: Local storage (`/static/uploads`)
- **Other Images**: Local Storage (`/static/img`) & (`/static/logos`)

---


## 🚀 Setup Instructions

1. Clone repo:  
   - `git clone https://github.com/taotab/plant_library.git`
   - `cd plant_library`
2. Install dependencies:  
   - `pip install -r requirements.txt`
   - (Use pip3 if needed, depending on your system)
3. Run init_db.py:
   - `python init_db.py`
   - (This reads schema.sql and sets up the SQLite database database.db in the root directory)
3. Run the app:  
   - `flask run`
4. Visit `http://localhost:5000` in browser. *(all viewing devices be in same network)*

---

## 📜 Documentation

- [`CHANGELOG.md`](./CHANGELOG.md): Version history and updates.
- [`NOTES.md`](./NOTES.md): Dev notes, design decisions, and future ideas.
- Demonstration link: https://youtu.be/lYxnKBvpMZ8?si=Qh4bm9A_u7vyt2Qb

---

## ✅ Admin Credentials (Demo)

Use `admin / P@ssword123` to log in (if seeded).

---

## 🔮 Planned Features

- Tag system (e.g., Medicinal, Edible, etc.)
- Optional animations or hover info on plant cards.
- Hashed password storage.
- Deploy online in hosting sites like Render, Pythonanywhere, etc.


---

```markdown

## 🗂️ File Structure

plant_library/
│
├── app.py                  # Main Flask application
├── database.db             # SQLite database
├── init_db.py              # One-time DB setup script (can be deleted later)
├── schema.sql              # DB schema (for table creation)
│
├── db/
│   └── helpers.py          # DB functions (insert_suggestion, get_db_connection, etc.), image compression
│
├── templates/
│   ├── layout.html
│   ├── suggest_plant.html
│   ├── thanks.html
│   └── register.html
│
└──static/                 # CSS, JS, uploaded images & logos (if served)
```

