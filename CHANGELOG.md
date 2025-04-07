# Changelog

All notable changes to this project will be documented in this file.  
This file follows a simplified version of [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Dates are in `YYYY-MM-DD` format.

---

## [Unreleased]

### Added
- Placeholder section for future planned features.
- Dynamic routing instead of hardcoding for every page's route in flask.
- `README.md` for project overview.

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

## Notes

- This project is being developed as a learning journey; some parts are left commented intentionally to track progress.
- Future versions may remove commented parts once functionality is finalized or moved to documentation.
