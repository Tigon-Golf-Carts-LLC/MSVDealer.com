# MSVDealer.com - Medium Speed Vehicle Dealer Website

A static website for listing Medium Speed Vehicle dealers across the United States. This project is designed to be hosted on GitHub Pages.

## Project Structure

- `index.html` - Main homepage listing all dealers
- `dealer-*.html` - Individual dealer pages (30 total)
- `css/styles.css` - Dark theme styling for the website
- `dealers.py` - Python script to generate HTML files from dealer data

## Features

- Dark theme design
- Responsive layout for mobile and desktop
- 30 dealer pages with detailed information
- Dealer grid on homepage with links to individual pages
- Information about Medium Speed Vehicles and their benefits

## Setup

1. Clone this repository
2. Open `index.html` in your browser to view the site locally
3. Deploy to GitHub Pages for public access

## Customization

To modify dealer information or add new dealers:

1. Edit the dealer data in `dealers.py`
2. Run the script to regenerate HTML files: `python dealers.py`
3. Commit and push changes to GitHub

## License

© 2025 MSVDealer.com - All Rights Reserved

## Lead forms (TIGON IOT Webhook Flows)

- `js/tigon-lead.js` + `css/tigon-lead.css` are loaded on every page (except the `index.html` redirect).
- They add a "Get a Quote" pop-up form and floating Call Now / Get a Quote buttons to every page, Call Now / Request a Quote buttons on dealer pages, and render the contact form into `<div data-tigon-form>` on `contact.html`.
- To pre-fill a specific cart on a page, add `<div data-tigon-listing data-brand="…" data-model="…" data-vin="…" data-sku="…"></div>`.
- New pages: add `<link rel="stylesheet" href="css/tigon-lead.css">` in `<head>` and `<script src="js/tigon-lead.js" defer></script>` before `</body>`.
