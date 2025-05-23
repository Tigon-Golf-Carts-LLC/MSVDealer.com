import os
import re
from pathlib import Path

# Get all dealer HTML files
dealer_files = list(Path('/home/ubuntu/dealership_enhanced').glob('dealer-*.html'))

# Read the template file
with open('/home/ubuntu/dealership_enhanced/dealer-template.html', 'r') as f:
    template = f.read()

# Process each dealer file
for dealer_file in dealer_files:
    # Read the current dealer file
    with open(dealer_file, 'r') as f:
        content = f.read()
    
    # Extract dealer name
    name_match = re.search(r'<h1>(.*?)</h1>\s*<p class="subtitle">Medium Speed Vehicles Dealer</p>', content)
    dealer_name = name_match.group(1) if name_match else "Unknown Dealer"
    
    # Extract phone number
    phone_match = re.search(r'<li><strong>Phone:</strong> (.*?)</li>', content)
    phone = phone_match.group(1) if phone_match else ""
    phone_html = f'<li><strong>Phone:</strong> <a href="tel:{phone.replace("-", "").replace(" ", "")}">{phone}</a></li>' if phone else ""
    
    # Extract address
    address_match = re.search(r'<li><strong>Address:</strong> (.*?)</li>', content)
    address = address_match.group(1) if address_match else ""
    address_html = f'<li><strong>Address:</strong> {address}</li>' if address else ""
    
    # Extract website
    website_match = re.search(r'<li><strong>Website:</strong> <a href=\'(.*?)\' target=\'_blank\'>Visit Dealer Site</a></li>', content)
    website = website_match.group(1) if website_match else ""
    website_html = f'<li><strong>Website:</strong> <a href=\'{website}\' target=\'_blank\'>Visit Dealer Site</a></li>' if website else ""
    
    # Extract Facebook
    facebook_match = re.search(r'<li><strong>Facebook:</strong> <a href=\'(.*?)\' target=\'_blank\'>Facebook</a></li>', content)
    facebook = facebook_match.group(1) if facebook_match else ""
    facebook_html = f'<li><strong>Facebook:</strong> <a href=\'{facebook}\' target=\'_blank\'>Facebook</a></li>' if facebook else ""
    
    # Extract YouTube
    youtube_match = re.search(r'<li><strong>YouTube:</strong> <a href=\'(.*?)\' target=\'_blank\'>YouTube</a></li>', content)
    youtube = youtube_match.group(1) if youtube_match else ""
    youtube_html = f'<li><strong>YouTube:</strong> <a href=\'{youtube}\' target=\'_blank\'>YouTube</a></li>' if youtube else ""
    
    # Extract Pinterest
    pinterest_match = re.search(r'<li><strong>Pinterest:</strong> <a href=\'(.*?)\' target=\'_blank\'>Pinterest</a></li>', content)
    pinterest = pinterest_match.group(1) if pinterest_match else ""
    pinterest_html = f'<li><strong>Pinterest:</strong> <a href=\'{pinterest}\' target=\'_blank\'>Pinterest</a></li>' if pinterest else ""
    
    # Extract Google Maps CID
    cid_match = re.search(r'<a href="(https://www\.google\.com/maps\?cid=[0-9]+)" target="_blank" class="map-link">View on Google Maps</a>', content)
    cid = cid_match.group(1) if cid_match else ""
    cid_html = f'<a href="{cid}" target="_blank" class="map-link">View on Google Maps</a>' if cid else ""
    
    # Extract lat/lon from the original Python data
    latlon_match = re.search(r'"latlon": "([^"]*)"', open('/home/ubuntu/dealership_enhanced/dealers.py', 'r').read())
    latlon = ""
    if latlon_match:
        dealer_id = str(dealer_file).split('/')[-1]
        # Find the latlon for this specific dealer
        dealer_section = re.search(rf'"filename": "{dealer_id}".*?"latlon": "([^"]*)"', 
                                  open('/home/ubuntu/dealership_enhanced/dealers.py', 'r').read(), 
                                  re.DOTALL)
        if dealer_section:
            latlon = dealer_section.group(1)
    
    # Create map embed if we have coordinates
    map_embed = ""
    if latlon and latlon != "":
        # Split latitude and longitude
        try:
            lat, lon = latlon.split(',')
            lat = lat.strip()
            lon = lon.strip()
            if lat and lon:
                map_embed = f'''
                <iframe 
                    width="100%" 
                    height="400" 
                    frameborder="0" 
                    style="border:0; margin-bottom: 20px;" 
                    src="https://www.google.com/maps/embed/v1/place?key=AIzaSyBZjCd5dL1xrLzpHRYK9KLzJ7JVTWhPHiQ&q={lat},{lon}&zoom=14" 
                    allowfullscreen>
                </iframe>
                '''
        except:
            map_embed = ""
    
    # Extract review link
    review_match = re.search(r'<h2>Leave a Review</h2><p>Had a great experience\? <a href=\'(.*?)\' target=\'_blank\'>Leave us a review</a> to let others know!</p>', content)
    review = review_match.group(1) if review_match else ""
    review_html = f'<h2>Leave a Review</h2><p>Had a great experience? <a href=\'{review}\' target=\'_blank\'>Leave us a review</a> to let others know!</p>' if review else ""
    
    # Create visit location section if we have an address
    visit_location_html = ""
    if address and "Service Area" not in address:
        visit_location_html = f'<h2>Visit Our Location</h2><p>Come visit our showroom at {address} to see our selection of Medium Speed Vehicless and speak with our knowledgeable staff.</p>'
    
    # Replace placeholders in template
    new_content = template.replace('DEALER_NAME', dealer_name)
    new_content = new_content.replace('DEALER_PHONE', phone_html)
    new_content = new_content.replace('DEALER_ADDRESS', address_html)
    new_content = new_content.replace('DEALER_WEBSITE', website_html)
    new_content = new_content.replace('DEALER_FACEBOOK', facebook_html)
    new_content = new_content.replace('DEALER_YOUTUBE', youtube_html)
    new_content = new_content.replace('DEALER_PINTEREST', pinterest_html)
    new_content = new_content.replace('DEALER_MAP_LINK', cid_html)
    new_content = new_content.replace('DEALER_MAP_EMBED', map_embed)
    new_content = new_content.replace('DEALER_VISIT_LOCATION', visit_location_html)
    new_content = new_content.replace('DEALER_REVIEW', review_html)
    
    # Write the updated file
    with open(dealer_file, 'w') as f:
        f.write(new_content)
    
    print(f"Updated {dealer_file}")

print("All dealer pages have been updated with tel: links and map embeds.")
