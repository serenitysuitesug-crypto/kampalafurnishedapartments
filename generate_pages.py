#!/usr/bin/env python3
import json
import os
import re

# Read apartment data
with open('data/apartments.json', 'r') as f:
    apartments = json.load(f)

# Create apartments directory if it doesn't exist
os.makedirs('apartments', exist_ok=True)

# HTML template for apartment pages
template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title} - Furnished Apartments Uganda</title>
    <meta name="description" content="{description}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        .apartment-hero {{ background: #f8f9fa; padding: 3rem 0; }}
        .price-badge {{ font-size: 1.5rem; color: #198754; }}
        .amenity-list {{ list-style: none; padding-left: 0; }}
        .amenity-list li {{ padding: 5px 0; }}
        .back-to-home {{ margin-top: 2rem; }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">Furnished Apartments Uganda</a>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-lg-8">
                <h1 class="mb-3">{title}</h1>
                <div class="d-flex align-items-center mb-4">
                    <span class="badge bg-primary me-3">{location}</span>
                    <span class="price-badge fw-bold">{price}</span>
                </div>
                
                <div class="mb-5">
                    <img src="../{main_image}" alt="{title} in {location}" class="img-fluid rounded" loading="lazy">
                </div>
                
                <h3 class="mb-3">Description</h3>
                <p class="mb-4">{full_description}</p>
                
                <h3 class="mb-3">Amenities & Services</h3>
                <ul class="amenity-list">
                    {amenities}
                </ul>
                
                <div class="card mt-4">
                    <div class="card-body text-center">
                        <h4 class="card-title">Book This Apartment</h4>
                        <p class="card-text">Contact us directly for availability and booking</p>
                        <a href="tel:+256778663411" class="btn btn-success btn-lg me-2">
                            <i class="bi bi-telephone"></i> Call Now
                        </a>
                        <a href="https://wa.me/256704229100?text=Hello! I'm interested in {whatsapp_text}" 
                           class="btn btn-whatsapp btn-lg" 
                           style="background-color: #25D366; color: white;">
                            <i class="bi bi-whatsapp"></i> WhatsApp
                        </a>
                    </div>
                </div>
            </div>
            
            <div class="col-lg-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Quick Details</h5>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item"><strong>Location:</strong> {location}</li>
                            <li class="list-group-item"><strong>Price:</strong> {price}</li>
                            <li class="list-group-item"><strong>Type:</strong> {type}</li>
                            <li class="list-group-item"><strong>Available:</strong> Yes</li>
                        </ul>
                    </div>
                </div>
                
                <div class="card mt-4">
                    <div class="card-body">
                        <h5 class="card-title">Gallery</h5>
                        <div class="row">
                            {gallery_images}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="back-to-home text-center mt-5">
            <a href="/" class="btn btn-outline-primary">
                ← View All Apartments
            </a>
        </div>
    </div>
    
    <footer class="bg-dark text-white mt-5 py-4">
        <div class="container text-center">
            <p>&copy; {year} Furnished Apartments Uganda. All rights reserved.</p>
            <p>Contact: +256778663411 | +256704229100</p>
        </div>
    </footer>
</body>
</html>
'''

for i, apt in enumerate(apartments):
    # Create URL-friendly slug
    slug = re.sub(r'[^\w\s-]', '', apt.get('title', f'apartment-{i}')).lower().replace(' ', '-')
    
    # Generate amenities list
    amenities = ''.join([f'<li>✅ {service}</li>' for service in apt.get('services', [])])
    
    # Generate gallery images
    gallery_html = ''
    for img in apt.get('gallery', []):
        gallery_html += f'''
        <div class="col-6 mb-2">
            <img src="../{img}" class="img-thumbnail" alt="Apartment image" loading="lazy">
        </div>'''
    
    # Fill template
    html_content = template.format(
        title=apt.get('title', 'Apartment'),
        location=apt.get('location', 'Kampala'),
        price=apt.get('price', 'Contact for price'),
        main_image=apt.get('image', ''),
        amenities=amenities,
        gallery_images=gallery_html,
        type=apt.get('title', '').split()[0] if ' ' in apt.get('title', '') else apt.get('title', ''),
        whatsapp_text=f"the {apt.get('title', '')} in {apt.get('location', '')}",
        full_description=f"A beautiful {apt.get('title', 'apartment').lower()} located in {apt.get('location', 'Kampala')}. Fully furnished with modern amenities including {', '.join(apt.get('services', ['WiFi', 'kitchen', 'security']))}. Perfect for short or long stays in Kampala.",
        description=f"Book {apt.get('title', 'apartment')} in {apt.get('location', 'Kampala')}. {apt.get('price', 'Affordable rates')}. Fully furnished with {', '.join(apt.get('services', ['WiFi', 'kitchen', 'security']))}. Contact for availability.",
        year=2024
    )
    
    # Write to file
    with open(f'apartments/{slug}.html', 'w') as f:
        f.write(html_content)
    
    print(f"Created: apartments/{slug}.html")

print(f"\nGenerated {len(apartments)} apartment pages!")
print("\nNext steps:")
print("1. Upload these HTML files to your server")
print("2. Update your sitemap.xml")
print("3. Add internal links from homepage")
