from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Seed the database with famous listings across categories"

    def handle(self, *args, **kwargs):
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("❌ No users found. Please create a user first."))
            return

        # Delete old listings
        Listing.objects.all().delete()

        # All 28 listings
        listings = [
            # 1
            {
                "title": "Cozy Beachfront Cottage",
                "description": "Escape to this charming beachfront cottage for a relaxing getaway. Enjoy stunning ocean views and easy access to the beach.",
                "image_url": "https://images.unsplash.com/photo-1552733407-5d5c46c3bb3b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 1500,
                "location": "Malibu",
                "country": "United States",
                "category": "Hot Beaches",
                "geometry": {"type":"Point","coordinates":[-118.7798, 34.0259]}
            },
            # 2
            {
                "title": "Modern Loft in Downtown",
                "description": "Stay in the heart of the city in this stylish loft apartment. Perfect for urban explorers!",
                "image_url": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 1200,
                "location": "New York City",
                "country": "United States",
                "category": "Trending",
                "geometry": {"type":"Point","coordinates":[-74.006,40.7128]}
            },
            # 3
            {
                "title": "Mountain Retreat",
                "description": "Unplug and unwind in this peaceful mountain cabin. Surrounded by nature, it's a perfect place to recharge.",
                "image_url": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 1000,
                "location": "Aspen",
                "country": "United States",
                "category": "Mountains",
                "geometry": {"type":"Point","coordinates":[-106.8175,39.1911]}
            },
            # 4
            {
                "title": "Historic Villa in Tuscany",
                "description": "Experience the charm of Tuscany in this beautifully restored villa. Explore the rolling hills and vineyards.",
                "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 2500,
                "location": "Florence",
                "country": "Italy",
                "category": "Castles",
                "geometry": {"type":"Point","coordinates":[11.2558,43.7696]}
            },
            # 5
            {
                "title": "Secluded Treehouse Getaway",
                "description": "Live among the treetops in this unique treehouse retreat. A true nature lover's paradise.",
                "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 800,
                "location": "Portland",
                "country": "United States",
                "category": "Camping",
                "geometry": {"type":"Point","coordinates":[-122.6765,45.5231]}
            },
            # 6
            {
                "title": "Beachfront Paradise",
                "description": "Step out of your door onto the sandy beach. This beachfront condo offers the ultimate relaxation.",
                "image_url": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 2000,
                "location": "Cancun",
                "country": "Mexico",
                "category": "Hot Beaches",
                "geometry": {"type":"Point","coordinates":[-86.8475,21.1619]}
            },
            # 7
            {
                "title": "Rustic Cabin by the Lake",
                "description": "Spend your days fishing and kayaking on the serene lake. This cozy cabin is perfect for outdoor enthusiasts.",
                "image_url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 900,
                "location": "Lake Tahoe",
                "country": "United States",
                "category": "Mountains",
                "geometry": {"type":"Point","coordinates":[-120.037,39.0968]}
            },
            # 8
            {
                "title": "Luxury Penthouse with City Views",
                "description": "Indulge in luxury living with panoramic city views from this stunning penthouse apartment.",
                "image_url": "https://images.unsplash.com/photo-1622396481328-9b1b78cdd9fd?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 3500,
                "location": "Los Angeles",
                "country": "United States",
                "category": "Trending",
                "geometry": {"type":"Point","coordinates":[-118.2437,34.0522]}
            },
            # 9
            {
                "title": "Ski-In/Ski-Out Chalet",
                "description": "Hit the slopes right from your doorstep in this ski-in/ski-out chalet in the Swiss Alps.",
                "image_url": "https://images.unsplash.com/photo-1502784444187-359ac186c5bb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 3000,
                "location": "Verbier",
                "country": "Switzerland",
                "category": "Mountains",
                "geometry": {"type":"Point","coordinates":[7.227,46.096]}
            },
            # 10
            {
                "title": "Safari Lodge in the Serengeti",
                "description": "Experience the thrill of the wild in a comfortable safari lodge. Witness the Great Migration up close.",
                "image_url": "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 4000,
                "location": "Serengeti National Park",
                "country": "Tanzania",
                "category": "Farms",
                "geometry": {"type":"Point","coordinates":[34.832, -2.333]}
            },
            # 11
            {
                "title": "Historic Canal House",
                "description": "Stay in a piece of history in this beautifully preserved canal house in Amsterdam's iconic district.",
                "image_url": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 1800,
                "location": "Amsterdam",
                "country": "Netherlands",
                "category": "Iconic Cities",
                "geometry": {"type":"Point","coordinates":[4.8952,52.3702]}
            },
            # 12
            {
                "title": "Private Island Retreat",
                "description": "Have an entire island to yourself for a truly exclusive and unforgettable vacation experience.",
                "image_url": "https://images.unsplash.com/photo-1618140052121-39fc6db33972?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 10000,
                "location": "Fiji",
                "country": "Fiji",
                "category": "Islands",
                "geometry": {"type":"Point","coordinates":[178.065, -17.7134]}
            },
            # 13
            {
                "title": "Charming Cottage in the Cotswolds",
                "description": "Escape to the picturesque Cotswolds in this quaint and charming cottage with a thatched roof.",
                "image_url": "https://images.unsplash.com/photo-1602088113235-229c19758e9f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 1200,
                "location": "Cotswolds",
                "country": "United Kingdom",
                "category": "Rooms",
                "geometry": {"type":"Point","coordinates":[-1.958,51.833]}
            },
            # 14
            {
                "title": "Historic Brownstone in Boston",
                "description": "Step back in time in this elegant historic brownstone located in the heart of Boston.",
                "image_url": "https://images.unsplash.com/photo-1533619239233-6280475a633a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 2200,
                "location": "Boston",
                "country": "United States",
                "category": "Trending",
                "geometry": {"type":"Point","coordinates":[-71.0589,42.3601]}
            },
            # 15
            {
                "title": "Beachfront Bungalow in Bali",
                "description": "Relax on the sandy shores of Bali in this beautiful beachfront bungalow with a private pool.",
                "image_url": "https://images.unsplash.com/photo-1602391833977-358a52198938?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 1800,
                "location": "Bali",
                "country": "Indonesia",
                "category": "Hot Beaches",
                "geometry": {"type":"Point","coordinates":[115.1889,-8.4095]}
            },
            # 16
            {
                "title": "Mountain View Cabin in Banff",
                "description": "Enjoy breathtaking mountain views from this cozy cabin in the Canadian Rockies.",
                "image_url": "https://images.unsplash.com/photo-1521401830884-6c03c1c87ebb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 1500,
                "location": "Banff",
                "country": "Canada",
                "category": "Mountains",
                "geometry": {"type":"Point","coordinates":[-115.572,51.1784]}
            },
            # 17
            {
                "title": "Art Deco Apartment in Miami",
                "description": "Step into the glamour of the 1920s in this stylish Art Deco apartment in South Beach.",
                "image_url": "https://plus.unsplash.com/premium_photo-1670963964797-942df1804579?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 1600,
                "location": "Miami",
                "country": "United States",
                "category": "Trending",
                "geometry": {"type":"Point","coordinates":[-80.1918,25.7617]}
            },
            # 18
            {
                "title": "Tropical Villa in Phuket",
                "description": "Escape to a tropical paradise in this luxurious villa with a private infinity pool in Phuket.",
                "image_url": "https://images.unsplash.com/photo-1470165301023-58dab8118cc9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 3000,
                "location": "Phuket",
                "country": "Thailand",
                "category": "Pools",
                "geometry": {"type":"Point","coordinates":[98.3933,7.8804]}
            },
            # 19
            {
                "title": "Historic Castle in Scotland",
                "description": "Live like royalty in this historic castle in the Scottish Highlands. Explore the rugged beauty of the area.",
                "image_url": "https://images.unsplash.com/photo-1585543805890-6051f7829f98?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 4000,
                "location": "Scottish Highlands",
                "country": "United Kingdom",
                "category": "Castles",
                "geometry": {"type":"Point","coordinates":[-3.1721,56.4907]}
            },
            # 20
            {
                "title": "Desert Oasis in Dubai",
                "description": "Experience luxury in the middle of the desert in this opulent oasis in Dubai with a private pool.",
                "image_url": "https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 5000,
                "location": "Dubai",
                "country": "United Arab Emirates",
                "category": "Pools",
                "geometry": {"type":"Point","coordinates":[55.2708,25.2048]}
            },
            # 21
            {
                "title": "Rustic Log Cabin in Montana",
                "description": "Unplug and unwind in this cozy log cabin surrounded by the natural beauty of Montana.",
                "image_url": "https://images.unsplash.com/photo-1586375300773-8384e3e4916f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 1100,
                "location": "Montana",
                "country": "United States",
                "category": "Mountains",
                "geometry": {"type":"Point","coordinates":[-110.3626,46.8797]}
            },
            # 22
            {
                "title": "Beachfront Villa in Greece",
                "description": "Enjoy the crystal-clear waters of the Mediterranean in this beautiful beachfront villa on a Greek island.",
                "image_url": "https://images.unsplash.com/photo-1602343168117-bb8ffe3e2e9f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 2500,
                "location": "Mykonos",
                "country": "Greece",
                "category": "Hot Beaches",
                "geometry": {"type":"Point","coordinates":[25.3333,37.4467]}
            },
            # 23
            {
                "title": "Eco-Friendly Treehouse Retreat",
                "description": "Stay in an eco-friendly treehouse nestled in the forest. It's the perfect escape for nature lovers.",
                "image_url": "https://images.unsplash.com/photo-1488462237308-ecaa28b729d7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 750,
                "location": "Costa Rica",
                "country": "Costa Rica",
                "category": "Camping",
                "geometry": {"type":"Point","coordinates":[-84.0907,10.5931]}
            },
            # 24
            {
                "title": "Historic Cottage in Charleston",
                "description": "Experience the charm of historic Charleston in this beautifully restored cottage with a private garden.",
                "image_url": "https://images.unsplash.com/photo-1587381420270-3e1a5b9e6904?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 1600,
                "location": "Charleston",
                "country": "United States",
                "category": "Rooms",
                "geometry": {"type":"Point","coordinates":[-79.9311,32.7765]}
            },
            # 25
            {
                "title": "Modern Apartment in Tokyo",
                "description": "Explore the vibrant city of Tokyo from this modern and centrally located apartment.",
                "image_url": "https://images.unsplash.com/photo-1480796927426-f609979314bd?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 2000,
                "location": "Tokyo",
                "country": "Japan",
                "category": "Trending",
                "geometry": {"type":"Point","coordinates":[139.6917,35.6895]}
            },
            # 26
            {
                "title": "Lakefront Cabin in New Hampshire",
                "description": "Spend your days by the lake in this cozy cabin in the scenic White Mountains of New Hampshire.",
                "image_url": "https://images.unsplash.com/photo-1578645510447-e20b4311e3ce?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 1200,
                "location": "New Hampshire",
                "country": "United States",
                "category": "Mountains",
                "geometry": {"type":"Point","coordinates":[-71.4548,43.1939]}
            },
            # 27
            {
                "title": "Luxury Villa in the Maldives",
                "description": "Indulge in luxury in this overwater villa in the Maldives with stunning views of the Indian Ocean.",
                "image_url": "https://images.unsplash.com/photo-1439066615861-d1af74d74000?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 6000,
                "location": "Maldives",
                "country": "Maldives",
                "category": "Pools",
                "geometry": {"type":"Point","coordinates":[73.5101,3.2028]}
            },
            # 28
            {
                "title": "Ski Chalet in Aspen",
                "description": "Hit the slopes in style with this luxurious ski chalet in the world-famous Aspen ski resort.",
                "image_url": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
                "price": 4000,
                "location": "Aspen",
                "country": "United States",
                "category": "Mountains",
                "geometry": {"type":"Point","coordinates":[-106.8175,39.1911]}
            },
            {
                "title": "Overwater Villa  Maldives",
                "description": "Crystal lagoons and luxury stays.",
                "image_url": "https://example.com/maldives.jpg",
                "price": 1200,
                "location": "Malé",
                "country": "Maldives",
                "category": "Islands",
                "geometry":{"type":"Point","coordinates":[73.5,4.2]},
            },
            {
                "title": "Santorini Cliff House",
                "description": "Iconic blue domes and white houses.",
                "image_url": "https://example.com/santorini.jpg",
                "price": 900,
                "location": "Santorini",
                "country": "Greece",
                "category": "Islands",
                "geometry":{"type":"Point","coordinates":[25.4,36.4]},
            },
            {
                "title": "Overwater Bungalow – Bora Bora",
                "description": "Iconic lagoon stay.",
                "image_url": "https://example.com/bora.jpg",
                "price": 1500,
                "location": "Bora Bora",
                "country": "French Polynesia",
                "category": "Islands",
                "geometry":{"type":"Point","coordinates":[-151.741,-16.5]},
            },
            {
                "title": "Beach Villa – Phuket",
                "description": "Thailand’s tropical paradise.",
                "image_url": "https://example.com/phuket.jpg",
                "price": 700,
                "location": "Phuket",
                "country": "Thailand",
                "category": "Islands",
                "geometry":{"type":"Point","coordinates":[98.4,7.9]},
            },

            # 🏊 POOLS
            {
                "title": "Marina Bay Sands Rooftop Pool",
                "description": "World’s most famous infinity pool.",
                "image_url": "https://example.com/marina.jpg",
                "price": 500,
                "location": "Singapore",
                "country": "Singapore",
                "category": "Pools",
                "geometry":{"type":"Point","coordinates":[103.85,1.28]},
            },
            {
                "title": "Jungle Villa  Ubud",
                "description": "Infinity pools in Bali’s jungles.",
                "image_url": "https://example.com/ubud.jpg",
                "price": 400,
                "location": "Ubud",
                "country": "Indonesia",
                "category": "Pools",
                "geometry":{"type":"Point","coordinates":[115.26,-8.5]},
            },
            {
                "title": "Beach Resort – Los Cabos",
                "description": "Poolside luxury in Mexico.",
                "image_url": "https://example.com/cabos.jpg",
                "price": 350,
                "location": "Los Cabos",
                "country": "Mexico",
                "category": "Pools",
                "geometry":{"type":"Point","coordinates":[-109.9,22.89]},
            },
            {
                "title": "Sky Pool – Dubai",
                "description": "High-rise luxury swimming.",
                "image_url": "https://example.com/dubai.jpg",
                "price": 800,
                "location": "Dubai",
                "country": "United Arab Emirates",
                "category": "Pools",
                "geometry":{"type":"Point","coordinates":[55.3,25.2]},
            },

            # ⛺ CAMPING
            {
                "title": "Yellowstone Tent Camp",
                "description": "Classic American camping.",
                "image_url": "https://example.com/yellowstone.jpg",
                "price": 150,
                "location": "Yellowstone",
                "country": "USA",
                "category": "Camping",
                "geometry":{"type":"Point","coordinates":[-110.6,44.6]},
                "title": "Sahara Desert Camp",
                "description": "Bedouin tents under stars.",
                "image_url": "https://example.com/sahara.jpg",
                "price": 180,
                "location": "Merzouga",
                "country": "Morocco",
                "category": "Camping",
                "geometry":{"type":"Point","coordinates":[-3.98,31.1]},
            },
            {
                "title": "Banff Mountain Camp",
                "description": "Canadian Rockies adventure.",
                "image_url": "https://example.com/banff.jpg",
                "price": 200,
                "location": "Banff",
                "country": "Canada",
                "category": "Camping",
                "geometry":{"type":"Point","coordinates":[-115.57,51.18]},
            },
            {
                "title": "Campervan Trip – New Zealand",
                "description": "Freedom camping across islands.",
                "image_url": "https://example.com/nz.jpg",
                "price": 220,
                "location": "Queenstown",
                "country": "New Zealand",
                "category": "Camping",
                "geometry":{"type":"Point","coordinates":[168.7,-45.03]},
            },

            # 🚜 FARMS
            {
                "title": "Tuscan Vineyard Stay",
                "description": "Olives, wine, and rustic villas.",
                "image_url": "https://example.com/tuscany.jpg",
                "price": 300,
                "location": "Tuscany",
                "country": "Italy",
                "category": "Farms",
                "geometry":{"type":"Point","coordinates":[11.25,43.77]},
            },
            {
                "title": "Kerala Spice Plantation",
                "description": "Coconut and spice farms.",
                "image_url": "https://example.com/kerala.jpg",
                "price": 120,
                "location": "Kerala",
                "country": "India",
                "category": "Farms",
                "geometry":{"type":"Point","coordinates":[76.27,10.85]},
            },
            {
                "title": "California Wine Country Farm",
                "description": "Organic food and vineyard stays.",
                "image_url": "https://example.com/california.jpg",
                "price": 250,
                "location": "Napa Valley",
                "country": "USA",
                "category": "Farms",
                "geometry":{"type":"Point","coordinates":[-122.36,38.5]},
            },
            {
                "title": "Australian Outback Farm",
                "description": "Sheep & cattle station life.",
                "image_url": "https://example.com/outback.jpg",
                "price": 200,
                "location": "Alice Springs",
                "country": "Australia",
                "category": "Farms",
                "geometry":{"type":"Point","coordinates":[133.88,-23.7]},
            },

            # ❄️ ARCTIC
            {
                "title": "Glass Igloo – Lapland",
                "description": "Northern Lights stay.",
                "image_url": "https://example.com/lapland.jpg",
                "price": 600,
                "location": "Rovaniemi",
                "country": "Finland",
                "category": "Arctic",
                "geometry":{"type":"Point","coordinates":[25.75,66.5]},
            },
            {
                "title": "Glacier Hotel – Iceland",
                "description": "Stay by ice caves and hot springs.",
                "image_url": "https://example.com/iceland.jpg",
                "price": 550,
                "location": "Reykjavik",
                "country": "Iceland",
                "category": "Arctic",
                "geometry":{"type":"Point","coordinates":[-21.9,64.14]},
            },
            {
                "title": "Fjord Cabin – Norway",
                "description": "Arctic fjordside cabins.",
                "image_url": "https://example.com/norway.jpg",
                "price": 400,
                "location": "Tromsø",
                "country": "Norway",
                "category": "Arctic",
                "geometry":{"type":"Point","coordinates":[18.95,69.65]},
            },
            {
                "title": "Alaska Wilderness Lodge",
                "description": "Snowy backcountry stays.",
                "image_url": "https://example.com/alaska.jpg",
                "price": 450,
                "location": "Anchorage",
                "country": "USA",
                "category": "Arctic",
                "geometry":{"type":"Point","coordinates":[-149.9,61.2]},
            },

            # 🚢 SHIP
            {
                "title": "Caribbean Cruise",
                "description": "Bahamas and Jamaica luxury.",
                "image_url": "https://example.com/caribbean.jpg",
                "price": 900,
                "location": "Caribbean Sea",
                "country": "Multiple",
                "category": "Ships",
                "geometry":{"type":"Point","coordinates":[-75,20]},
            },
            {
                "title": "Kerala Houseboat",
                "description": "Backwater cruising in India.",
                "image_url": "https://example.com/houseboat.jpg",
                "price": 150,
                "location": "Alleppey",
                "country": "India",
                "category": "Ships",
                "geometry":{"type":"Point","coordinates":[76.34,9.5]},
            },
            {
                "title": "Venice Canal Boat",
                "description": "Historic waterways of Venice.",
                "image_url": "https://example.com/venice.jpg",
                "price": 220,
                "location": "Venice",
                "country": "Italy",
                "category": "Ships",
                "geometry":{"type":"Point","coordinates":[12.33,45.44]},
            },
            {
                "title": "Dubai Luxury Yacht",
                "description": "Skyscraper coast cruising.",
                "image_url": "https://example.com/yacht.jpg",
                "price": 1200,
                "location": "Dubai",
                "country": "UAE",
                "category": "Ships",
                "geometry":{"type":"Point","coordinates":[55.3,25.2]},
            },

            # 🏚 DOMES
            {
                "title": "Bubble Dome – Iceland",
                "description": "Sleep under Northern Lights.",
                "image_url": "https://example.com/bubble.jpg",
                "price": 450,
                "location": "Golden Circle",
                "country": "Iceland",
                "category": "Domes",
                "geometry":{"type":"Point","coordinates":[-20.3,64.3]},
            },
            {
                "title": "Rainforest Eco-Dome – Costa Rica",
                "description": "Eco domes in lush rainforest.",
                "image_url": "https://example.com/costa.jpg",
                "price": 300,
                "location": "La Fortuna",
                "country": "Costa Rica",
                "category": "Domes",
                "geometry":{"type":"Point","coordinates":[-84.64,10.47]},
            },
            {
                "title": "Joshua Tree Dome",
                "description": "Desert dome near National Park.",
                "image_url": "https://example.com/joshua.jpg",
                "price": 250,
                "location": "Joshua Tree",
                "country": "USA",
                "category": "Domes",
                "geometry":{"type":"Point","coordinates":[-116.31,34.13]},
            },
            {
                "title": "Dome Glamping – Japan",
                "description": "Japanese countryside domes.",
                "image_url": "https://example.com/japan.jpg",
                "price": 280,
                "location": "Nagano",
                "country": "Japan",
                "category": "Domes",
                "geometry":{"type":"Point","coordinates":[138.2,36.65]},
            },

            # ☀️ HOT BEACHES
            {
                "title": "Goa Beach Stay",
                "description": "Sun, sand, and nightlife.",
                "image_url": "https://example.com/goa.jpg",
                "price": 150,
                "location": "Goa",
                "country": "India",
                "category": "Hot Beaches",
                "geometry":{"type":"Point","coordinates":[74.1,15.5]},
            },
            {
                "title": "Miami South Beach Hotel",
                "description": "Iconic beach vibes in the USA.",
                "image_url": "https://example.com/miami.jpg",
                "price": 300,
                "location": "Miami",
                "country": "USA",
                "category": "Hot Beaches",
                "geometry":{"type":"Point","coordinates":[-80.19,25.76]},
            },
            {
                "title": "Bondi Surf Lodge",
                "description": "Australia’s famous surfing beach.",
                "image_url": "https://example.com/bondi.jpg",
                "price": 250,
                "location": "Bondi Beach",
                "country": "Australia",
                "category": "Hot Beaches",
                "geometry":{"type":"Point","coordinates":[151.27,-33.89]},
            },
            {
                "title": "Rio Copacabana Hotel",
                "description": "Brazil’s most vibrant beach.",
                "image_url": "https://example.com/rio.jpg",
                "price": 280,
                "location": "Rio de Janeiro",
                "country": "Brazil",
                "category": "Hot Beaches",
                "geometry":{"type":"Point","coordinates":[-43.17,-22.97]},
            },
        ]

        for item in listings:
            Listing.objects.create(
                owner=user,
                title=item["title"],
                description=item["description"],
                image_url=item["image_url"],
                price=item["price"],
                location=item["location"],
                country=item["country"],
                category=item["category"],
                geometry_type="Point",
                geometry_coordinates=item["geometry"]["coordinates"],
            )

        self.stdout.write(self.style.SUCCESS("✅ 28 listings seeded successfully!"))