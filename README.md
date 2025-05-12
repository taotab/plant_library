# 🌿 Plant Library – Ayurvedic Plant Portal

## 📖 Project Overview

A virtual garden to explore and manage information about Ayurvedic plants.  
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
   `git clone https://github.com/taotab/plant_library.git`
2. Install dependencies:  
   `pip install -r requirements.txt`
3. Run init_db.py:
   `python init_db.py`
3. Run the app:  
   `flask run`
4. Visit `http://localhost:5000` in browser. *(all viewing devices be in same network)*

---

## 📜 Documentation

- [`CHANGELOG.md`](./CHANGELOG.md): Version history and updates.
- [`notes.md`](./notes.md): Dev notes, design decisions, and future ideas.

---

## ✅ Admin Credentials (Demo)

Use `admin / P@ssword123` to log in (if seeded).

---

## 🔮 Planned Features

- Search/filter by plant type or location.
- Tag system (e.g., Medicinal, Edible, etc.)
- Optional animations or hover info on plant cards.
- Hashed password storage.
