# Changelog

All notable changes to this project will be documented in this file.  
This file follows a simplified version of [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Dates are in `YYYY-MM-DD` format.

## Purpose: Record of what has changed over time. (Added/changed/removed/fixed)


## [1.0.0] - 2025-05-12

### Added
- Admin dashboard to manage plant suggestions and approved plants.
- Edit, Approve, and Delete functionality with modals.
- Upload image support for plant suggestions.
- Image compression using PIL python, before saving images for better efficiency, web rendering and less storage.
- SQLite-backed storage for user credentials and plant records.
- Separation of suggestions and approved plants in dashboard view.
- Login/register with password validation, session-based login protection.
- Documentations added for README, NOTES.

### Changed
- Admin view now shows suggestions and approved plants using toggle sections.
- Dashboard buttons use icons and modals for better UX.

### Fixed
- Image file deletion now handled with database record removal.
- Bug with view persistence (toggle) when redirecting after actions.
- Session protection for admin-only pages.

---


## [0.1.3] - 2025-04-17

### Added
- Register Page.
- Message greeting in homepage of username using session.
- All error handling messages regarding password and username credentials during register page.
- Pop message in html before logout confirmation

### Fixed
- Password confirmation matching in flask backend for better security.
- Password strength checker using regex search function. (concise)
- Existing username check (database handling).

---

## [0.1.2] - 2025-04-10

### Added
- Login and logout button.

### Fixed
- Login credential checks using Flask Session method now for better security.

---

## [0.1.1] - 2025-04-06

### Fixed
- Removed commented `<link>` tag to Chamomile stylesheet which was possibly causing layout issues or unexpected behavior in HTML.
- Used jinja2 syntax for all links reference *(url_for())* instead of hardcoding paths of links, for better ease with Flask support.
- General cleanup of old commented code (HTML/CSS) to prevent confusion or browser misinterpretation.

---

## [0.1.0] - 2025-04-05

### Added
- Initial layout and structure with basic HTML and CSS.
- Header, sections, and minimal JS interactivity.
- Used bootstrap for header, navbar and footer along with other cards.
- Jinja2 syntax for extend layout page, for concise non repeat with all plants pages.
- Initial commit to Git.

---

## [Unreleased]
- (Placeholder for future planned features like search, filtering, tags, etc.)

---

## 🛠 Future Enhancements

- Implement tags, categories, and search filters.
- Add image resizing/thumbnails for optimization.
- Allow multiple admins with roles/permissions.
- Optional: hash passwords using `werkzeug.security`.

## Notes

- This project is being developed as a learning journey; some parts are left commented intentionally to track progress.
- Future versions may remove commented parts once functionality is finalized or moved to documentation.
