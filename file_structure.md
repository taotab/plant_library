your_project/
│
├── app.py                  # Main Flask application
├── database.db             # SQLite database
├── init_db.py              # One-time DB setup script (can be deleted later)
│
├── db/
│   └── helpers.py          # DB functions (insert_suggestion, get_db_connection, etc.)
│
├── templates/
│   ├── layout.html
│   ├── suggest_plant.html
│   ├── thanks.html
│   └── register.html
│
├── static/                 # CSS, JS, uploaded images (if served)
│
└── schema.sql              # DB schema (for table creation)
