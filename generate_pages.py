#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime

# Read apartment data
with open('data/apartments.json', 'r') as f:
    apartments = json.load(f)

print(f"Found {len(apartments)} apartments in JSON")

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
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f6fa; }}
        .apartment-hero {{ background: #f8f9fa; padding: 3rem 0; }}
        .price-badge {{ font-size: 1.5rem; color: #198754; font-weight: bold; }}
        .amenity-list {{ list-style: none; padding-left: 0; }}
        .amenity-list li {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
        .back-to-home {{ margin-top: 2rem; }}
        .gallery-img {{ height: 150px; object-fit: cover; cursor: pointer; }}
        .gallery-img:hover {{ opacity: 0.8; }}
    </style>
</head>
<body>
    <!-- Simple Header -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <div class="rounded-circle bg-white text-primary d-inline-flex align-items-center justify-content-center" 
                     style="width:40px; height:40px; font-size:1rem; font-weight:700; margin-right:10px;">
                    FA
                </div>
                Furnished Apartments Uganda
            </a>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-lg-8">
                <h1 class="mb-3 fw-bold">{title}</h1>
                <div class="d-flex align-items-center mb-4">
                    <span class="badge bg-primary me-3 fs-6">{location}</span>
                    <span class="price-badge">{price}</span>
                </div>
                
                <!-- Main Image -->
                <div class="mb-4">
                    <img src="../{main_image}" alt="{title} in {location}, Kampala" 
                         class="img-fluid rounded shadow" loading="lazy" style="max-height: 500px; width: 100%; object-fit: cover;">
                </div>
                
                <!-- Description -->
                <div class="card mb-4">
                    <div class="card-body">
                        <h3 class="card-title mb-3">About This Apartment</h3>
                        <p class="card-text">{full_description}</p>
                    </div>
                </div>
                
                <!-- Amenities -->
                <div class="card mb-4">
                    <div class="card-body">
                        <h3 class="card-title mb-3">Amenities & Services</h3>
                        <ul class="amenity-list">
                            {amenities}
                        </ul>
                    </div>
                </div>
                
                <!-- Booking CTA -->
                <div class="card mb-4 border-success">
                    <div class="card-body text-center bg-light">
                        <h4 class="card-title text-success">Ready to Book?</h4>
                        <p class="card-text">Contact us directly for availability and best rates</p>
                        <div class="d-flex flex-column flex-md-row justify-content-center gap-3">
                            <a href="tel:+256778663411" class="btn btn-primary btn-lg">
                                <i class="bi bi-telephone"></i> Call +256 778 663411
                            </a>
                            <a href="https://wa.me/256704229100?text=Hello! I'm interested in {whatsapp_text}" 
                               class="btn btn-success btn-lg">
                                <i class="bi bi-whatsapp"></i> WhatsApp Now
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Sidebar -->
            <div class="col-lg-4">
                <!-- Quick Details -->
                <div class="card shadow mb-4">
                    <div class="card-body">
                        <h5 class="card-title mb-3"><i class="bi bi-info-circle"></i> Quick Details</h5>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item d-flex justify-content-between">
                                <span><strong>Location:</strong></span>
                                <span>{location}</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between">
                                <span><strong>Price:</strong></span>
                                <span class="fw-bold text-success">{price}</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between">
                                <span><strong>Type:</strong></span>
                                <span>{type}</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between">
                                <span><strong>Status:</strong></span>
                                <span class="badge bg-success">Available</span>
                            </li>
                        </ul>
                    </div>
                </div>
                
                <!-- Gallery -->
                <div class="card shadow">
                    <div class="card-body">
                        <h5 class="card-title mb-3"><i class="bi bi-images"></i> Gallery</h5>
                        <div class="row g-2">
                            {gallery_images}
                        </div>
                    </div>
                </div>
                
                <!-- Other Apartments -->
                <div class="card shadow mt-4">
                    <div class="card-body">
                        <h5 class="card-title mb-3"><i class="bi bi-house-door"></i> View Other Apartments</h5>
                        <p>Browse our full selection of furnished apartments in Kampala</p>
                        <a href="/" class="btn btn-outline-primary w-100">
                            View All Apartments
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Footer -->
    <footer class="bg-dark text-white mt-5 py-4">
        <div class="container">
            <div class="row">
                <div class="col-md-6 text-center text-md-start">
                    <h5>Furnished Apartments Uganda</h5>
                    <p>Modern, secure, fully furnished apartments in Kampala</p>
                </div>
                <div class="col-md-6 text-center text-md-end">
                    <p><i class="bi bi-telephone"></i> +256 778 663411 | +256 704 229100</p>
                    <p><i class="bi bi-whatsapp"></i> WhatsApp: +256 704 229100</p>
                </div>
            </div>
            <div class="text-center mt-3 pt-3 border-top border-secondary">
                <p class="mb-0">&copy; {year} Furnished Apartments Uganda. All rights reserved.</p>
            </div>
        </div>
    </footer>
    
    <!-- Simple Image Modal for Gallery -->
    <script>
    function openImage(src) {{
        window.open(src, '_blank');
    }}
    </script>
</body>
</html>
'''

# Generate sitemap entries
sitemap_entries = []
today = datetime.now().strftime('%Y-%m-%d')

for i, apt in enumerate(apartments):
    print(f"Processing apartment {i+1}: {apt.get('title', 'Unknown')}")
    
    # Create URL-friendly slug
    slug = re.sub(r'[^\w\s-]', '', apt.get('title', f'apartment-{i}')).lower().replace(' ', '-')
    
    # Get main image - use first image in gallery if no main image specified
    main_image = apt.get('image', '')
    if not main_image and 'gallery' in apt and len(apt['gallery']) > 0:
        main_image = apt['gallery'][0]
    
    # Generate amenities list
    amenities = ''.join([f'<li><i class="bi bi-check-circle text-success me-2"></i> {service}</li>' 
                         for service in apt.get('services', ['WiFi', 'Fully Furnished', 'Kitchen', 'Security', 'Hot Water'])])
    
    # Generate gallery images HTML
    gallery_images = ''
    gallery = apt.get('gallery', [])
    for img in gallery[:6]:  # Show max 6 images in gallery
        gallery_images += f'''
        <div class="col-4 col-md-6">
            <img src="../{img}" class="img-fluid rounded gallery-img" 
                 alt="{apt.get('title')} image" 
                 onclick="openImage('../{img}')">
        </div>'''
    
    # If no gallery images, use main image
    if not gallery_images and main_image:
        gallery_images = f'''
        <div class="col-12">
            <img src="../{main_image}" class="img-fluid rounded" 
                 alt="{apt.get('title')}">
        </div>'''
    
    # Determine apartment type from title
    title = apt.get('title', 'Apartment')
    if 'studio' in title.lower():
        apt_type = 'Studio'
    elif '1' in title or 'one' in title.lower():
        apt_type = '1 Bedroom'
    elif '2' in title or 'two' in title.lower():
        apt_type = '2 Bedrooms'
    elif '3' in title or 'three' in title.lower():
        apt_type = '3 Bedrooms'
    else:
        apt_type = title.split()[0] if ' ' in title else title
    
    # Fill template
    html_content = template.format(
        title=title,
        location=apt.get('location', 'Kampala'),
        price=apt.get('price', 'Contact for pricing'),
        main_image=main_image,
        amenities=amenities,
        gallery_images=gallery_images,
        type=apt_type,
        whatsapp_text=f"the {title} in {apt.get('location', 'Kampala')}",
        full_description=f"A beautiful {title.lower()} located in {apt.get('location', 'Kampala')}, Kampala. This fully furnished apartment comes with modern amenities and is perfect for both short-term and long-term stays. Features include {', '.join(apt.get('services', ['high-speed WiFi', 'fully equipped kitchen', '24/7 security', 'hot water']))}. Ideal for tourists, business travelers, or relocating professionals.",
        description=f"Book {title} in {apt.get('location', 'Kampala')}, Kampala. {apt.get('price', 'Competitive rates')}. Fully furnished with amenities. Contact for availability and booking.",
        year=datetime.now().year
    )
    
    # Write to file
    filename = f'apartments/{slug}.html'
    with open(filename, 'w') as f:
        f.write(html_content)
    
    print(f"  Created: {filename}")
    
    # Add to sitemap
    sitemap_entries.append(f'''  <url>
    <loc>https://yourdomain.com/apartments/{slug}.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>''')

print(f"\nGenerated {len(apartments)} apartment pages!")

# Generate sitemap.xml
sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yourdomain.com/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
{chr(10).join(sitemap_entries)}
</urlset>'''

with open('sitemap.xml', 'w') as f:
    f.write(sitemap_content)

print(f"Generated sitemap.xml with {len(sitemap_entries) + 1} URLs")

# Generate robots.txt
robots_content = '''User-agent: *
Allow: /
Disallow: /data/
Sitemap: https://yourdomain.com/sitemap.xml

# Crawl-delay: 10
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /'''

with open('robots.txt', 'w') as f:
    f.write(robots_content)

print("Generated robots.txt")
print("\n🎉 Phase 1 Complete! Next steps:")
print("1. Upload ALL files to your server")
print("2. Replace 'yourdomain.com' in sitemap.xml with your actual domain")
print("3. Submit sitemap to Google Search Console")
print("4. Test that links work: /apartments/apartment-a.html")
