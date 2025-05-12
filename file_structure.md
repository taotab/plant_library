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
