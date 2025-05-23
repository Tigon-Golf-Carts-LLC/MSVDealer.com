import os
import zipfile

# Dealer info as dictionaries
dealers = [
    {
        "filename": "dealer-tigon.html",
        "name": "TIGON National",
        "phone": "1-844-844-6638",
        "address": "Nationwide",
        "latlon": "",
        "cid": "https://www.google.com/maps?cid=913687030872245288",
        "facebook": "https://www.facebook.com/Tigongolfcarts",
        "youtube": "https://www.youtube.com/@TigonGolfCarts",
        "website": "https://tigongolfcarts.com",
        "pinterest": "https://www.pinterest.com/tigongolfcarts/",
        "review": "https://g.page/r/CSiEBX-DEa4MEBM/review"
    },
    {
        "filename": "dealer-dover-de.html",
        "name": "Dover, DE",
        "phone": "302-546-0010",
        "address": "5158 N Dupont Hwy, Dover, DE 19901",
        "latlon": "39.22044318468275, -75.57452048907642",
        "cid": "https://www.google.com/maps?cid=12843447677705895190",
        "facebook": "https://www.facebook.com/TigonGolfCartsDover/",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsDoverDE",
        "website": "https://tigongolfcarts.com/dover/",
        "pinterest": "",
        "review": "https://g.page/r/CRa9-YidFz2yEBM/review"
    },
    {
        "filename": "dealer-pocono-pa.html",
        "name": "Pocono, PA",
        "phone": "570-643-0152",
        "address": "1712 Pennsylvania 940, Pocono Pines, PA 18350",
        "latlon": "41.10286354605563, -75.48758590250345",
        "cid": "https://www.google.com/maps?cid=17137841834562046914",
        "facebook": "https://www.facebook.com/TigonGolfCartsPoconos/",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsPoconosPA",
        "website": "https://tigongolfcarts.com/pocono/",
        "pinterest": "",
        "review": "https://g.page/r/CcJL5i1Z2NXtEBM/review"
    },
    {
        "filename": "dealer-ocean-view-nj.html",
        "name": "Ocean View, NJ",
        "phone": "609-840-0404",
        "address": "101 NJ-50, Ocean View, NJ 08230",
        "latlon": "39.22254797811702, -74.70417212536503",
        "cid": "https://www.google.com/maps?cid=6446924254429489274",
        "facebook": "https://www.facebook.com/TigonGolfCartsOceanView/",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsOceanViewNJ",
        "website": "https://tigongolfcarts.com/ocean-view/",
        "pinterest": "",
        "review": "https://g.page/r/CXqoHr9zE3hZEBM/review"
    },
    {
        "filename": "dealer-hatfield-pa.html",
        "name": "Hatfield, PA",
        "phone": "215-595-8736",
        "address": "2333 Bethlehem Pike, Hatfield, PA 19440",
        "latlon": "40.29839945958623, -75.28308913039525",
        "cid": "https://www.google.com/maps?cid=8221925612164093496",
        "facebook": "https://www.facebook.com/TigonGolfCartsHatfield/",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsHatfieldPA",
        "website": "https://tigongolfcarts.com/hatfield/",
        "pinterest": "",
        "review": "https://g.page/r/CTgWulrIJRpyEBM/review"
    },
    {
        "filename": "dealer-scranton-wilkes-barre-pa.html",
        "name": "Scranton-Wilkes-Barre, PA",
        "phone": "570-344-4443",
        "address": "1225 N Keyser Ave #2, Scranton, PA 18504",
        "latlon": "41.4374075,-75.6835104",
        "cid": "https://www.google.com/maps?cid=13243686786001524416",
        "facebook": "https://www.facebook.com/TigonGolfCartsScranton/",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsScrantonWilkesPA",
        "website": "https://tigongolfcarts.com/scranton-wilkes-barre/",
        "pinterest": "",
        "review": "https://g.page/r/CcDWJ7z2Bsu3EBM/review"
    },
    {
        "filename": "dealer-raleigh-nc.html",
        "name": "Raleigh, NC",
        "phone": "984-489-0298",
        "address": "2700 S Wilmington St, Raleigh, NC 27603",
        "latlon": "35.7471032,-78.6452007",
        "cid": "https://www.google.com/maps?cid=14570072271497929915",
        "facebook": "https://www.facebook.com/TigonGolfCartsRaleigh/",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsRaleighNC",
        "website": "https://tigongolfcarts.com/raleigh/",
        "pinterest": "https://www.pinterest.com/tigongolfcarts/tigon-golf-carts-in-raleigh/",
        "review": "https://g.page/r/CbskZw6JSzPKEBM/review"
    },
    {
        "filename": "dealer-orangeburg-sc.html",
        "name": "Orangeburg, SC",
        "phone": "803-596-0246",
        "address": "4166 North Rd, Orangeburg, SC 29118",
        "latlon": "33.547201,-80.9162039",
        "cid": "https://www.google.com/maps?cid=17192321019507936230",
        "facebook": "https://www.facebook.com/TigonGolfCartsOrangeburg/",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsOrangeburgSC",
        "website": "https://tigongolfcarts.com/orangeburg/",
        "pinterest": "",
        "review": ""
    },
    {
        "filename": "dealer-swanton-oh.html",
        "name": "Swanton, OH",
        "phone": "419-402-8400",
        "address": "10420 AIrport Hwy, Swanton, OH 43558",
        "latlon": "41.6013184,-83.7926472",
        "cid": "https://www.google.com/maps?cid=16517552730289967239",
        "facebook": "https://www.facebook.com/TigonGolfCartsSwanton/",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsSwantonOH",
        "website": "https://tigongolfcarts.com/swanton/",
        "pinterest": "",
        "review": "https://g.page/r/CYeQt8exIjrlEBM/review"
    },
    {
        "filename": "dealer-south-bend-in.html",
        "name": "South Bend, IN",
        "phone": "574-703-0456",
        "address": "52129 State Road 933, South Bend, IN 46637",
        "latlon": "41.7360283,-86.2511865",
        "cid": "https://www.google.com/maps?cid=17532455648086849827",
        "facebook": "https://www.facebook.com/TigonGolfCartsSouthBend/",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsSouthBendIN",
        "website": "https://tigongolfcarts.com/south-bend/",
        "pinterest": "",
        "review": ""
    },
    {
        "filename": "dealer-gloucester-point-va.html",
        "name": "Gloucester Point, VA",
        "phone": "804-792-0234",
        "address": "2810 George Washington Memorial Hwy, Gloucester Point, VA 23072",
        "latlon": "37.2850625,-76.5074161",
        "cid": "https://www.google.com/maps?cid=16682967888503617377",
        "facebook": "https://www.facebook.com/TigonGolfCartsGloucesterPoint/",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsGloucesterPoint",
        "website": "https://tigongolfcarts.com/gloucester-point/",
        "pinterest": "",
        "review": ""
    },
    {
        "filename": "dealer-lecanto-fl.html",
        "name": "Lecanto, FL",
        "phone": "352-453-0345",
        "address": "299 E. Gulf to Lake Hwy, Lecanto, FL 34461",
        "latlon": "28.858622,-82.4295381",
        "cid": "https://www.google.com/maps?cid=4773802157529013859",
        "facebook": "https://www.facebook.com/TigonGolfCartsLecanto/",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsLecantoFL",
        "website": "https://tigongolfcarts.com/lecanto/",
        "pinterest": "",
        "review": "https://g.page/r/CWOeggPF8z9CEBM/review"
    },
    {
        "filename": "dealer-pleasantville-nj.html",
        "name": "Pleasantville, NJ",
        "phone": "640-444-3094",
        "address": "7000 Black Horse Pike, Pleasantville, NJ 08232",
        "latlon": "39.38812835576412, -74.5186949022294",
        "cid": "https://www.google.com/maps?cid=7635149767591436869",
        "facebook": "https://www.facebook.com/TigonGolfCartPleasantville",
        "youtube": "",
        "website": "https://tigongolfcarts.com/pleasantville/",
        "pinterest": "https://www.pinterest.com/tigongolfcarts/tigon-golf-carts-in-pleasantville-nj/",
        "review": "https://g.page/r/CUWiMchCgPVpEBM/review"
    },
    {
        "filename": "dealer-portsmouth-va.html",
        "name": "Portsmouth, VA",
        "phone": "757-977-0146",
        "address": "2008 Portsmouth Blvd, Portsmouth, VA 23704",
        "latlon": "36.817786,-76.3235434",
        "cid": "https://www.google.com/maps?cid=5113923461119431468",
        "facebook": "https://www.facebook.com/TigonGolfCartsPortsmouthVA/",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsPortsmouthVA",
        "website": "https://tigongolfcarts.com/portsmouth/",
        "pinterest": "",
        "review": "https://g.page/r/CSxTjwxLTvhGEBM/review"
    },
    {
        "filename": "dealer-virginia-beach-va.html",
        "name": "Virginia Beach, VA",
        "phone": "1-844-844-6638",
        "address": "1101 Virginia Beach Blvd, Virginia Beach, VA 23451",
        "latlon": "36.8414381,-75.9965854",
        "cid": "https://www.google.com/maps?cid=17806490138133315425",
        "facebook": "https://www.facebook.com/TigonGolfCartsVirginiaBeach/",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsVirginiaBeachVA",
        "website": "https://tigongolfcarts.com/virginia-beach/",
        "pinterest": "",
        "review": ""
    },
    {
        "filename": "dealer-tristate.html",
        "name": "TriState Golf Cars",
        "phone": "",
        "address": "",
        "latlon": "",
        "cid": "",
        "facebook": "",
        "youtube": "",
        "website": "",
        "pinterest": "",
        "review": "https://g.page/r/CcfFABSQEz-VEBM/review"
    },
    # Service states (next 12)
    {
        "filename": "dealer-pennsylvania.html",
        "name": "Pennsylvania",
        "phone": "1-844-844-6638",
        "address": "",
        "latlon": "41.1169824,-77.6047047",
        "cid": "https://www.google.com/maps?cid=13935683838976847185",
        "facebook": "",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsPennsylvania",
        "website": "https://tigongolfcarts.com/pennsylvania/",
        "pinterest": "",
        "review": "https://g.page/r/CVHtXfydfmXBEBM/review"
    },
    {
        "filename": "dealer-new-jersey.html",
        "name": "New Jersey",
        "phone": "1-844-844-6638",
        "address": "",
        "latlon": "40.073132,-74.724323",
        "cid": "https://www.google.com/maps?cid=15178469885958324473",
        "facebook": "",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsNewJersey",
        "website": "https://tigongolfcarts.com/new-jersey/",
        "pinterest": "",
        "review": "https://g.page/r/CfmAgjrxwaTSEBM/review"
    },
    {
        "filename": "dealer-delaware.html",
        "name": "Delaware",
        "phone": "1-844-844-6638",
        "address": "",
        "latlon": "39.145324,-75.386594",
        "cid": "https://www.google.com/maps?cid=11044789483047204293",
        "facebook": "",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsDelaware",
        "website": "https://tigongolfcarts.com/delaware/",
        "pinterest": "",
        "review": "https://g.page/r/CcW1_1uE-UaZEBM/review"
    },
    {
        "filename": "dealer-virginia.html",
        "name": "Virginia",
        "phone": "1-844-844-6638",
        "address": "",
        "latlon": "37.5334624,-78.866703",
        "cid": "https://www.google.com/maps?cid=6737760967527982175",
        "facebook": "",
        "youtube": "https://www.youtube.com/@TigonGolfCartsVirginia",
        "website": "https://tigongolfcarts.com/virginia/",
        "pinterest": "",
        "review": "https://g.page/r/CV9k_9rmVYFdEBM/review"
    },
    {
        "filename": "dealer-north-carolina.html",
        "name": "North Carolina",
        "phone": "1-844-844-6638",
        "address": "",
        "latlon": "",
        "cid": "",
        "facebook": "",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsNorthCarolina",
        "website": "https://tigongolfcarts.com/north-carolina/",
        "pinterest": "",
        "review": ""
    },
    {
        "filename": "dealer-south-carolina.html",
        "name": "South Carolina",
        "phone": "1-844-844-6638",
        "address": "",
        "latlon": "",
        "cid": "",
        "facebook": "",
        "youtube": "",
        "website": "https://tigongolfcarts.com/south-carolina/",
        "pinterest": "",
        "review": ""
    },
    {
        "filename": "dealer-florida.html",
        "name": "Florida",
        "phone": "1-844-844-6638",
        "address": "",
        "latlon": "27.698638,-83.804601",
        "cid": "https://www.google.com/maps?cid=15821077580647342669",
        "facebook": "",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsFlorida",
        "website": "https://tigongolfcarts.com/florida/",
        "pinterest": "",
        "review": "https://g.page/r/CU2iYWY8wo_bEBM/review"
    },
    {
        "filename": "dealer-indiana.html",
        "name": "Indiana",
        "phone": "1-844-844-6638",
        "address": "",
        "latlon": "",
        "cid": "",
        "facebook": "",
        "youtube": "",
        "website": "https://tigongolfcarts.com/indiana/",
        "pinterest": "",
        "review": "https://g.page/r/CU_4NMYL3ORdEBM/review"
    },
    {
        "filename": "dealer-ohio.html",
        "name": "Ohio",
        "phone": "1-844-844-6638",
        "address": "",
        "latlon": "40.3633984,-82.669505",
        "cid": "https://www.google.com/maps?cid=7815966071951211924",
        "facebook": "",
        "youtube": "",
        "website": "https://tigongolfcarts.com/ohio/",
        "pinterest": "",
        "review": "https://g.page/r/CZQ9KE-743dsEBM/review"
    },
    {
        "filename": "dealer-maryland.html",
        "name": "Maryland",
        "phone": "1-844-844-6638",
        "address": "",
        "latlon": "",
        "cid": "",
        "facebook": "",
        "youtube": "https://www.youtube.com/@TIGONGolfCartsMaryland",
        "website": "https://tigongolfcarts.com/maryland/",
        "pinterest": "",
        "review": "https://g.page/r/CeRBOVZDpiHzEBM/review"
    },
    {
        "filename": "dealer-philadelphia.html",
        "name": "Philadelphia",
        "phone": "1-844-844-6638",
        "address": "",
        "latlon": "40.0024979,-75.1180146",
        "cid": "https://www.google.com/maps?cid=6103352888615501339",
        "facebook": "",
        "youtube": "",
        "website": "",
        "pinterest": "",
        "review": "https://g.page/r/CRv-x4Add7NUEBM/review"
    },
    {
        "filename": "dealer-new-york.html",
        "name": "New York",
        "phone": "1-844-844-6638",
        "address": "",
        "latlon": "",
        "cid": "",
        "facebook": "",
        "youtube": "",
        "website": "",
        "pinterest": "",
        "review": "https://g.page/r/Ca-zWbvWZcPcEBM/review"
    },
]

# Dealer H2s/content generator
def dealer_content(dealer):
    content = f'''
    <h2>Why Choose {dealer["name"]} for Your Medium Speed Vehicles?</h2>
    <p>
        {dealer["name"]} offers specialized sales and service for Medium Speed Vehicless (LSVs) and electric golf carts.
        Customers benefit from knowledgeable staff, convenient location, and a selection of street-legal vehicles for every lifestyle.
        Whether you need a new LSV for your neighborhood, business, or recreation, {dealer["name"]} delivers value and peace of mind.
    </p>
    <h2>Dealer Info & Contact</h2>
    <ul>
        <li><strong>Phone:</strong> {dealer["phone"] if dealer["phone"] else "Call for details"}</li>
        <li><strong>Address:</strong> {dealer["address"] if dealer["address"] else "Service Area: " + dealer["name"]}</li>
        {"<li><strong>Website:</strong> <a href='%s' target='_blank'>Visit Dealer Site</a></li>" % dealer["website"] if dealer["website"] else ""}
        {"<li><strong>Facebook:</strong> <a href='%s' target='_blank'>Facebook</a></li>" % dealer["facebook"] if dealer["facebook"] else ""}
        {"<li><strong>YouTube:</strong> <a href='%s' target='_blank'>YouTube</a></li>" % dealer["youtube"] if dealer["youtube"] else ""}
        {"<li><strong>Pinterest:</strong> <a href='%s' target='_blank'>Pinterest</a></li>" % dealer["pinterest"] if dealer["pinterest"] else ""}
    </ul>
    <h2>Medium Speed Vehicles Options</h2>
    <p>
        At {dealer["name"]}, we offer a variety of Medium Speed Vehicless to meet your specific needs:
    </p>
    <ul>
        <li><strong>Street Legal Golf Carts:</strong> Perfect for neighborhood transportation</li>
        <li><strong>Electric Utility Vehicles:</strong> Ideal for work sites and property maintenance</li>
        <li><strong>Personal Transportation Vehicles:</strong> Comfortable, efficient community travel</li>
        <li><strong>Custom LSVs:</strong> Tailored to your specific requirements</li>
    </ul>
    <h2>Benefits of Medium Speed Vehicless</h2>
    <p>
        Medium Speed Vehicless offer numerous advantages over traditional transportation options:
    </p>
    <ul>
        <li>Eco-friendly electric operation</li>
        <li>Lower operating costs than conventional vehicles</li>
        <li>Street-legal on roads with speed limits up to 35 mph</li>
        <li>Easy parking and maneuverability</li>
        <li>Reduced carbon footprint</li>
        <li>Community-friendly transportation</li>
    </ul>
    {"<h2>Visit Our Location</h2><p>Come visit our showroom at %s to see our selection of Medium Speed Vehicless and speak with our knowledgeable staff.</p>" % dealer["address"] if dealer["address"] else ""}
    {"<h2>Leave a Review</h2><p>Had a great experience? <a href='%s' target='_blank'>Leave us a review</a> to let others know!</p>" % dealer["review"] if dealer["review"] else ""}
    '''
    return content

# Generate HTML files
def generate_html_files():
    # Create index.html
    index_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LSV Dealer - Medium Speed Vehicles Dealers</title>
        <link rel="stylesheet" href="css/styles.css">
    </head>
    <body>
        <header>
            <div class="container">
                <h1>LSVDealer.com</h1>
                <p>Your Source for Medium Speed Vehicles Dealers Nationwide</p>
            </div>
        </header>
        
        <nav>
            <div class="container">
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="#about">About LSVs</a></li>
                    <li><a href="#dealers">Find Dealers</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </div>
        </nav>
        
        <main class="container">
            <section id="hero">
                <h2>Find Your Perfect Medium Speed Vehicles</h2>
                <p>Connect with authorized dealers specializing in street-legal golf carts and Medium Speed Vehicless.</p>
            </section>
            
            <section id="about">
                <h2>About Medium Speed Vehicless</h2>
                <p>Medium Speed Vehicless (LSVs) are electric vehicles that can travel at speeds of 20-25 mph. They are street legal on roads with posted speed limits of 35 mph or less in most states. LSVs offer an eco-friendly, cost-effective transportation alternative for neighborhoods, planned communities, campuses, and small towns.</p>
                <p>All street-legal LSVs include required safety features such as headlights, turn signals, mirrors, windshield, seat belts, and more. They provide convenient transportation with lower operating costs than traditional vehicles.</p>
            </section>
            
            <section id="dealers">
                <h2>Our Dealer Network</h2>
                <p>Find a Medium Speed Vehicles dealer near you:</p>
                
                <div class="dealer-grid">
    '''
    
    # Add dealer cards to index.html
    for dealer in dealers:
        dealer_card = f'''
                    <div class="dealer-card">
                        <h3>{dealer["name"]}</h3>
                        <p>{dealer["address"] if dealer["address"] else "Service Area: " + dealer["name"]}</p>
                        <p>{dealer["phone"] if dealer["phone"] else ""}</p>
                        <a href="{dealer["filename"]}" class="btn">View Dealer</a>
                    </div>
        '''
        index_html += dealer_card
    
    # Complete index.html
    index_html += '''
                </div>
            </section>
            
            <section id="contact">
                <h2>Contact Us</h2>
                <p>For general inquiries about our dealer network:</p>
                <p>Email: info@lsvdealer.com</p>
                <p>Phone: 1-800-LSV-DEAL</p>
            </section>
        </main>
        
        <footer>
            <div class="container">
                <p>&copy; 2025 LSVDealer.com - All Rights Reserved</p>
            </div>
        </footer>
    </body>
    </html>
    '''
    
    # Write index.html
    with open('index.html', 'w') as f:
        f.write(index_html)
    
    # Generate individual dealer pages
    for dealer in dealers:
        dealer_html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{dealer["name"]} - Medium Speed Vehicles Dealer | LSVDealer.com</title>
            <link rel="stylesheet" href="css/styles.css">
        </head>
        <body>
            <header>
                <div class="container">
                    <h1>LSVDealer.com</h1>
                    <p>Your Source for Medium Speed Vehicles Dealers Nationwide</p>
                </div>
            </header>
            
            <nav>
                <div class="container">
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="index.html#about">About LSVs</a></li>
                        <li><a href="index.html#dealers">Find Dealers</a></li>
                        <li><a href="index.html#contact">Contact</a></li>
                    </ul>
                </div>
            </nav>
            
            <main class="container">
                <section class="dealer-header">
                    <h1>{dealer["name"]}</h1>
                    <p class="subtitle">Medium Speed Vehicles Dealer</p>
                    {f'<a href="{dealer["cid"]}" target="_blank" class="map-link">View on Google Maps</a>' if dealer["cid"] else ""}
                </section>
                
                <section class="dealer-content">
                    {dealer_content(dealer)}
                </section>
                
                <section class="back-link">
                    <a href="index.html#dealers">&larr; Back to All Dealers</a>
                </section>
            </main>
            
            <footer>
                <div class="container">
                    <p>&copy; 2025 LSVDealer.com - All Rights Reserved</p>
                </div>
            </footer>
        </body>
        </html>
        '''
        
        # Write dealer page
        with open(f'{dealer["filename"]}', 'w') as f:
            f.write(dealer_html)

# Call the function to generate HTML files
if __name__ == "__main__":
    generate_html_files()
