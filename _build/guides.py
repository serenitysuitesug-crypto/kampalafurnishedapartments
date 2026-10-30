"""
Travel guide articles. Each guide becomes a page at /guides/<slug>/.

Body text is HTML. Placeholders in {curly braces} are filled in by build.py
from the live apartment data, so prices stay correct when apartments change:
  {ntinda_from} {kisaasi_from} {ntinda_count} {kisaasi_count}
  {whatsapp_link} {call} {checkin} {checkout} {weekly_off} {monthly_off} {pickup_price}
To add a guide, copy one of the dictionaries below and change its fields.
"""

GUIDES = [
    {
        "slug": "entebbe-airport-to-ntinda",
        "title": "Getting from Entebbe Airport to Ntinda, Kampala",
        "seo_title": "Entebbe Airport to Ntinda: Taxi, Uber, Time and Cost",
        "description": "How to get from Entebbe International Airport to Ntinda, Kampala: taxi, Uber, pre-booked transfers, expressway tolls, travel time and arrival tips.",
        "summary": "Taxis, Uber, pre-booked transfers, expressway tolls and how long the drive really takes.",
        "updated": "2026-10-30",
        "icon": "bi-airplane",
        "area": "Ntinda",
        "body": """
<p class="lead">Entebbe International Airport is Uganda's main airport, about 40 km from Ntinda by road. Most guests reach our apartments in <strong>roughly 1 to 1.5 hours</strong>, but the drive can take longer in Kampala's rush-hour traffic. Here's how to plan the trip.</p>

<h2>The quick answer</h2>
<ul>
  <li><strong>Distance:</strong> about 40–45 km by road</li>
  <li><strong>Travel time:</strong> around 1 to 1.5 hours; allow up to 2 hours on weekday mornings and evenings</li>
  <li><strong>Easiest option:</strong> our airport pickup ({pickup_price}), an airport taxi or an Uber</li>
  <li><strong>Expressway toll:</strong> UGX 5,000 per car, paid in cash (Ugandan shillings only) at the toll plaza</li>
</ul>

<h2>Your transport options</h2>

<h3>1. Book an airport pickup with us</h3>
<p>If you're staying with us, the simplest option is our airport pickup for <strong>{pickup_price}</strong> per trip. Send us your flight number and arrival time on <a href="{whatsapp_link}">WhatsApp</a> and we'll arrange a driver to meet you at arrivals and bring you straight to your apartment. It's the least stressful choice after a long flight, especially if you land at night.</p>

<h3>2. Uber</h3>
<p>Uber operates at Entebbe Airport, and ride-hailing apps are widely used across Kampala. Open the app once you have mobile data or the airport WiFi, check the fare estimate, and follow the in-app directions to the pickup point. Fares change with demand and traffic, so compare the estimate before you confirm.</p>

<h3>3. Airport taxi</h3>
<p>Licensed taxis wait outside the arrivals hall. Agree the full fare to Ntinda <em>before</em> you get in, and confirm whether it includes the expressway toll. Having the price settled up front avoids surprises at the end of the trip.</p>

<h3>4. Pre-booked transfer</h3>
<p>Several online transfer companies let you book a car in advance with a fixed price, which is useful for groups or travellers with lots of luggage. These usually cost more than a local taxi, but the price and the driver are confirmed before you fly.</p>

<h3>5. Public transport (budget option)</h3>
<p>It's possible to reach Ntinda by shared minibus taxis, changing in central Kampala, but it's slow, can take close to 3 hours with connections, and isn't practical with suitcases. We don't recommend it for your arrival day.</p>

<h2>The route</h2>
<p>Most drivers take the <strong>Kampala–Entebbe Expressway</strong>, a toll road of about 51 km that bypasses the busy old Entebbe Road. From the Kampala end, drivers continue to Ntinda either through the city or along the <strong>Kampala Northern Bypass</strong>, depending on traffic. The expressway is the quickest part of the journey; most of the variation in travel time comes from traffic inside Kampala.</p>

<h2>Tips for arriving at Entebbe</h2>
<ul>
  <li><strong>Carry some Ugandan shillings.</strong> The expressway toll is cash-only in shillings, and small notes are handy for tips and snacks. You'll find ATMs and currency exchange at the airport.</li>
  <li><strong>Get a local SIM card.</strong> Mobile network kiosks are available at the airport, and a local SIM makes Uber, WhatsApp and maps easy to use.</li>
  <li><strong>Avoid rush hour if you can.</strong> Weekday mornings and late afternoons are the slowest times to cross Kampala.</li>
  <li><strong>Share your arrival time with your host.</strong> We'll make sure the apartment is ready. Check-in is from {checkin}, and if you land early we'll do our best to help.</li>
</ul>

<h2>Where to stay in Ntinda</h2>
<p>We have {ntinda_count} fully furnished apartments in Ntinda, from <strong>{ntinda_from} per night</strong>, each with free WiFi and a kitchen. Stay a week or longer and you get {weekly_off}% off (7+ nights) or {monthly_off}% off (30+ nights).</p>
""",
        "faqs": [
            ("How long does it take to get from Entebbe Airport to Ntinda?",
             "Usually around 1 to 1.5 hours by car. Allow up to 2 hours during weekday morning and evening rush hours."),
            ("How much is the Entebbe Expressway toll?",
             "UGX 5,000 per car for a one-way trip, paid in cash in Ugandan shillings at the toll plaza. Rates can change, so carry a little extra."),
            ("Does Uber work at Entebbe Airport?",
             "Yes. Uber operates pickups at Entebbe International Airport. Check the app for the current fare estimate and pickup point."),
            ("Can you arrange an airport pickup?",
             "Yes. Our airport pickup costs {pickup_price} per trip. Send your flight number and arrival time on WhatsApp and we'll arrange a driver to meet you at arrivals."),
        ],
    },
    {
        "slug": "where-to-stay-in-kampala-ntinda-vs-kisaasi",
        "title": "Where to Stay in Kampala: Ntinda vs Kisaasi",
        "seo_title": "Where to Stay in Kampala: Ntinda vs Kisaasi Compared",
        "description": "Ntinda or Kisaasi? Compare two of north-east Kampala's best neighbourhoods for short and long stays: atmosphere, amenities, getting around and apartment prices.",
        "summary": "Two popular north-east Kampala neighbourhoods compared: atmosphere, amenities, getting around and prices.",
        "updated": "2026-10-30",
        "icon": "bi-signpost-split",
        "area": None,
        "body": """
<p class="lead">If you're looking for a furnished apartment in Kampala, Ntinda and Kisaasi often come up together. They're neighbours in north-east Kampala and both make a comfortable base, but they feel quite different. Here's how to choose.</p>

<h2>At a glance</h2>
<div class="table-responsive">
<table class="table compare">
  <thead><tr><th></th><th>Ntinda</th><th>Kisaasi</th></tr></thead>
  <tbody>
    <tr><th>Feel</th><td>Busy, lively suburb with everything nearby</td><td>Calmer, more residential and growing</td></tr>
    <tr><th>Best for</th><td>Business travellers, first-time visitors, short stays</td><td>Families, longer stays, guests who want quiet</td></tr>
    <tr><th>Shops and restaurants</th><td>Many within walking distance</td><td>Along the main roads, a short ride away</td></tr>
    <tr><th>Getting around</th><td>Very easy: taxis, boda bodas and ride-hailing everywhere</td><td>Easy by car or ride-hailing; a little further from the busiest areas</td></tr>
    <tr><th>Our apartments</th><td>{ntinda_count} apartments, from {ntinda_from}/night</td><td>{kisaasi_count} apartments, from {kisaasi_from}/night</td></tr>
  </tbody>
</table>
</div>

<h2>Ntinda: convenient and connected</h2>
<p>Ntinda is one of Kampala's busiest and best-connected suburbs, in Nakawa Division about 7 km north-east of the city centre. Supermarkets, cafés, restaurants, banks and pharmacies are all close, so daily errands are easy, and transport is never hard to find.</p>
<p><strong>Choose Ntinda if</strong> you want convenience: you're here for work in north-east Kampala, it's your first visit, or you'd like to walk to shops and places to eat. Ntinda also links easily to Bukoto, Naguru, Kiwatule and Kisaasi.</p>
<p><a href="/furnished-apartments-ntinda/">See our furnished apartments in Ntinda</a></p>

<h2>Kisaasi: calmer and more residential</h2>
<p>Kisaasi sits just north of Ntinda, between Bukoto, Kyanja and Kulambiro. It's quieter and more residential, while still having shops, supermarkets and restaurants along its main roads. Many guests find it more relaxed, especially at night.</p>
<p><strong>Choose Kisaasi if</strong> you value peace and space: you're travelling with family, staying for weeks or months, working remotely, or you simply prefer a calmer neighbourhood that's still close to everything Ntinda offers.</p>
<p><a href="/furnished-apartments-kisaasi/">See our furnished apartments in Kisaasi</a></p>

<h2>Getting around from either area</h2>
<p>Both neighbourhoods are well served by ride-hailing apps such as Uber and Bolt, by boda bodas (motorbike taxis) and by shared minibus taxis. The Kampala Northern Bypass is close to both, which helps for trips across the city. Travel time to the city centre depends far more on traffic than on distance, so allow extra time at rush hour. Entebbe International Airport is roughly 1 to 1.5 hours away by road from either area; see our <a href="/guides/entebbe-airport-to-ntinda/">airport transfer guide</a>.</p>

<h2>Still deciding?</h2>
<p>Tell us what your trip looks like (dates, who's coming and what matters most) on <a href="{whatsapp_link}">WhatsApp</a>, and we'll suggest the apartment that fits best. Whichever area you choose, every apartment has free WiFi and a kitchen, and longer stays get {weekly_off}% off weekly and {monthly_off}% off monthly.</p>
""",
        "faqs": [
            ("Is Ntinda or Kisaasi better for a short stay?",
             "Ntinda is usually better for short stays and business trips because shops, restaurants and transport are all close by. Kisaasi suits longer stays and guests who prefer a quieter area."),
            ("Are Ntinda and Kisaasi close to each other?",
             "Yes. They're neighbouring areas in north-east Kampala, a short drive apart, so you can easily enjoy both."),
            ("Which area is cheaper?",
             "Prices depend more on the apartment than the area. Our apartments start from {ntinda_from} per night in Ntinda and {kisaasi_from} per night in Kisaasi."),
        ],
    },
]
