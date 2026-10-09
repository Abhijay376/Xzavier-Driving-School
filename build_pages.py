import sys
sys.path.insert(0, "/home/claude/site2")
from build import page_shell, trust_section_html, OUT, set_area_nav_items, set_country_nav_items
import os
import math

# ============================================================
# AREA / SUBURB LANDING PAGES: data
# ============================================================
# Coordinates are approximate suburb-centre lat/long, used only to rank
# "nearest suburbs" for the areaServed schema field (not survey-grade).
SUBURB_COORDS = {
    "Dandenong": (-37.9877, 145.2148),
    "Noble Park": (-37.9622, 145.1758),
    "Hallam": (-38.0004, 145.2649),
    "Hampton Park": (-38.0139, 145.2489),
    "Berwick": (-38.0359, 145.3444),
    "Cranbourne": (-38.1136, 145.2833),
    "Narre Warren": (-38.0177, 145.3057),
    "Pakenham": (-38.0736, 145.4854),
    "Frankston": (-38.1436, 145.1233),
    "Carrum Downs": (-38.0906, 145.1467),
    "Heatherton": (-37.9581, 145.0847),
    "Springvale": (-37.9497, 145.1522),
    # extra South East Melbourne suburbs, used only as a pool to compute the
    # "nearest 20 suburbs" list for each of the 12 pages above
    "Keysborough": (-37.9975, 145.1508),
    "Endeavour Hills": (-37.9686, 145.2494),
    "Doveton": (-37.9967, 145.2298),
    "Clayton": (-37.9186, 145.1147),
    "Clayton South": (-37.9394, 145.1225),
    "Mulgrave": (-37.9436, 145.1636),
    "Wheelers Hill": (-37.9086, 145.1817),
    "Rowville": (-37.9436, 145.2311),
    "Lynbrook": (-38.0294, 145.2611),
    "Lyndhurst": (-38.0489, 145.2894),
    "Clyde": (-38.1108, 145.3436),
    "Clyde North": (-38.0836, 145.3411),
    "Officer": (-38.0642, 145.4092),
    "Beaconsfield": (-38.0417, 145.3728),
    "Botanic Ridge": (-38.1594, 145.2778),
    "Skye": (-38.0658, 145.2039),
    "Seaford": (-38.1006, 145.1264),
    "Langwarrin": (-38.1594, 145.1839),
    "Chelsea": (-38.0511, 145.1211),
    "Bonbeach": (-38.0653, 145.1214),
    "Patterson Lakes": (-38.0794, 145.1408),
    "Aspendale": (-38.0247, 145.1017),
    "Mordialloc": (-38.0033, 145.0886),
    "Parkdale": (-37.9925, 145.0872),
    "Mentone": (-37.9797, 145.0678),
    "Cheltenham": (-37.9647, 145.0561),
    "Moorabbin": (-37.9394, 145.0578),
    "Oakleigh": (-37.9000, 145.0906),
    "Huntingdale": (-37.9128, 145.1181),
    "Dingley Village": (-37.9789, 145.1358),
    "Lysterfield": (-37.9394, 145.2831),
    "Scoresby": (-37.9022, 145.2494),
    "Ferntree Gully": (-37.8814, 145.2953),
    "Boronia": (-37.8511, 145.2814),
}

def haversine_km(a, b):
    lat1, lon1 = a
    lat2, lon2 = b
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    x = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(x))

def nearest_n_suburbs(suburb, n=20):
    origin = SUBURB_COORDS[suburb]
    dists = [(name, haversine_km(origin, coord)) for name, coord in SUBURB_COORDS.items() if name != suburb]
    dists.sort(key=lambda t: t[1])
    return [name for name, _ in dists[:n]]

SUBURB_WIKIDATA = {
    "Dandenong": "Q1159408",
    "Noble Park": "Q7045757",
    "Hallam": "Q5642748",
    "Hampton Park": "Q5646261",
    "Berwick": "Q829245",
    "Cranbourne": "Q3309297",
    "Narre Warren": "Q6966236",
    "Pakenham": "Q2046587",
    "Frankston": "Q1136771",
    "Carrum Downs": "Q1045308",
    "Heatherton": "Q5694243",
    "Springvale": "Q7581218",
}

# nearest VicRoads drive test centre + its page slug, per suburb
SUBURB_TEST_CENTRE = {
    "Dandenong": ("Heatherton", "drive-test-heatherton.html"),
    "Noble Park": ("Heatherton", "drive-test-heatherton.html"),
    "Springvale": ("Heatherton", "drive-test-heatherton.html"),
    "Heatherton": ("Heatherton", "drive-test-heatherton.html"),
    "Hallam": ("Pakenham", "drive-test-pakenham.html"),
    "Hampton Park": ("Pakenham", "drive-test-pakenham.html"),
    "Berwick": ("Pakenham", "drive-test-pakenham.html"),
    "Cranbourne": ("Pakenham", "drive-test-pakenham.html"),
    "Narre Warren": ("Pakenham", "drive-test-pakenham.html"),
    "Pakenham": ("Pakenham", "drive-test-pakenham.html"),
    "Frankston": ("Frankston", "drive-test-frankston.html"),
    "Carrum Downs": ("Frankston", "drive-test-frankston.html"),
    "Keysborough": ("Heatherton", "drive-test-heatherton.html"),
    "Endeavour Hills": ("Heatherton", "drive-test-heatherton.html"),
    "Doveton": ("Heatherton", "drive-test-heatherton.html"),
    "Clayton": ("Heatherton", "drive-test-heatherton.html"),
    "Clayton South": ("Heatherton", "drive-test-heatherton.html"),
    "Mulgrave": ("Heatherton", "drive-test-heatherton.html"),
    "Wheelers Hill": ("Heatherton", "drive-test-heatherton.html"),
    "Rowville": ("Heatherton", "drive-test-heatherton.html"),
    "Oakleigh": ("Heatherton", "drive-test-heatherton.html"),
    "Lynbrook": ("Frankston", "drive-test-frankston.html"),
    "Lyndhurst": ("Frankston", "drive-test-frankston.html"),
    "Clyde": ("Pakenham", "drive-test-pakenham.html"),
    "Clyde North": ("Pakenham", "drive-test-pakenham.html"),
    "Officer": ("Pakenham", "drive-test-pakenham.html"),
    "Beaconsfield": ("Pakenham", "drive-test-pakenham.html"),
}

AREA_SUBURBS = ["Noble Park", "Hallam", "Hampton Park", "Berwick", "Cranbourne",
                "Narre Warren", "Pakenham", "Frankston", "Carrum Downs", "Heatherton", "Springvale",
                # 15 additional Dandenong-area suburb pages
                "Keysborough", "Endeavour Hills", "Doveton", "Clayton", "Clayton South",
                "Mulgrave", "Wheelers Hill", "Rowville", "Lynbrook", "Lyndhurst",
                "Clyde", "Clyde North", "Officer", "Beaconsfield", "Oakleigh"]

# Local knowledge facts used on each suburb page's "Local Knowledge" section,
# so every page carries genuinely suburb-specific detail rather than a
# find-and-replace of the suburb name (real, well-known public landmarks --
# train stations, shopping centres, main roads -- not VicRoads test claims).
SUBURB_LOCAL_FACTS = {
    "Noble Park": ["Noble Park train station on the Pakenham/Cranbourne line", "Buckley Street shopping strip"],
    "Hallam": ["Hallam train station", "South Gippsland Freeway access at Hallam Road"],
    "Hampton Park": ["Hampton Park Shopping Centre", "Somerville Road and Hallam Road corridor"],
    "Berwick": ["the Berwick Village shopping strip", "Berwick train station and the Princes Highway"],
    "Cranbourne": ["Cranbourne Park Shopping Centre", "Cranbourne train station, end of the Cranbourne line"],
    "Narre Warren": ["Fountain Gate Shopping Centre, one of Melbourne's largest", "Narre Warren train station"],
    "Pakenham": ["Pakenham train station, end of the Pakenham line", "the Princes Highway through Pakenham"],
    "Frankston": ["Frankston train station, end of the Frankston line", "Bayside Shopping Centre on Nepean Highway"],
    "Carrum Downs": ["Carrum Downs Shopping Centre", "Hall Road"],
    "Heatherton": ["Kingston Road and Heatherton Road", "proximity to the VicRoads Heatherton test centre itself"],
    "Springvale": ["Springvale train station", "the Springvale Road shopping and dining precinct"],
    "Keysborough": ["Parkmore Shopping Centre", "Cheltenham Road and Corrigan Road"],
    "Endeavour Hills": ["Endeavour Hills Shopping Centre", "Heatherton Road and Kurrajong Way"],
    "Doveton": ["Doveton Shopping Centre", "Power Road and Sherwood Park"],
    "Clayton": ["Clayton train station", "Clayton Road, close to Monash University"],
    "Clayton South": ["the Clarinda shopping strip", "Centre Road and Clayton Road"],
    "Mulgrave": ["Waverley Gardens Shopping Centre", "Police Road and the Monash Freeway"],
    "Wheelers Hill": ["Brandon Park Shopping Centre", "Ferntree Gully Road and Jells Road"],
    "Rowville": ["Stud Park Shopping Centre", "Wellington Road and Stud Road"],
    "Lynbrook": ["Lynbrook train station", "Evans Road"],
    "Lyndhurst": ["the South Gippsland Highway corridor", "proximity to Casey Fields"],
    "Clyde": ["Clyde Road and the newer estates around it", "the growing Clyde town centre"],
    "Clyde North": ["the Cranbourne-Frankston Road corridor", "Berwick-Cranbourne Road"],
    "Officer": ["Officer train station", "the Princes Highway through Officer"],
    "Beaconsfield": ["Beaconsfield train station", "O'Neil Road and the Beaconsfield shops"],
    "Oakleigh": ["Oakleigh train station", "the Eaton Mall dining precinct"],
}

# Per-suburb content written for each page individually.
SUBURB_PROFILES = {
"Noble Park": {
 "intro": "Noble Park sits between Springvale and Dandenong, and a lot of our learners here are students or shift workers who need early or late lessons. The suburb mixes quiet residential grids with some of the busiest arterial roads in the south east, so it is a good place to build confidence quickly.",
 "roads": ["Turning across traffic on the Princes Highway, where the gaps are short and drivers move fast", "Heatherton Road and Corrigan Road intersections, which have multiple turning lanes and arrows", "Parking and pulling out around the Buckley Street shops, where pedestrians cross between cars"],
 "tip": "Most Noble Park learners struggle with lane choice on multi-lane roads. We spend time on reading lane arrows early, so you are in the right lane well before the intersection."},
"Hallam": {
 "intro": "Hallam is a small suburb wedged between Dandenong and Narre Warren, but it sits on some of the busiest freeway and highway links in the area. Learners here often need to get used to fast merging much earlier than they expect.",
 "roads": ["Merging onto the Monash Freeway and the Hallam Bypass, where you need to match speed before you join", "Hallam Road, with its mix of school traffic and trucks", "The Princes Highway service lanes, which catch out new drivers who miss the entry point"],
 "tip": "We practise freeway merges on quieter times first, then build up to peak traffic. Confident merging is one of the things testers notice straight away."},
"Hampton Park": {
 "intro": "Hampton Park is mostly residential, with long curving streets, lots of roundabouts and plenty of families learning together. It is a calm place to start, but the main roads around it are busy.",
 "roads": ["Roundabouts along Hallam Road and through the estates, where giving way correctly matters", "Pound Road and Somerville Road, which carry fast traffic past side streets", "School zones around the local primary and secondary schools at drop-off and pick-up times"],
 "tip": "Roundabouts are the most common reason Hampton Park learners lose marks. We drill signalling on exit and choosing the right lane on the bigger two-lane ones."},
"Berwick": {
 "intro": "Berwick has a busy village centre, hilly streets and fast roads on every side. Many of our Berwick learners are Year 11 and 12 students fitting lessons around school.",
 "roads": ["High Street in Berwick Village, with angle parking, pedestrian crossings and slow traffic", "Hill starts and blind crests on the streets around the village", "Clyde Road and Berwick-Cranbourne Road, which are busy and keep changing as the area grows"],
 "tip": "Hill starts and checking blind spots when pulling out of angle parks are the two skills we focus on most here, because they come up so often around Berwick."},
"Cranbourne": {
 "intro": "Cranbourne is a large and fast-growing suburb with a mix of older streets near the town centre and newer estates further out. Learners here often have long drives to work or study, so they need to be confident on high-speed roads.",
 "roads": ["The South Gippsland Highway through the town centre, with traffic lights close together", "Sladen Street and Thompsons Road, where roadworks and lane changes are common", "Newer estates with narrow streets, parked cars on both sides and lots of roundabouts"],
 "tip": "Because Cranbourne roads change so often, we teach you to read signs and lane markings rather than rely on memory. That habit carries straight into the test."},
"Narre Warren": {
 "intro": "Narre Warren is home to Fountain Gate, one of the biggest shopping centres in Melbourne, and the traffic around it can be hard for new drivers. Outside the centre the suburb is mostly quiet residential streets.",
 "roads": ["Car parks and entry roads around Fountain Gate, with pedestrians, trolleys and people reversing", "The Princes Highway and Narre Warren-Cranbourne Road, which are busy for most of the day", "Webb Street and the streets around the train station"],
 "tip": "We use the roads near Fountain Gate to practise scanning for hazards. Seeing a pedestrian or a reversing car early is exactly what the test is looking for."},
"Pakenham": {
 "intro": "Pakenham has its own VicRoads test centre, so most local learners sit their test only a few minutes from home. That means the roads you practise on every week are likely to be the roads you are tested on.",
 "roads": ["Main Street and the town centre, with parked cars, crossings and slow traffic", "The Princes Highway and the freeway ramps on the edge of town", "Newer estates with roundabouts, speed humps and changing speed limits"],
 "tip": "Because the test centre is in town, we can run full mock tests on the real local roads. Learners who do one or two mock tests usually go in far more relaxed."},
"Frankston": {
 "intro": "Frankston is a big bayside suburb at the end of the Frankston line. The VicRoads test centre for this area is a short drive away in Seaford, so most Frankston learners test close to home.",
 "roads": ["Nepean Highway and the Frankston city centre, with trucks, buses and lots of pedestrians", "Cranbourne Road and the Peninsula Link ramps, where traffic is fast", "Hilly residential streets with parked cars and tight turns"],
 "tip": "Frankston city centre is a great place to practise patience and observation. We work on keeping a safe gap and not rushing turns when traffic is heavy."},
"Carrum Downs": {
 "intro": "Carrum Downs is one of the closest suburbs to the VicRoads test centre in Seaford. It has a large industrial area, so learners here get used to sharing the road with trucks early on.",
 "roads": ["Frankston-Dandenong Road, where trucks and fast traffic share the lanes", "Hall Road and the roundabouts near the shopping centre", "EastLink entry and exit ramps on the edge of the suburb"],
 "tip": "We teach you how to give trucks the space they need, especially when they turn. Driving calmly around heavy vehicles is a skill testers pay attention to."},
"Heatherton": {
 "intro": "Heatherton is where one of the main VicRoads test centres in the south east is located, on Corporate Drive. Learners from all over the area come here for their test, so knowing these roads is a real advantage.",
 "roads": ["Warrigal Road and Centre Dandenong Road, which are wide, busy and have lots of turning lanes", "Kingston Road, with changing speed limits", "Business park roads near the test centre, with parked trucks and driveways"],
 "tip": "Local learners have the benefit of driving the test area during normal lessons. We make sure you are comfortable with the busiest intersections near the centre, not just the quiet streets."},
"Springvale": {
 "intro": "Springvale is a busy, multicultural centre known for its food and markets. Many of our Springvale learners are overseas licence holders who already drive but need to learn Victorian road rules and test habits.",
 "roads": ["Springvale Road through the shopping area, with heavy traffic, buses and people crossing", "The Princes Highway and Centre Road intersections", "Side streets near the market and station where parking is tight"],
 "tip": "Overseas drivers often have good car control but lose marks on observation and road rules. We focus on head checks, full stops and giving way the Victorian way."},
"Keysborough": {
 "intro": "Keysborough has newer estates on one side and fast roads and industrial areas on the other. It sits close to the Heatherton test centre, so many local learners test there.",
 "roads": ["Cheltenham Road and Perry Road, with fast traffic and long straight sections", "The Dingley Bypass and EastLink, where speeds are high", "Estate streets with roundabouts and parked cars"],
 "tip": "Keysborough learners often need to practise keeping to the speed limit on long, straight roads. We work on checking your speedometer without losing focus on the road."},
"Endeavour Hills": {
 "intro": "Endeavour Hills is a hilly residential suburb with winding streets and lots of courts and cul-de-sacs. It is a good place to build low-speed control and practise turning around safely.",
 "roads": ["Hill starts and steep driveways throughout the suburb", "Heatherton Road, which is busy and has several traffic lights close together", "Winding streets with blind corners, where you need to keep left and slow down"],
 "tip": "Three-point turns and reverse parking on a slope come up a lot here. We practise them until they feel easy, because they are often part of the test."},
"Doveton": {
 "intro": "Doveton is a small, established suburb right next to Dandenong. It is close to our base, so we can often fit Doveton lessons in at short notice.",
 "roads": ["The Princes Highway, where you need to turn across several lanes of traffic", "Power Road and Kidds Road intersections", "Older residential streets with narrow lanes and parked cars"],
 "tip": "Many Doveton learners are nervous about the Princes Highway. We build up slowly, starting with left turns before moving on to right turns across traffic."},
"Clayton": {
 "intro": "Clayton is home to Monash University and Monash Medical Centre, so a lot of our Clayton learners are university students and hospital staff with busy schedules.",
 "roads": ["Clayton Road, which is busy with buses, students and hospital traffic", "North Road and Centre Road, with lots of traffic lights and turning lanes", "Streets around the university, where pedestrians and cyclists are everywhere"],
 "tip": "Clayton is a good place to practise watching for cyclists and pedestrians. We focus on checking mirrors and blind spots before every turn."},
"Clayton South": {
 "intro": "Clayton South, including the Clarinda area, is mostly quiet residential streets with a few busy roads running through. It is very close to the Heatherton test centre.",
 "roads": ["Centre Road and Clayton Road, which are busy at peak times", "Heatherton Road and the roads leading towards the test centre", "Quiet streets that are good for practising parking and turns"],
 "tip": "Being so close to Heatherton, we can practise on the main roads near the test centre during normal lessons, which takes a lot of the surprise out of test day."},
"Mulgrave": {
 "intro": "Mulgrave sits next to the Monash Freeway and has big roads, large intersections and shopping centres. Learners here need to get comfortable with fast, multi-lane traffic.",
 "roads": ["Springvale Road and Wellington Road, which have many lanes and turning arrows", "Monash Freeway entry and exit ramps", "Shopping centre car parks around Waverley Gardens"],
 "tip": "Lane changes are a key skill in Mulgrave. We practise signalling, checking mirrors and blind spots, and then moving over smoothly without slowing down."},
"Wheelers Hill": {
 "intro": "Wheelers Hill is a leafy, hilly suburb with lots of quiet streets and a few busy main roads. It suits learners who want to build confidence before moving onto heavier traffic.",
 "roads": ["Ferntree Gully Road, which is fast and busy at peak times", "Jells Road and the hills around Jells Park", "Quiet residential streets for parking, turns and hill starts"],
 "tip": "Because of the hills, we focus on controlling your speed going downhill and moving off smoothly uphill. Both come up often around Wheelers Hill."},
"Rowville": {
 "intro": "Rowville is a family suburb with lots of roundabouts, school zones and a busy shopping area around Stud Park. Many of our learners here are teenagers learning with help from their parents.",
 "roads": ["Stud Road and Wellington Road, which are busy and have several lanes", "Roundabouts throughout the suburb", "School zones, which have lower speed limits at set times"],
 "tip": "We give Rowville learners a simple practice plan to use with their parents between lessons, so the hours you log at home actually help you pass."},
"Lynbrook": {
 "intro": "Lynbrook is a newer, smaller suburb with modern estates and quick access to the freeway. Its quiet streets are great for beginners, but you are only a few minutes from fast roads.",
 "roads": ["Evans Road and the roads around Lynbrook station", "The South Gippsland Freeway and Western Port Highway nearby", "Estate streets with roundabouts and parked cars"],
 "tip": "We use Lynbrook's quiet streets for your first lessons, then move to nearby highways once your basic control is solid."},
"Lyndhurst": {
 "intro": "Lyndhurst is a growing area with new estates next to busy highways and industrial land. Learners here need to be ready for trucks and high speeds as well as quiet estate streets.",
 "roads": ["The Western Port Highway and South Gippsland Highway, with trucks and fast traffic", "Thompsons Road, which is busy and often has roadworks", "New estate streets where the layout keeps changing"],
 "tip": "Following distance is the big one in Lyndhurst. We teach you to keep a safe gap behind trucks and to give yourself room to stop."},
"Clyde": {
 "intro": "Clyde has grown very fast in recent years, with new estates and roads opening all the time. Learners here often deal with roadworks, temporary signs and changing speed limits.",
 "roads": ["Clyde Road and Ballarto Road, which are being upgraded in stages", "New estate streets with roundabouts and lots of construction traffic", "Thompsons Road as you head towards Cranbourne and Berwick"],
 "tip": "Roadworks are a common test hazard. We practise reading temporary signs and lowering your speed early, which is exactly what testers want to see."},
"Clyde North": {
 "intro": "Clyde North is one of the newest areas in the south east, with brand new estates, schools and shops. Many families here have learners getting ready for their test at the same time.",
 "roads": ["Berwick-Cranbourne Road and Soldiers Road, which are busy and growing", "New estate roundabouts and narrow streets with parked cars", "School zones around the new schools"],
 "tip": "New estates can make learners too relaxed. We practise staying alert for kids, parked cars and people pulling out of driveways."},
"Officer": {
 "intro": "Officer sits between Beaconsfield and Pakenham and is growing quickly. It is close to the Pakenham test centre, so most local learners test there.",
 "roads": ["The Princes Highway and Princes Freeway ramps", "Station Street and the roads around Officer station", "New estates with roundabouts and changing layouts"],
 "tip": "We spend time on the roads between Officer and Pakenham, so the trip to the test centre and the roads around it feel familiar."},
"Beaconsfield": {
 "intro": "Beaconsfield is a quiet suburb at the foot of the hills, with a small shopping strip and quick access to the highway. The hilly roads make it great for building control.",
 "roads": ["The Princes Highway and Old Princes Highway", "O'Neil Road and the streets around the shops", "Hilly, winding roads heading up towards the Dandenong Ranges"],
 "tip": "Winding roads teach you to slow down before a bend, not in it. That skill makes a big difference to how smooth and safe your driving looks on test day."},
"Oakleigh": {
 "intro": "Oakleigh is an older suburb with a busy shopping and food strip around Eaton Mall and Atherton Road. Streets here are narrower and busier than in the outer suburbs.",
 "roads": ["Warrigal Road and Dandenong Road, which are busy and have many lanes", "Atherton Road and the streets around Eaton Mall, with lots of pedestrians", "Narrow side streets with parked cars on both sides"],
 "tip": "Narrow streets mean you often need to give way to oncoming cars. We practise judging gaps and pulling over safely so you stay calm in tight spots."},
}

# NAP (Name / Address / Phone). Address sourced from an old repo, NOT confirmed
# by the user; flagged clearly in the build log and final summary.
NAP_NAME = "X Zavier Driving School (XDS)"
NAP_ADDRESS = "124 Stud Rd, Dandenong VIC 3175"
NAP_PHONE_DISPLAY = "0434 538 142"
NAP_PHONE_TEL = "0434538142"
NAP_EMAIL = "xzavierdrivingschool@gmail.com"

def slugify(suburb):
    return suburb.lower().replace(" ", "-")

def area_page_href(suburb):
    return "area-" + slugify(suburb) + ".html"

# Register the "Areas We Serve" nav dropdown BEFORE any page is generated,
# so every page (including index.html, generated further down) gets it.
set_area_nav_items([
    ("area-" + slugify(s), area_page_href(s), s) for s in AREA_SUBURBS
])

TIER_INFO = {
    "recognised": {
        "label": "Recognised Country",
        "summary": "Direct exchange, with no knowledge or practical test required in most cases.",
        "requirement": "No. You need a current full licence (not a learner or provisional licence), but age and years of experience do not change the requirement.",
    },
    "edr": {
        "label": "Experienced Driver Recognition Country",
        "summary": "A knowledge test is generally required, and a practical driving test as well if you're under 25 or have less driving experience.",
        "requirement": "Under 25 usually needs a knowledge + practical test; 25+ with 3+ years&rsquo; experience may qualify for a more direct pathway.",
    },
    "other": {
        "label": "Full Victorian Licensing Process",
        "summary": "The full Victorian process applies: a knowledge test, a hazard perception test, and a practical driving test.",
        "requirement": "No. Since Experienced Driver Recognition ended in Victoria on 30 April 2025, the same three tests apply whatever your age or years of driving.",
    },
}

COUNTRIES = [
    {
        "name": "India", "slug": "india", "tier": "other",
        "note": "Indian licences are not on Victoria&rsquo;s recognised country list. Experienced Driver Recognition, which some websites still mention, ended in Victoria on 30 April 2025, so Indian licence holders now complete all three tests whatever their age or experience.",
        "side": "India drives on the left, like Australia, so the road layout will feel familiar.",
        "language": "Most Indian licences show your details in English. If any part of yours is not in English, get a NAATI-certified translation. VicRoads can also check your licence with the Indian Consulate if it cannot verify it another way.",
        "habits": ["Coming to a full stop at stop signs, even when the road looks clear", "Giving way to traffic already on a roundabout, and signalling left as you leave it", "Sticking to the speed limit exactly, including 40 km/h school zones", "Not using the horn except to warn of danger"],
    },
    {
        "name": "Philippines", "slug": "philippines", "tier": "other",
        "note": "Philippine licences are not on Victoria&rsquo;s recognised country list, and Experienced Driver Recognition ended in Victoria on 30 April 2025. That means Philippine licence holders now complete all three tests.",
        "side": "The Philippines drives on the right, so this is the biggest change. Turning right across traffic, entering roundabouts clockwise and keeping left all take practice.",
        "language": "Philippine LTO licences are issued in English, so a translation is not usually needed.",
        "habits": ["Keeping left, especially after turning into a quiet street", "Looking right first at intersections and roundabouts", "Turning right into the correct lane, not the far lane", "Head checks over your right shoulder before changing lanes"],
    },
    {
        "name": "China", "slug": "china", "tier": "other",
        "note": "Chinese licences are not on Victoria&rsquo;s recognised country list, so the full Victorian licensing process applies.",
        "side": "China drives on the right, so you will need to retrain your habits for left-side driving, including where you look first at intersections.",
        "language": "Chinese licences are not in English, so you need a NAATI-certified translation or one from the Chinese Consulate. If you want to sit a test in Chinese or need an interpreter, VicRoads asks you to book an in-person appointment.",
        "habits": ["Keeping left, especially after turns", "Looking right first when entering roundabouts and side roads", "Giving way to pedestrians when turning", "Using the full width of your lane, not hugging the centre line"],
    },
    {
        "name": "Sri Lanka", "slug": "sri-lanka", "tier": "other",
        "note": "Sri Lankan licences are not on Victoria&rsquo;s recognised country list, so the full Victorian licensing process applies.",
        "side": "Sri Lanka drives on the left, like Australia, so the road layout will feel familiar.",
        "language": "Check whether every detail on your licence is in English. If any part is in Sinhala or Tamil only, get a NAATI-certified translation.",
        "habits": ["Full stops at stop signs and staying behind the line", "Keeping a safe following distance on fast roads", "Checking blind spots with a head check, not just mirrors", "Waiting for a safe gap rather than edging into traffic"],
    },
    {
        "name": "Pakistan", "slug": "pakistan", "tier": "other",
        "note": "Pakistani licences are not on Victoria&rsquo;s recognised country list, so the full Victorian licensing process applies.",
        "side": "Pakistan drives on the left, like Australia, so the road layout will feel familiar.",
        "language": "Check whether every detail on your licence is in English. If any part is in Urdu only, get a NAATI-certified translation.",
        "habits": ["Staying in your lane and signalling every lane change", "Giving way correctly at roundabouts and T-intersections", "Keeping to speed limits and slowing for school zones", "Full stops at stop signs"],
    },
    {
        "name": "Nepal", "slug": "nepal", "tier": "other",
        "note": "Nepalese licences are not on Victoria&rsquo;s recognised country list, so the full Victorian licensing process applies.",
        "side": "Nepal drives on the left, like Australia. If most of your driving was on hilly or narrow roads, multi-lane roads and freeways in Melbourne may take some getting used to.",
        "language": "Check whether every detail on your licence is in English. If any part is in Nepali only, get a NAATI-certified translation.",
        "habits": ["Merging onto freeways at the right speed", "Choosing the correct lane on multi-lane roads", "Head checks before changing lanes", "Keeping a steady speed that matches the limit"],
    },
    {
        "name": "United Kingdom", "slug": "uk", "tier": "recognised",
        "note": "UK licences are on Victoria&rsquo;s recognised country list, so a full UK car licence can usually be swapped for a Victorian licence without a knowledge or drive test.",
        "side": "The UK drives on the left, and most road rules are similar. Speeds are in km/h, and there are some rules that catch UK drivers out, like hook turns in Melbourne&rsquo;s CBD.",
        "language": "UK licences are in English, so no translation is needed. A UK provisional licence is a learner licence, not a full licence, so it does not qualify for a direct swap.",
        "habits": ["Remembering speeds are in km/h, not mph", "Giving way at roundabouts to vehicles already on them, which works the same as in the UK", "Hook turns at signed intersections in the Melbourne CBD", "40 km/h school zones at set times"],
    },
]

COUNTRY_LINKS_HTML = "\n        ".join(
    '<a href="{slug}-to-vicroads-licence.html" class="area-chip">{name}<small>{label}</small></a>'.format(
        slug=c["slug"], name=c["name"], label=TIER_INFO[c["tier"]]["label"]
    ) for c in COUNTRIES
)

# Register the footer "Licence Conversion" column links (before any page is
# generated, same pattern as set_area_nav_items).
set_country_nav_items([
    ("country-" + c["slug"], c["slug"] + "-to-vicroads-licence.html", c["name"] + " to VicRoads")
    for c in COUNTRIES
])

def nap_faq_section(suburb_label, address=NAP_ADDRESS, extra_faqs=None):
    faqs = [
        ("Where is X Zavier Driving School located?",
         "Our home base and instructor meeting point is {addr}. We also provide pickup and drop-off for lessons across {area} and surrounding South East Melbourne suburbs, so you don't need to travel to us.".format(addr=address, area=suburb_label)),
        ("What is the best way to contact XDS?",
         "WhatsApp is the fastest way to reach us on {phone}, and most messages get a reply within the hour. You can also call {phone}, email {email}, or use the Contact Us form on this site.".format(phone=NAP_PHONE_DISPLAY, email=NAP_EMAIL)),
    ]
    if extra_faqs:
        faqs = faqs + extra_faqs
    items = "\n        ".join(
        '''<div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">{q}<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">{a}</div></div>
        </div>'''.format(q=q, a=a) for q, a in faqs
    )
    return '''<section class="block block-alt" id="nap-faq">
    <div class="container">
      <div class="info-grid">
        <div class="info-card">
          <h2><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7z"/></svg>Business Details</h2>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7z"/></svg><div><strong>Name</strong><span>{name}</span></div></div>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7z"/></svg><div><strong>Address</strong><span>{addr}</span></div></div>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg><div><strong>Phone</strong><span><a href="tel:{tel}">{phone}</a></span></div></div>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 4h16a1 1 0 011 1v14a1 1 0 01-1 1H4a1 1 0 01-1-1V5a1 1 0 011-1zm1 2v.6l7 4.7 7-4.7V6H5zm14 2.3l-6.5 4.3a1 1 0 01-1 0L5 8.3V18h14V8.3z"/></svg><div><strong>Email</strong><span><a href="mailto:{email}">{email}</a></span></div></div>
        </div>
        <div class="faq-list">
          {faqs}
        </div>
      </div>
    </div>
  </section>'''.format(name=NAP_NAME, addr=address, tel=NAP_PHONE_TEL, phone=NAP_PHONE_DISPLAY, email=NAP_EMAIL, faqs=items)

SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "DrivingSchool",
  "name": "X Zavier Driving School",
  "alternateName": "XDS",
  "telephone": "+61434538142",
  "email": "xzavierdrivingschool@gmail.com",
  "url": "https://drivetestvic.com.au",
  "areaServed": ["Dandenong", "Frankston", "Mooroolbark", "Pakenham", "Heatherton", "South East Melbourne"],
  "sameAs": ["https://share.google/PSBVWeY83VacVhKtu"],
  "employee": {
    "@type": "Person",
    "name": "Medii Sha",
    "jobTitle": "VicRoads ADI Accredited Driving Instructor",
    "sameAs": "https://www.facebook.com/meddii.sha/"
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "I'm based in Dandenong, where will I actually sit my test?",
      "acceptedAnswer": { "@type": "Answer", "text": "VicRoads Dandenong doesn't run practical drive tests, so Dandenong learners are usually booked at VicRoads Heatherton. Your instructor will train you specifically on that centre's local roads well before test day." }
    },
    {
      "@type": "Question",
      "name": "Do I need my own car, or can I use yours for the test?",
      "acceptedAnswer": { "@type": "Answer", "text": "Either works. Bring a fully compliant personal vehicle, or hire one of our dual-control instructor cars, already built into the Express Test Package and Ultimate Test Pass Pack." }
    },
    {
      "@type": "Question",
      "name": "I passed my test overseas, do I still need to sit a VicRoads test?",
      "acceptedAnswer": { "@type": "Answer", "text": "It depends entirely on which country issued your licence. Recognised countries can usually swap directly, and all other countries need the knowledge, hazard perception and drive tests. Run it through our free Overseas Licence Conversion Checker for an instant, specific answer." }
    },
    {
      "@type": "Question",
      "name": "Do your instructors only work in Dandenong itself?",
      "acceptedAnswer": { "@type": "Answer", "text": "No, Dandenong is our base but our coverage runs across South East Melbourne, with dedicated local pages for each of the 26 suburbs we serve and all four VicRoads test centres we prepare students for: Frankston, Mooroolbark, Pakenham and Heatherton." }
    }
  ]
}
</script>
'''

BYLINE = '<span class="byline"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6 6.6.7-5 4.4 1.5 6.5L12 16.8 6 19.6l1.5-6.5-5-4.4 6.6-.7z"/></svg>Reviewed by Medii Sha, VicRoads ADI Accredited Instructor</span>'

# Real-world VicRoads test-centre coordinates (approximate street-level,
# looked up per physical address -- NOT the suburb-centre SUBURB_COORDS
# values above, which are too coarse for a site-specific location schema).
CENTRE_GEO = {
    "Frankston": {"address": "71 Hartnett Dr, Seaford VIC 3198", "lat": -38.1051, "lon": 145.1339},
    "Mooroolbark": {"address": "Shop 1, 191 Hull Rd, Mooroolbark VIC 3138", "lat": -37.7942, "lon": 145.3117},
    "Pakenham": {"address": "33 Exchange Drive, Pakenham VIC 3810", "lat": -38.0759, "lon": 145.4834},
    "Heatherton": {"address": "77 Corporate Dr, Heatherton VIC 3202", "lat": -37.9556, "lon": 145.0797},
}

def centre_schema(name):
    g = CENTRE_GEO[name]
    return '''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "DrivingSchool",
  "name": "X Zavier Driving School",
  "alternateName": "XDS",
  "telephone": "+61434538142",
  "email": "xzavierdrivingschool@gmail.com",
  "url": "https://drivetestvic.com.au/drive-test-{slug}.html",
  "description": "VicRoads {name} drive test centre guide and test preparation from X Zavier Driving School.",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "{addr}",
    "addressRegion": "VIC",
    "addressCountry": "AU"
  }},
  "geo": {{
    "@type": "GeoCoordinates",
    "latitude": {lat},
    "longitude": {lon}
  }},
  "sameAs": ["https://share.google/PSBVWeY83VacVhKtu"]
}}
</script>
'''.format(slug=slugify(name), name=name, addr=g["address"], lat=g["lat"], lon=g["lon"])

PACKAGES_SECTION = '''<section class="block block-alt" id="packages">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">Lessons &amp; Test Packages</span>
        <h2>Our Driving Packages</h2>
        <p>Simple, transparent pricing. Message us on WhatsApp to lock in a time.</p>
      </div>
      <div class="pkg-grid">
        <div class="pkg-card">
          <div class="pkg-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4a1 1 0 011-1h8a1 1 0 011 1v3h3a1 1 0 011 1v11a1 1 0 01-1 1H4a1 1 0 01-1-1V8a1 1 0 011-1h3V4z"/></svg></div>
          <h3>Single Lesson</h3>
          <p class="pkg-sub">1 &times; 1-hour driving lesson</p>
          <div class="pkg-price">$70<span>/lesson</span></div>
          <ul class="pkg-list">
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Pick-up &amp; drop-off included</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Dual-control vehicle</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Flexible scheduling</li>
          </ul>
          <a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61434538142?text=Hi%20XDS!%20I'd%20like%20to%20enquire%20about%20a%20Single%20Lesson%20(%2470).">Enquire on WhatsApp</a>
        </div>
        <div class="pkg-card">
          <div class="pkg-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6 6.6.7-5 4.4 1.5 6.5L12 16.8 6 19.6l1.5-6.5-5-4.4 6.6-.7z"/></svg></div>
          <h3>5-Lesson Pass</h3>
          <p class="pkg-sub">5 &times; 1-hour driving lessons</p>
          <div class="pkg-price">$325<span>/pack</span></div>
          <div class="pkg-note">Save $25 vs. single lessons</div>
          <ul class="pkg-list">
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Consistent instructor</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Progress tracking</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Bulk-rate pricing</li>
          </ul>
          <a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61434538142?text=Hi%20XDS!%20I'd%20like%20to%20book%20the%205-Lesson%20Pass%20(%24325).">Enquire on WhatsApp</a>
        </div>
        <div class="pkg-card featured">
          <span class="pkg-badge">Most Popular</span>
          <div class="pkg-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M5 11l1.5-4.5A2 2 0 018.4 5h7.2a2 2 0 011.9 1.5L19 11v7a1 1 0 01-1 1h-1a1 1 0 01-1-1v-1H8v1a1 1 0 01-1 1H6a1 1 0 01-1-1v-7z"/></svg></div>
          <h3>Express Test Package</h3>
          <p class="pkg-sub">2 lessons + test car hire</p>
          <div class="pkg-price">$220<span>/package</span></div>
          <ul class="pkg-list">
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Pre-test refresher lesson</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Compliant test-day vehicle</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Pickup from test centre</li>
          </ul>
          <a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61434538142?text=Hi%20XDS!%20I'd%20like%20to%20book%20the%20Express%20Test%20Package%20(%24220).">Enquire on WhatsApp</a>
        </div>
        <div class="pkg-card">
          <div class="pkg-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 1l9 4v6c0 5.2-3.4 9.6-9 11-5.6-1.4-9-5.8-9-11V5z"/></svg></div>
          <h3>Ultimate Test Pass Pack</h3>
          <p class="pkg-sub">Complete package + extras</p>
          <div class="pkg-price">$560<span>/package</span></div>
          <div class="pkg-note">Save $70 &middot; Best value</div>
          <ul class="pkg-list">
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>5 lessons + 1 mock test</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Free test-day vehicle hire</li>
            <li><svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.4-1.5z"/></svg>Full test-route preparation</li>
          </ul>
          <a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61434538142?text=Hi%20XDS!%20I'd%20like%20to%20book%20the%20Ultimate%20Test%20Pass%20Pack%20(%24560).">Enquire on WhatsApp</a>
        </div>
      </div>
      <p class="price-note">Prices shown are indicative starting rates. Ask on WhatsApp for current availability and bulk-package discounts, and gift vouchers are available for any package.</p>
    </div>
  </section>'''

print("part 1 loaded", len(PACKAGES_SECTION))

def centre_packages_section(centre_name):
    return '''<section class="block block-alt">
    <div class="container">
      <div class="section-title"><h2>Our Driving Packages</h2></div>
      <div class="pkg-grid">
        <div class="pkg-card"><h3>Single Lesson</h3><p class="pkg-sub">1 &times; 1-hour lesson</p><div class="pkg-price">$70</div><a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61434538142?text=Hi%20XDS!%20I''d%20like%20a%20Single%20Lesson%20ahead%20of%20my%20{centre}%20test.">Enquire on WhatsApp</a></div>
        <div class="pkg-card"><h3>5-Lesson Pass</h3><p class="pkg-sub">Save $25</p><div class="pkg-price">$325</div><a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61434538142?text=Hi%20XDS!%20I''d%20like%20the%205-Lesson%20Pass%20ahead%20of%20my%20{centre}%20test.">Enquire on WhatsApp</a></div>
        <div class="pkg-card featured"><span class="pkg-badge">Popular for {centre}</span><h3>Express Test Package</h3><p class="pkg-sub">Lessons + test car hire</p><div class="pkg-price">$220</div><a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61434538142?text=Hi%20XDS!%20I''d%20like%20the%20Express%20Test%20Package%20for%20my%20{centre}%20test.">Enquire on WhatsApp</a></div>
        <div class="pkg-card"><h3>Ultimate Test Pass Pack</h3><p class="pkg-sub">Complete package + extras</p><div class="pkg-price">$560</div><a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="https://wa.me/61434538142?text=Hi%20XDS!%20I''d%20like%20the%20Ultimate%20Test%20Pass%20Pack%20for%20my%20{centre}%20test.">Enquire on WhatsApp</a></div>
      </div>
    </div>
  </section>'''.replace("''", "'").format(centre=centre_name)

TOOLS_LINKS_SECTION = '''<section class="block">
    <div class="container">
      <div class="section-title"><h2>Interactive Tools</h2></div>
      <div class="tools-grid">
        <div class="tool-card"><h3><svg viewBox="0 0 24 24" fill="currentColor"><path d="M5 11l1.5-4.5A2 2 0 018.4 5h7.2a2 2 0 011.9 1.5L19 11v7a1 1 0 01-1 1h-1a1 1 0 01-1-1v-1H8v1a1 1 0 01-1 1H6a1 1 0 01-1-1v-7z"/></svg>VicRoads Test Readiness Quiz</h3><p>Check your weak spots before test day.</p><a href="readiness-quiz.html" class="btn btn-navy btn-block">Start Quiz &rarr;</a></div>
        <div class="tool-card"><h3><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a4 4 0 014 4c0 2-1.5 3.4-2.5 4.4A6 6 0 0116 16v2a2 2 0 01-2 2H10a2 2 0 01-2-2v-2a6 6 0 012.5-5.6C9.5 9.4 8 8 8 6a4 4 0 014-4z"/></svg>Overseas Licence Conversion Checker</h3><p>Converting from overseas? Check eligibility.</p><a href="licence-checker.html" class="btn btn-navy btn-block">Check Eligibility &rarr;</a></div>
      </div>
    </div>
  </section>'''

def instructor_section(centre_name):
    return '''<section class="block">
    <div class="container">
      <div class="section-title"><h2>Your Instructor for {centre}</h2></div>
      <div class="instructor-card" style="max-width:600px;margin:0 auto">
        <div class="instructor-photo">MS</div>
        <div><h3>Medii Sha</h3><p>VicRoads ADI Accredited Instructor &middot; 7+ Years Experience</p><a href="https://www.facebook.com/meddii.sha/" target="_blank" rel="noopener">View Facebook Profile &rarr;</a></div>
      </div>
    </div>
  </section>'''.format(centre=centre_name)

VEHICLE_REQ_SECTION = '''<section class="block block-alt">
    <div class="container">
      <div class="section-title"><h2>Vehicle Requirements</h2></div>
      <div class="two-col">
        <div class="info-card"><h3 style="margin-bottom:10px;color:var(--navy)">Using your own vehicle</h3><ul class="bullet-list"><li>Roadworthy and currently registered</li><li>Working horn, indicators, brake lights, headlights, wipers</li><li>Functioning front and rear demisters</li><li>Valid insurance and correctly displayed L-plates</li></ul></div>
        <div class="info-card"><h3 style="margin-bottom:10px;color:var(--navy)">Using an XDS instructor vehicle</h3><ul class="bullet-list"><li>Already meets all VicRoads compliance requirements</li><li>Dual-control for added safety</li><li>Included in the Express Test Package and Ultimate Test Pass Pack</li></ul></div>
      </div>
    </div>
  </section>'''

TERMINATION_CRITICAL_SECTION = '''<div class="two-col" style="margin-top:20px">
        <div class="info-card"><h3 style="margin-bottom:10px;color:var(--navy)">Immediate Termination Errors</h3><ul class="bullet-list x"><li>Intervention by the tester</li><li>Disobeying a direction/sign</li><li>Collision</li><li>Failing to give way</li><li>Excessive speed</li><li>Stopping in a dangerous position</li><li>Failing to stop</li><li>Dangerous action</li></ul></div>
        <div class="info-card"><h3 style="margin-bottom:10px;color:var(--navy)">Critical Errors</h3><p style="font-size:.82rem;color:var(--muted);margin-bottom:10px">More than 1 in Stage 1, or more than 2 overall, ends the test.</p><ul class="bullet-list warn"><li>Too slow</li><li>Fail to look</li><li>Fail to signal</li><li>Blocking a pedestrian crossing</li><li>Mounting the kerb</li><li>Stalling</li><li>Incomplete stop</li><li>Illegal action</li></ul></div>
      </div>'''

print("part 2 loaded")

# ============================================================
# HOME PAGE
# ============================================================
HOME_HERO = '''<section class="hero">
    <div class="container">
      <div>
        <h1>Driving Instructor Dandenong &amp; VicRoads Test Specialists</h1>
        <p class="lead">X Zavier Driving School (XDS) is a VicRoads ADI accredited team based in Dandenong, backed by 4.9&#9733; from 105+ verified Google reviews. Learners across South East Melbourne choose us to get test-ready faster, with instructors who know the local VicRoads centres road by road.</p>
        <div class="hero-actions">
          <a class="btn btn-wa" target="_blank" rel="noopener" href="https://wa.me/61434538142?text=Hi%20XDS!%20I'd%20like%20to%20book%20a%20driving%20lesson.">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm5.8 14.2c-.2.7-1.4 1.3-2 1.4-.5.1-1.1.1-1.8-.1-.4-.1-1-.3-1.7-.6-3-1.3-4.9-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3.1s.8-2.2 1-2.5c.3-.3.6-.4.8-.4h.6c.2 0 .5 0 .7.5.3.7.9 2.2 1 2.4.1.2.1.4 0 .6-.1.2-.2.3-.4.5l-.5.6c-.2.2-.3.4-.1.7.2.3.9 1.5 1.9 2.4 1.3 1.2 2.4 1.5 2.7 1.7.3.2.5.1.7-.1l.9-1c.2-.3.5-.2.8-.1.3.1 2 1 2.3 1.1.3.2.5.2.6.3.1.2.1.9-.1 1.6z"/></svg>
            Message Us on WhatsApp
          </a>
          <button class="btn btn-outline" onclick="openContactModal()">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 4h16a1 1 0 011 1v14a1 1 0 01-1 1H4a1 1 0 01-1-1V5a1 1 0 011-1zm1 2v.6l7 4.7 7-4.7V6H5zm14 2.3l-6.5 4.3a1 1 0 01-1 0L5 8.3V18h14V8.3z"/></svg>
            Send an Enquiry
          </button>
        </div>
        <div class="hero-badges">
          <span class="hero-badge"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6 6.6.7-5 4.4 1.5 6.5L12 16.8 6 19.6l1.5-6.5-5-4.4 6.6-.7z"/></svg>VicRoads ADI Accredited</span>
          <span class="hero-badge"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6 6.6.7-5 4.4 1.5 6.5L12 16.8 6 19.6l1.5-6.5-5-4.4 6.6-.7z"/></svg>4.9&#9733; from 105+ Reviews</span>
          <span class="hero-badge"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6 6.6.7-5 4.4 1.5 6.5L12 16.8 6 19.6l1.5-6.5-5-4.4 6.6-.7z"/></svg>Dandenong-Based Since Day One</span>
        </div>

        <div class="search-wrap">
          <label for="testCenterSearch">Find your VicRoads test centre</label>
          <div class="search-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
            <input type="text" id="testCenterSearch" placeholder="Try &ldquo;Frankston&rdquo;, &ldquo;Pakenham&rdquo;, &ldquo;Heatherton&rdquo;&hellip;" autocomplete="off" oninput="filterCenters(this.value)" onkeydown="if(event.key==='Enter'){goToFirstCenterMatch(this.value)}">
            <button onclick="goToFirstCenterMatch(document.getElementById('testCenterSearch').value)">Search</button>
          </div>
          <div id="searchResults" class="search-results" hidden></div>
        </div>
      </div>
      <div class="hero-visual instructor-promo">
        <div class="instructor-promo-top">
          <div class="instructor-promo-avatar">MS</div>
          <div>
            <div class="instructor-promo-name">Medii Sha</div>
            <div class="instructor-promo-meta">Auto &middot; 7+ yrs instructing</div>
          </div>
        </div>
        <div class="instructor-promo-stars">&#9733;&#9733;&#9733;&#9733;&#9733; <span>4.9 &middot; 105+ reviews</span></div>
        <div class="instructor-promo-price">From $70/hr</div>
        <a href="contact-us.html" class="instructor-promo-btn">View Profile</a>
      </div>
    </div>
  </section>'''

WHY_CHOOSE_SECTION = '''<section class="block">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">The XDS Difference</span>
        <h2>What Makes XDS Different</h2>
        <p>Here&rsquo;s what Dandenong and South East Melbourne learners actually get when they book with X Zavier Driving School.</p>
      </div>
      <div class="why-grid">
        <div class="why-card">
          <div class="why-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M5 11l1.5-4.5A2 2 0 018.4 5h7.2a2 2 0 011.9 1.5L19 11v7a1 1 0 01-1 1h-1a1 1 0 01-1-1v-1H8v1a1 1 0 01-1 1H6a1 1 0 01-1-1v-7zm2.2-1h9.6l-1-3H8.2l-1 3zM7 14a1 1 0 100-2 1 1 0 000 2zm10 0a1 1 0 100-2 1 1 0 000 2z"/></svg></div>
          <h3>One Booking, Test-Day Sorted</h3>
          <p>Lessons and a compliant dual-control test car bundled into a single package, so there&rsquo;s nothing extra to organise on the day.</p>
        </div>
        <div class="why-card">
          <div class="why-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4a1 1 0 011-1h8a1 1 0 011 1v3h3a1 1 0 011 1v11a1 1 0 01-1 1H4a1 1 0 01-1-1V8a1 1 0 011-1h3V4zm2 3h6V5H9v2zM4 9v10h16V9H4z"/></svg></div>
          <h3>Not Locked to One Instructor</h3>
          <p>If your instructor isn&rsquo;t the right match, swap at any time. No awkward conversation, no cancellation fee.</p>
        </div>
        <div class="why-card">
          <div class="why-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 5v5.4l4.2 2.5-.8 1.3-5-3V7h1.6z"/></svg></div>
          <h3>Book &amp; Reschedule Anytime</h3>
          <p>Our online booking runs 24/7, so a change of plans doesn&rsquo;t mean waiting on a callback during business hours.</p>
        </div>
        <div class="why-card">
          <div class="why-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 1a2 2 0 012 2v1.06A8 8 0 0119.94 10H21a2 2 0 012 2v0a2 2 0 01-2 2h-1.06A8 8 0 0114 19.94V21a2 2 0 01-2 2 2 2 0 01-2-2v-1.06A8 8 0 014.06 14H3a2 2 0 01-2-2 2 2 0 012-2h1.06A8 8 0 0110 4.06V3a2 2 0 012-2zm0 5a6 6 0 100 12 6 6 0 000-12z"/></svg></div>
          <h3>Upfront, No-Surprise Pricing</h3>
          <p>Every package below shows the full price and what&rsquo;s included, with bulk-lesson discounts built in, not buried in fine print.</p>
        </div>
        <div class="why-card">
          <div class="why-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M20 7h-3.2a3 3 0 10-5.6-2 3 3 0 10-5.6 2H2a1 1 0 00-1 1v3a1 1 0 001 1h9v9h2v-9h9a1 1 0 001-1V8a1 1 0 00-1-1zM9 7a1 1 0 111-1 1 1 0 01-1 1zm6 0a1 1 0 111-1 1 1 0 01-1 1zM3 13V9h8v4H3zm10 0V9h8v4h-8zM4 15h7v7H5a1 1 0 01-1-1v-6zm9 0h7v6a1 1 0 01-1 1h-6v-7z"/></svg></div>
          <h3>Gift a Lesson Package</h3>
          <p>Driving lesson vouchers make an easy gift for a new P-plater in the family, redeemable against any package.</p>
        </div>
      </div>
    </div>
  </section>'''

TOOLS_HOME_SECTION = '''<section class="block" id="tools">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">Free Interactive Tools</span>
        <h2>Check Where You Stand in Under a Minute</h2>
        <p>No phone call needed. Try the quick versions below, or open the full tool for a detailed report.</p>
      </div>
      <div class="tools-grid">
        <div class="tool-card">
          <h3><svg viewBox="0 0 24 24" fill="currentColor"><path d="M5 11l1.5-4.5A2 2 0 018.4 5h7.2a2 2 0 011.9 1.5L19 11v7a1 1 0 01-1 1h-1a1 1 0 01-1-1v-1H8v1a1 1 0 01-1 1H6a1 1 0 01-1-1v-7z"/></svg>VicRoads Test Readiness Quiz</h3>
          <p>3 quick questions to get an instant read on your weak spots.</p>
          <div id="miniQuizArea">
            <div class="quiz-progress" id="miniQuizProgress">Question 1 of 3</div>
            <div class="progress-bar"><div class="progress-fill" id="miniQuizFill" style="width:33%"></div></div>
            <div class="quiz-q" id="miniQuizQ">How confident are you with parallel or reverse parking?</div>
            <div class="quiz-options" id="miniQuizOptions">
              <button onclick="miniAnswerQuiz(0)">Very confident, consistent every time</button>
              <button onclick="miniAnswerQuiz(1)">Somewhat, sometimes need extra attempts</button>
              <button onclick="miniAnswerQuiz(2)">Not confident, I avoid it</button>
            </div>
          </div>
          <div class="tool-result" id="miniQuizResult"></div>
          <a href="readiness-quiz.html" class="tool-link">Take the full 8-question quiz &rarr;</a>
        </div>

        <div class="tool-card">
          <h3><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a4 4 0 014 4c0 2-1.5 3.4-2.5 4.4A6 6 0 0116 16v2a2 2 0 01-2 2H10a2 2 0 01-2-2v-2a6 6 0 012.5-5.6C9.5 9.4 8 8 8 6a4 4 0 014-4z"/></svg>Overseas Licence Conversion Checker</h3>
          <p>Find out in seconds whether you can convert directly, or need a test.</p>
          <div class="tool-field">
            <label>Which country issued your licence?</label>
            <select id="miniCountrySelect">
              <option value="">Select country</option>
              <option value="recognised">UK, Ireland, USA, Canada, New Zealand, Germany, Japan, Singapore</option>
              <option value="other">India, Philippines, China, Sri Lanka, Pakistan, Nepal or any other country</option>
            </select>
          </div>
          <div class="tool-field">
            <label>Your current age</label>
            <input type="number" id="miniAgeInput" placeholder="e.g. 27" min="16" max="99">
          </div>
          <button class="tool-btn" onclick="miniCheckLicence()">Check My Pathway</button>
          <div class="tool-result" id="miniLicenceResult"></div>
          <a href="licence-checker.html" class="tool-link">Open the full checker with requirements table &rarr;</a>
        </div>
      </div>
    </div>
  </section>'''

REVIEWS_SECTION = '''<section class="block block-alt" id="reviews">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">Social Proof</span>
        <h2>What Our Students Say</h2>
        <p>Real reviews from learners who passed their VicRoads test with XDS.</p>
      </div>
      <div class="reviews-badge-row">
        <div class="rating-badge">
          <div class="num">4.9</div>
          <div>
            <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            <div class="sub">105+ Verified Google Reviews</div>
          </div>
        </div>
        <a href="https://share.google/PSBVWeY83VacVhKtu" target="_blank" rel="noopener" class="btn btn-outline-navy">View Our Google Business Profile</a>
      </div>
      <div class="review-grid">
        <div class="review-card">
          <span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
          <p>"Medii Sha was an amazing instructor. Patient, calm and really helped me build my confidence. Passed first time! Highly recommend XDS."</p>
          <div class="review-who"><span class="review-avatar">S</span><div><div class="review-name">Sarah L.</div><div class="review-loc">Passed at Dandenong VicRoads</div></div></div>
        </div>
        <div class="review-card">
          <span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
          <p>"The online booking system is so easy and convenient. The lessons were well structured and exactly what I needed. Thanks XDS!"</p>
          <div class="review-who"><span class="review-avatar">J</span><div><div class="review-name">James T.</div><div class="review-loc">Passed at Frankston VicRoads</div></div></div>
        </div>
        <div class="review-card">
          <span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
          <p>"Great experience from start to finish. Flexible instructors and the test car was perfect. Highly recommend to anyone learning to drive."</p>
          <div class="review-who"><span class="review-avatar">P</span><div><div class="review-name">Priya K.</div><div class="review-loc">Passed at Heatherton VicRoads</div></div></div>
        </div>
      </div>
    </div>
  </section>'''

AREAS_SECTION = '''<section class="block" id="areas">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">Where We Cover</span>
        <h2>VicRoads Test Centres &amp; Service Areas</h2>
        <p>We prepare students for drive tests at four VicRoads centres, with lessons available across Dandenong and beyond.</p>
      </div>
      <div class="area-grid">
        <a href="drive-test-frankston.html" class="area-chip">Drive Test Frankston<small>Test centre guide</small></a>
        <a href="drive-test-mooroolbark.html" class="area-chip">Drive Test Mooroolbark<small>Test centre guide</small></a>
        <a href="drive-test-pakenham.html" class="area-chip">Drive Test Pakenham<small>Test centre guide</small></a>
        <a href="drive-test-heatherton.html" class="area-chip">Drive Test Heatherton<small>Test centre guide</small></a>
        <span class="area-chip no-test">Dandenong<small>Lessons &amp; instructor base (VicRoads Dandenong does not conduct drive tests)</small></span>
      </div>
    </div>
  </section>'''

FAQ_SECTION = '''<section class="block block-alt" id="faq">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">FAQ</span>
        <h2>Frequently Asked Questions</h2>
      </div>
      <div class="faq-list" id="homeFaqList"></div>
    </div>
  </section>'''

FINAL_CTA_HOME = '''<section class="final-cta" id="contact-info">
    <div class="container">
      <h2>Ready to Book Your First Lesson?</h2>
      <p>Message us on WhatsApp, the fastest way to lock in a time slot with a VicRoads ADI accredited instructor.</p>
      <div class="btn-row">
        <a class="btn btn-wa" target="_blank" rel="noopener" href="https://wa.me/61434538142?text=Hi%20XDS!%20I'd%20like%20to%20book%20a%20driving%20lesson.">Chat on WhatsApp</a>
        <a class="btn btn-outline" href="tel:0434538142">Call 0434 538 142</a>
        <a class="btn btn-outline" href="contact-us.html">Visit Contact Page</a>
      </div>
    </div>
  </section>'''

HOME_BODY = '\n  '.join([
    HOME_HERO,
    trust_section_html(),
    WHY_CHOOSE_SECTION,
    PACKAGES_SECTION,
    TOOLS_HOME_SECTION,
    REVIEWS_SECTION,
    AREAS_SECTION,
    FAQ_SECTION,
    nap_faq_section(
        "Dandenong",
        extra_faqs=[
            ("Does XDS offer driving lessons in Dandenong?",
             "Yes, Dandenong is our home base and main service area. We offer driving lessons Dandenong learners can book directly, with flexible instructor options and pickup from home, school or work."),
            ("Which VicRoads test centre do Dandenong learners use?",
             "VicRoads Dandenong does not conduct practical drive tests. Dandenong-based learners are typically booked in at <a href=\"drive-test-heatherton.html\">VicRoads Heatherton</a>, and our instructors prepare you specifically for that test centre's local roads."),
            ("How much do driving lessons cost in Dandenong?",
             "Pricing is the same for all Dandenong learners. See our Lessons &amp; Test Packages above, from a Single Lesson through to the Ultimate Test Pass Pack, with bulk discounts available, and message us on WhatsApp for current availability."),
        ],
    ),
    FINAL_CTA_HOME,
])

home_html = page_shell(
    title="Driving Instructor Dandenong | VicRoads Test Prep &amp; Lessons | XDS",
    description="XDS is a VicRoads ADI accredited driving school serving Dandenong and South East Melbourne. 4.9★ rated with 105+ reviews. Book lessons, test packages, and get local VicRoads test centre guides for Frankston, Mooroolbark, Pakenham and Heatherton.",
    depth=0,
    body_content=HOME_BODY,
    page_key="home",
    schema=SCHEMA,
    breadcrumbs=[("Home", None)],
    show_sidebar=False,
)
open(os.path.join(OUT, "index.html"), "w").write(home_html)
print("index.html written:", len(home_html), "bytes")

# ============================================================
# DRIVE TEST FRANKSTON (exact spec content)
# ============================================================
FRANKSTON_HERO = '''<section class="page-hero">
    <div class="container">
      <h1>VicRoads Drive Test Frankston</h1>
      <p>Everything you need to know about the Frankston (Seaford) VicRoads test centre: local roads, common fail points, and how XDS instructors prepare you for this specific route.</p>
      ''' + BYLINE + '''
    </div>
  </section>'''

FRANKSTON_BODY = '\n  '.join([
    FRANKSTON_HERO,
    trust_section_html(),
    '''<section class="block">
    <div class="container">
      <div class="info-grid">
        <div class="info-card">
          <h2><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7zm0 9.5A2.5 2.5 0 1112 6.5a2.5 2.5 0 010 5z"/></svg>Test Centre Details</h2>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7z"/></svg><div><strong>Location</strong><span>71 Hartnett Dr, Seaford VIC 3198</span></div></div>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 5v5.4l4.2 2.5-.8 1.3-5-3V7h1.6z"/></svg><div><strong>Hours</strong><span>Monday to Friday, 8:30 am to 4:30 pm (by appointment only)</span></div></div>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 16V6a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H8l-4 4v-6z"/></svg><div><strong>Public transit access</strong><span>Peninsula Bvd / Hartnett Dr bus stop (4 min walk) &middot; Lorna St / Klauer St bus stop (6 min walk) &middot; Bus routes 779 &amp; 901 &middot; Frankston train line</span></div></div>
        </div>
        <div class="info-card">
          <h3 style="margin-bottom:10px">Quick facts</h3>
          <ul class="bullet-list">
            <li>Minor faults: up to 15 allowed before failing</li>
            <li>Test runs in two stages: 10 minutes + 20 minutes</li>
            <li>Pre-drive safety check required before you start driving</li>
            <li>Test vehicle must be roadworthy and compliant</li>
          </ul>
        </div>
      </div>
    </div>
  </section>''',
    '''<section class="block block-alt">
    <div class="container">
      <div class="section-title"><h2>Test Format &amp; Rules</h2></div>
      <div class="two-col">
        <div class="info-card">
          <h3 style="margin-bottom:10px;color:var(--navy)">Minor vs. Major / Dangerous Faults</h3>
          <ul class="bullet-list">
            <li>Minor faults: up to 15 allowed across the whole test</li>
            <li>16th minor fault results in an automatic fail</li>
          </ul>
          <ul class="bullet-list x" style="margin-top:10px">
            <li>Major or dangerous faults result in an immediate fail, regardless of minor fault count</li>
          </ul>
        </div>
        <div class="info-card">
          <h3 style="margin-bottom:10px;color:var(--navy)">Pre-Drive Safety Checks Checklist</h3>
          <ul class="bullet-list">
            <li>Horn</li><li>Indicators</li><li>Wipers</li><li>Brake lights</li><li>Demisters (front &amp; rear)</li><li>Boot</li><li>Ignition in neutral / park before starting</li>
          </ul>
        </div>
      </div>
      <div class="two-col" style="margin-top:20px">
        <div class="stage-card">
          <h3>Stage 1: Basic Controls</h3>
          <div class="stage-meta">Duration: 10 minutes</div>
          <p>Low-risk environment covering basic vehicle control and low-speed manoeuvres such as a 3-point turn or reverse parallel park. You must pass Stage 1 before progressing to Stage 2.</p>
        </div>
        <div class="stage-card">
          <h3>Stage 2: Busy Traffic</h3>
          <div class="stage-meta">Duration: 20 minutes</div>
          <p>Conducted in busier traffic conditions: high-speed merging, lane changes, and complex intersections around Frankston and Seaford.</p>
        </div>
      </div>
      ''' + TERMINATION_CRITICAL_SECTION + '''
    </div>
  </section>''',
    '''<section class="block">
    <div class="container">
      <div class="section-title">
        <h2>Local Frankston Test Roads &amp; Fail Points</h2>
        <p>Real fail-point knowledge from instructors who test students on this exact route.</p>
      </div>
      <div class="fail-point">
        <div class="fail-num">1</div>
        <div><h3>Hartnett Drive <span class="speed">60 km/h</span></h3><p>Immediate roundabout negotiation right as you exit the VicRoads driveway, a common early hesitation point.</p></div>
      </div>
      <div class="fail-point">
        <div class="fail-num">2</div>
        <div><h3>Frankston-Dandenong Road <span class="speed">80 km/h</span></h3><p>Requires confident high-speed gap selection and lane switching in fast-moving traffic.</p></div>
      </div>
      <div class="fail-point">
        <div class="fail-num">3</div>
        <div><h3>Klauer Street &amp; Seaford Road <span class="speed">60 / 40 km/h</span></h3><p>School zone speed limit timing traps, a frequent source of minor and critical speed faults.</p></div>
      </div>
      <div class="fail-point">
        <div class="fail-num">4</div>
        <div><h3>Galway Street &amp; Hadley Street <span class="speed">40 / 50 km/h</span></h3><p>Narrow residential streets commonly used for Stage 1 low-speed manoeuvres.</p></div>
      </div>
    </div>
  </section>''',
    VEHICLE_REQ_SECTION,
    instructor_section("Frankston"),
    centre_packages_section("Frankston"),
    TOOLS_LINKS_SECTION,
])

frankston_html = page_shell(
    title="Drive Test Frankston | VicRoads Test Prep Guide | XDS",
    description="Frankston (Seaford) VicRoads test centre details, local roads and common fail points, from VicRoads ADI accredited instructor Medii Sha.",
    depth=0,
    body_content=FRANKSTON_BODY,
    page_key="drive-test-frankston",
    schema=centre_schema("Frankston"),
    breadcrumbs=[("Drive Test Frankston", None)],
)
open(os.path.join(OUT, "drive-test-frankston.html"), "w").write(frankston_html)
print("drive-test-frankston.html written:", len(frankston_html), "bytes")

# ============================================================
# GENERIC DRIVE-TEST-CENTRE PAGE TEMPLATE (Mooroolbark / Pakenham / Heatherton)
# ============================================================
def centre_page(name, slug, address, transit, quick_extra, fail_points, meta_title, meta_desc):
    hero = '''<section class="page-hero">
    <div class="container">
      <h1>VicRoads Drive Test {name}</h1>
      <p>Test centre details, the two-stage test format, and the local roads XDS instructors use to prepare {name} learners.</p>
      {byline}
    </div>
  </section>'''.format(name=name, byline=BYLINE)

    details = '''<section class="block">
    <div class="container">
      <div class="info-grid">
        <div class="info-card">
          <h2><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7z"/></svg>Test Centre Details</h2>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7z"/></svg><div><strong>Location</strong><span>{address}</span></div></div>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 5v5.4l4.2 2.5-.8 1.3-5-3V7h1.6z"/></svg><div><strong>Hours</strong><span>Monday to Friday, 8:30 am to 4:30 pm (by appointment only)</span></div></div>
          <div class="info-row"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 16V6a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H8l-4 4v-6z"/></svg><div><strong>Public transit access</strong><span>{transit}</span></div></div>
        </div>
        <div class="info-card">
          <h3 style="margin-bottom:10px">Quick facts</h3>
          <ul class="bullet-list">
            <li>Minor faults: up to 15 allowed before failing</li>
            <li>Two stages: 10 minutes + 20 minutes</li>
            <li>Pre-drive safety check required before you start driving</li>
            <li>{extra}</li>
          </ul>
        </div>
      </div>
    </div>
  </section>'''.format(address=address, transit=transit, extra=quick_extra)

    fmt_rules = '''<section class="block block-alt">
    <div class="container">
      <div class="section-title"><h2>Test Format &amp; Rules</h2><p>The same statewide VicRoads structure applies at every test centre, including {name}.</p></div>
      <div class="two-col">
        <div class="stage-card"><h3>Stage 1: Basic Controls</h3><div class="stage-meta">Duration: 10 minutes</div><p>Low-risk manoeuvres such as a 3-point turn or reverse parallel park, usually on the quieter streets near the centre.</p></div>
        <div class="stage-card"><h3>Stage 2: Busy Traffic</h3><div class="stage-meta">Duration: 20 minutes</div><p>Busier roads around {name}, including roundabouts, lane changes and local traffic.</p></div>
      </div>
      {tc}
    </div>
  </section>'''.format(name=name, tc=TERMINATION_CRITICAL_SECTION)

    fail_html = '\n      '.join(
        '<div class="fail-point"><div class="fail-num">{i}</div><div><h3>{road} <span class="speed">{speed}</span></h3><p>{desc}</p></div></div>'.format(
            i=i+1, road=fp['road'], speed=fp['speed'], desc=fp['desc']
        ) for i, fp in enumerate(fail_points)
    )
    fail_section = '''<section class="block">
    <div class="container">
      <div class="section-title"><h2>Local {name} Test Roads &amp; Fail Points</h2><p>Guidance based on instructor experience training students for this test centre.</p></div>
      {fails}
    </div>
  </section>'''.format(name=name, fails=fail_html)

    body = '\n  '.join([
        hero,
        trust_section_html(),
        details,
        fmt_rules,
        fail_section,
        VEHICLE_REQ_SECTION,
        instructor_section(name),
        centre_packages_section(name),
        TOOLS_LINKS_SECTION,
    ])

    html = page_shell(
        title=meta_title,
        description=meta_desc,
        depth=0,
        body_content=body,
        page_key="drive-test-" + slug,
        schema=centre_schema(name),
        breadcrumbs=[("Drive Test " + name, None)],
    )
    open(os.path.join(OUT, "drive-test-" + slug + ".html"), "w").write(html)
    print("drive-test-" + slug + ".html written:", len(html), "bytes")


centre_page(
    name="Mooroolbark",
    slug="mooroolbark",
    address="Shop 1, 191 Hull Rd, Mooroolbark VIC 3138",
    transit="Short walk from Mooroolbark railway station (Lilydale line) and local bus services along Hull Road",
    quick_extra="Located in the Mooroolbark Village shopping strip on Hull Road",
    fail_points=[
        {"road":"Hull Road", "speed":"60 km/h", "desc":"The main road directly outside the test centre, where busy shopping-strip traffic and pedestrian activity require careful speed management."},
        {"road":"Manchester &amp; Cambridge Roads", "speed":"50 km/h", "desc":"Residential streets commonly used for Stage 1 manoeuvres, including 3-point turns."},
        {"road":"Croydon-area roundabouts", "speed":"50 / 60 km/h", "desc":"Multi-lane roundabout negotiation and correct lane discipline are a frequent focus in Stage 2."},
    ],
    meta_title="Drive Test Mooroolbark | VicRoads Test Prep Guide | XDS",
    meta_desc="Mooroolbark VicRoads test centre details, local roads and common fail points, from VicRoads ADI accredited instructor Medii Sha.",
)

centre_page(
    name="Pakenham",
    slug="pakenham",
    address="33 Exchange Drive, Pakenham VIC 3810 (from 16 November 2026)",
    transit="Parking is available on site, including accessible spaces. Check your booking confirmation for the exact location",
    quick_extra="VicRoads is moving Pakenham testing to its new Exchange Drive centre. The old Pakenham Testing Centre runs until Friday 13 November 2026, and tests booked on or after Monday 16 November are at 33 Exchange Drive",
    fail_points=[
        {"road":"Princes Highway", "speed":"80 km/h", "desc":"High-speed merging and lane discipline through Pakenham&rsquo;s main highway corridor."},
        {"road":"John Street &amp; Main Street", "speed":"50 km/h", "desc":"Busy town-centre streets with pedestrian crossings and frequent give-way situations."},
        {"road":"Toomuc Valley Road roundabouts", "speed":"50 / 60 km/h", "desc":"Roundabout entry and exit lane discipline is a common focus area in Stage 2."},
    ],
    meta_title="Drive Test Pakenham | VicRoads Test Prep Guide | XDS",
    meta_desc="Pakenham VicRoads test centre details, local roads and common fail points, from VicRoads ADI accredited instructor Medii Sha.",
)

centre_page(
    name="Heatherton",
    slug="heatherton",
    address="77 Corporate Dr, Heatherton VIC 3202",
    transit="Located in the Heatherton business/corporate park and served by local bus routes. The nearest train stations (Westall and Clayton) are several km away, so most learners drive or are dropped off",
    quick_extra="One of the busiest test centres in South East Melbourne",
    fail_points=[
        {"road":"Corporate Drive &amp; Kingston Road", "speed":"60 km/h", "desc":"Wide industrial-area roads used early in the test, good for building confidence with lane positioning."},
        {"road":"Old Dandenong Road", "speed":"70 km/h", "desc":"Higher-speed merging and overtaking lanes feature heavily in Stage 2."},
        {"road":"Springvale Road &amp; Westall Road", "speed":"60 / 70 km/h", "desc":"Busy multi-lane intersections requiring confident gap selection and observation."},
    ],
    meta_title="Drive Test Heatherton | VicRoads Test Prep Guide | XDS",
    meta_desc="Heatherton VicRoads test centre details, local roads and common fail points, from VicRoads ADI accredited instructor Medii Sha.",
)

# ============================================================
# COUNTRY-SPECIFIC LICENCE CONVERSION PAGES
# ============================================================

def country_page(country):
    name = country["name"]
    slug = country["slug"]
    tier = TIER_INFO[country["tier"]]
    note = country["note"]

    hero = '''<section class="page-hero">
    <div class="container">
      <h1>{name} to VicRoads Driving Licence Conversion</h1>
      <p>How to convert your {name} driving licence to a Victorian licence: your tier, requirements, and step-by-step process.</p>
      {byline}
    </div>
  </section>'''.format(name=name, byline=BYLINE)

    intro = '''<section class="block">
    <div class="container" style="max-width:800px">
      <p style="font-size:1rem;color:#334155">If you plan to live in Victoria for more than 6 months, VicRoads says you must convert your overseas licence to a Victorian one. The 6 months starts from the day you first begin living in Victoria. Here is what that means for someone holding a {name} licence.</p>
    </div>
  </section>
  <section class="block">
    <div class="container" style="max-width:800px">
      <div class="section-title"><h2>Things {name} Licence Holders Should Know</h2></div>
      <ul class="bullet-list">
        <li><strong>Driving side:</strong> {side}</li>
        <li><strong>Translation:</strong> {language}</li>
      </ul>
      <h3 style="margin:22px 0 10px">Habits we work on with {name} drivers</h3>
      <ul class="bullet-list">
        {habits}
      </ul>
      <h3 style="margin:22px 0 10px">Good to know</h3>
      <ul class="bullet-list">
        <li>VicRoads lets you take the hazard perception test online, and has a free practice version.</li>
        <li>Permanent residents may be able to get documents translated free through the Department of Home Affairs Free Translating Service.</li>
        <li>VicRoads test and licence fees are paid separately to any lessons.</li>
      </ul>
      <p style="font-size:.85rem;color:var(--muted);margin-top:16px">Rules change. Always confirm your exact requirements with the <a href="https://www.vicroads.vic.gov.au/licences/new-to-victoria/convert-your-overseas-licence" target="_blank" rel="noopener">VicRoads requirements checker</a> before you book anything.</p>
    </div>
  </section>'''.format(name=name, side=country["side"], language=country["language"],
                     habits="".join("<li>{0}</li>".format(h) for h in country["habits"]))

    tier_card = '''<section class="block block-alt">
    <div class="container">
      <div class="info-grid">
        <div class="info-card">
          <h2><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm-1.2 14.4l-4.2-4.2 1.4-1.4 2.8 2.8 6-6 1.4 1.4z"/></svg>Your Tier: {label}</h2>
          <p style="font-size:.9rem;color:#334155;margin-bottom:12px">{summary}</p>
          <p style="font-size:.85rem;color:var(--muted)">{note}</p>
        </div>
        <div class="info-card">
          <h3 style="margin-bottom:10px">Does age or experience change this?</h3>
          <p style="font-size:.88rem;color:var(--muted)">{requirement}</p>
          <div style="margin-top:16px"><a href="licence-checker.html" class="tool-link">Use the full interactive checker for your exact pathway &rarr;</a></div>
        </div>
      </div>
    </div>
  </section>'''.format(label=tier["label"], summary=tier["summary"], note=note, requirement=tier["requirement"])

    steps = '''<section class="block">
    <div class="container">
      <div class="section-title"><h2>Step-by-Step: {name} Licence to Victorian Licence</h2></div>
      <ol class="step-list" style="max-width:700px;margin:0 auto">
        <li><h3>Check with VicRoads</h3><p>Run your details through the VicRoads requirements checker to confirm what applies to your {name} licence.</p></li>
        <li><h3>Gather your documents</h3><p>Valid {name} licence, passport/visa, proof of Victorian address, and an official English translation if your licence isn&rsquo;t in English.</p></li>
        <li><h3>Book any required tests</h3><p>{summary}</p></li>
        <li><h3>Prepare with a local instructor</h3><p>If a practical test is required, XDS instructors can prepare you for your specific VicRoads test centre. See our guides for Frankston, Mooroolbark, Pakenham and Heatherton.</p></li>
        <li><h3>Receive your Victorian licence</h3><p>Once you&rsquo;ve completed the required steps, your Victorian driver licence is issued and your {name} licence is typically surrendered.</p></li>
      </ol>
    </div>
  </section>'''.format(name=name, label=tier["label"], summary=tier["summary"])

    faq = '''<section class="block block-alt">
    <div class="container">
      <div class="section-title"><span class="eyebrow">FAQ</span><h2>{name} Licence Conversion FAQ</h2></div>
      <div class="faq-list">
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">Do I need a driving test to convert my {name} licence in Victoria?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">{summary} You can confirm this with our <a href="licence-checker.html">licence checker</a> or the VicRoads requirements checker.</div></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">How can XDS help me convert my {name} licence?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">Our VicRoads ADI accredited instructors prepare {name} licence holders for the Victorian drive test, including the test routes at Frankston, Pakenham and Heatherton.</div></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">How many lessons does an experienced {name} driver need?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">All our lessons are automatic. Experienced drivers usually need fewer lessons than new learners, because the focus is on Victorian road rules and test habits rather than car control. We will tell you after your first lesson what you need.</div></div>
        </div>
      </div>
    </div>
  </section>'''.format(name=name, summary=tier["summary"])

    body = '\n  '.join([hero, trust_section_html(), intro, tier_card, steps, faq, TOOLS_LINKS_SECTION])

    html = page_shell(
        title="{name} Driving Licence Conversion in Victoria | XDS".format(name=name),
        description="What {name} licence holders need to do to get a Victorian licence: tests, translation, and the driving habits to work on before your VicRoads test.".format(name=name),
        depth=0,
        body_content=body,
        page_key="licence-checker",
        breadcrumbs=[("Licence Checker", "licence-checker.html"), (name, None)],
    )
    fname = "{slug}-to-vicroads-licence.html".format(slug=slug)
    open(os.path.join(OUT, fname), "w").write(html)
    print(fname, "written:", len(html), "bytes")


# ============================================================
# READINESS QUIZ PAGE
# ============================================================
QUIZ_BODY = '\n  '.join([
    '''<section class="page-hero">
    <div class="container">
      <h1>Are You Ready for Your VicRoads Test?</h1>
      <p>8 quick questions. Get your weak spots and a personalised lesson recommendation at the end, completely free.</p>
      ''' + BYLINE + '''
    </div>
  </section>''',
    trust_section_html(),
    '''<section class="block">
    <div class="container" style="max-width:760px">
      <div class="tool-card" style="padding:32px">
        <div id="fullQuizArea">
          <div class="quiz-progress" id="fullQuizProgress">Question 1 of 8</div>
          <div class="progress-bar"><div class="progress-fill" id="fullQuizFill" style="width:12.5%"></div></div>
          <div class="quiz-q" id="fullQuizQ"></div>
          <div class="quiz-options" id="fullQuizOptions"></div>
        </div>
        <div class="tool-result" id="fullQuizResult"></div>
      </div>
      <p class="price-note">This quiz gives general guidance only and is not a substitute for an in-car assessment with a qualified instructor.</p>
    </div>
  </section>''',
    '''<section class="block block-alt">
    <div class="container" style="max-width:800px">
      <div class="section-title">
        <span class="eyebrow">How to Pass Your VicRoads Test</span>
        <h2>How to Pass Your VicRoads Driving Test</h2>
        <p>Straightforward, instructor-reviewed guidance for learners preparing for their VicRoads drive test in Melbourne.</p>
      </div>
      <div class="info-card" style="margin-bottom:16px">
        <h3 style="color:var(--navy);margin-bottom:8px">Common VicRoads Test Fail Reasons</h3>
        <p style="font-size:.9rem;color:var(--muted)">Most learners who don&rsquo;t pass fall down on a small number of repeat issues: incomplete mirror and blind-spot checks, hesitating at roundabouts, poor speed control through school zones, and struggling with parallel or reverse parking under time pressure. The readiness quiz above is built around these exact weak spots so you can target your remaining practice instead of guessing.</p>
      </div>
      <div class="info-card" style="margin-bottom:16px">
        <h3 style="color:var(--navy);margin-bottom:8px">How Many Lessons Before My Driving Test?</h3>
        <p style="font-size:.9rem;color:var(--muted)">There&rsquo;s no single answer, since it depends on your existing supervised driving hours and confidence level. As a general guide, most learners with solid practice need 5 to 10 lessons focused on test-day manoeuvres and their local test route, while learners with less experience or specific weak areas often benefit from a full lesson package such as our 5-Lesson Pass or Ultimate Test Pass Pack. Your quiz result above gives a personalised starting point.</p>
      </div>
      <div class="info-card">
        <h3 style="color:var(--navy);margin-bottom:8px">Driving Test Practice Tips for Melbourne Learners</h3>
        <ul class="bullet-list">
          <li>Practise on or near your actual test route before test day. See our test centre guides for Frankston, Mooroolbark, Pakenham and Heatherton.</li>
          <li>Do a full pre-drive safety check every time you practise, not just before the test.</li>
          <li>Book a lesson in the same time slot as your test so you&rsquo;re used to that traffic pattern.</li>
          <li>Focus extra practice on whatever the quiz above flags as your weak spot, rather than just repeating what you&rsquo;re already good at.</li>
        </ul>
      </div>
    </div>
  </section>''',
    '''<section class="block">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">FAQ</span>
        <h2>Readiness &amp; Test Prep FAQ</h2>
      </div>
      <div class="faq-list">
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">Am I ready for my driving test?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">Take the free quiz above. It checks the areas VicRoads testers focus on most (parking, roundabouts, observation, highway merging) and gives you a personalised readiness result in under two minutes.</div></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">What are the most common VicRoads test fail reasons?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">Incomplete observation checks, hesitating at roundabouts, incorrect speed in school zones, and parking manoeuvres that need more than the allowed attempts are the most frequent reasons learners lose enough points to fail.</div></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">How many lessons do I need before my driving test?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">Most learners need 5 to 10 lessons focused on test manoeuvres and their local test route, on top of general supervised practice. Your quiz result above gives a recommendation based on your specific weak spots.</div></div>
        </div>
      </div>
    </div>
  </section>''',
])

quiz_html = page_shell(
    title="VicRoads Test Readiness Quiz | Free Driving Test Check | XDS",
    description="Take our free 8-question VicRoads test readiness quiz to see if you're ready, and get a personalised lesson recommendation in under 2 minutes.",
    depth=0,
    body_content=QUIZ_BODY,
    page_key="readiness-quiz",
    breadcrumbs=[("Readiness Quiz", None)],
)
open(os.path.join(OUT, "readiness-quiz.html"), "w").write(quiz_html)
print("readiness-quiz.html written:", len(quiz_html), "bytes")

# ============================================================
# LICENCE CHECKER PAGE
# ============================================================
CHECKER_BODY = '\n  '.join([
    '''<section class="page-hero">
    <div class="container">
      <h1>Overseas Licence Conversion Checker</h1>
      <p>Find out whether you can convert your overseas licence directly, need a knowledge test only, or must complete the full VicRoads driving test.</p>
      ''' + BYLINE + '''
    </div>
  </section>''',
    trust_section_html(),
    '''<section class="block">
    <div class="container" style="max-width:760px">
      <div class="tool-card" style="padding:32px">
        <div class="tool-field">
          <label>Which country issued your current licence?</label>
          <select id="fullCountrySelect">
            <option value="">Select country</option>
            <option value="recognised">Recognised country (UK, Ireland, USA, Canada, New Zealand, France, Germany, Japan, Singapore and others)</option>
            <option value="other">Any other country (including India, Philippines, China, Sri Lanka, Pakistan, Nepal)</option>
          </select>
        </div>
        <div class="tool-field">
          <label>Your current age</label>
          <input type="number" id="fullAgeInput" placeholder="e.g. 27" min="16" max="99">
        </div>
        <div class="tool-field">
          <label>Years of driving experience on your overseas licence</label>
          <input type="number" id="fullExpInput" placeholder="e.g. 5" min="0" max="80">
        </div>
        <button class="tool-btn" onclick="fullCheckLicence()">Check My Pathway</button>
        <div class="tool-result" id="fullLicenceResult"></div>
      </div>
    </div>
  </section>''',
    '''<section class="block block-alt">
    <div class="container">
      <div class="section-title">
        <h2>Victoria&rsquo;s Overseas Licence Rules</h2>
        <p>Since Experienced Driver Recognition ended on 30 April 2025, there are two groups: recognised countries, and everyone else.</p>
      </div>
      <div class="table-wrap">
        <table class="req-table">
          <thead><tr><th>Tier</th><th>Example countries</th><th>Age / experience requirement</th><th>What&rsquo;s required</th></tr></thead>
          <tbody>
            <tr><td><strong>Recognised country</strong></td><td>Austria, Belgium, Bosnia and Herzegovina, Canada, Croatia, Denmark, Finland, France, Germany, Greece, Guernsey, Ireland, Isle of Man, Italy, Japan, Jersey, Luxembourg, Malta, Netherlands, New Zealand, Norway, Portugal, Singapore, Spain, Sweden, Switzerland, United Kingdom, USA</td><td>Needs a current full licence</td><td>Direct swap, no knowledge or drive test in most cases</td></tr>
            <tr><td><strong>All other countries</strong></td><td>Including India, Philippines, China, Sri Lanka, Pakistan, Nepal</td><td>Same for every age and experience level</td><td>Road rules knowledge test, hazard perception test and practical drive test</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>''',
    '''<section class="block">
    <div class="container">
      <div class="section-title">
        <h2>Step-by-Step Conversion Process</h2>
      </div>
      <ol class="step-list" style="max-width:700px;margin:0 auto">
        <li><h3>Check your group</h3><p>Use the checker above, then confirm with the VicRoads requirements checker.</p></li>
        <li><h3>Gather your documents</h3><p>Valid overseas licence, passport/visa, proof of address, and an official translation if your licence isn&rsquo;t in English.</p></li>
        <li><h3>Sit the knowledge test (if required)</h3><p>Licences from non-recognised countries need a road rules knowledge test.</p></li>
        <li><h3>Complete the hazard perception test (if required)</h3><p>VicRoads lets you take this online, and offers a free practice test.</p></li>
        <li><h3>Take your practical drive test</h3><p>Where required, XDS instructors can prepare you specifically for your local VicRoads test centre. See our test centre guides for Frankston, Mooroolbark, Pakenham and Heatherton.</p></li>
        <li><h3>Receive your Victorian licence</h3><p>Once you pass the required steps, your Victorian driver licence is issued and your overseas licence is typically surrendered.</p></li>
      </ol>
    </div>
  </section>''',
    '''<section class="block block-alt" id="country-guides">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">Country-Specific Guides</span>
        <h2>Converting From a Specific Country?</h2>
        <p>Guides for the countries our students most often come from.</p>
      </div>
      <div class="area-grid" id="countryLinksGrid">
        {country_links}
      </div>
    </div>
  </section>''',
    '''<section class="block">
    <div class="container">
      <div class="section-title">
        <span class="eyebrow">FAQ</span>
        <h2>Licence Conversion FAQ</h2>
      </div>
      <div class="faq-list">
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">How do I convert an overseas licence in Victoria?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">It depends on which country issued your licence. Use the checker above to find your tier, then follow the step-by-step process: gather your documents, sit a knowledge test if required, complete a hazard perception and/or practical test if required, then receive your Victorian licence.</div></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">Do I need a driving test to convert my licence in Victoria?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">Only if your licence is not from a recognised country. Everyone else needs the knowledge test, hazard perception test and drive test.</div></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">What is the recognised country driving licence list for Victoria?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">It includes the UK, Ireland, the USA, Canada, New Zealand, Singapore, Japan and most of Western Europe. The full list is in the table above. Holders of a full licence from these countries can generally swap it for a Victorian licence without a test.</div></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">What happened to Experienced Driver Recognition?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="faq-a"><div class="faq-a-inner">It ended in Victoria on 30 April 2025. Drivers from countries that used to be on that list now follow the same process as other non-recognised countries.</div></div>
        </div>
      </div>
    </div>
  </section>''',
])
CHECKER_BODY = CHECKER_BODY.format(country_links=COUNTRY_LINKS_HTML)

checker_html = page_shell(
    title="Overseas Licence Conversion Checker | Victoria Rules | XDS",
    description="Find out free if you can convert your overseas licence directly, or need a knowledge/practical test in Victoria. Check your tier and requirements now.",
    depth=0,
    body_content=CHECKER_BODY,
    page_key="licence-checker",
    breadcrumbs=[("Licence Checker", None)],
)
open(os.path.join(OUT, "licence-checker.html"), "w").write(checker_html)
print("licence-checker.html written:", len(checker_html), "bytes")

# ============================================================
# CONTACT US PAGE
# ============================================================
CONTACT_BODY = '\n  '.join([
    '''<section class="page-hero">
    <div class="container">
      <h1>Contact X Zavier Driving School</h1>
      <p>Questions about lessons, test packages, or which VicRoads test centre suits you? Reach us on WhatsApp, phone, email, or send an enquiry below.</p>
    </div>
  </section>''',
    trust_section_html(),
    '''<section class="block">
    <div class="container">
      <div class="contact-grid">
        <div>
          <div class="section-title" style="text-align:left;margin-bottom:10px">
            <span class="eyebrow">Get In Touch</span>
            <h2>Ways to Reach Us</h2>
          </div>
          <p style="color:var(--muted);font-size:.9rem">We usually reply within the hour during business hours. WhatsApp is the fastest way to lock in a lesson time.</p>
          <div class="contact-methods">
            <a class="contact-method" target="_blank" rel="noopener" href="https://wa.me/61434538142?text=Hi%20XDS!%20I'd%20like%20to%20get%20in%20touch.">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm5.8 14.2c-.2.7-1.4 1.3-2 1.4-.5.1-1.1.1-1.8-.1-.4-.1-1-.3-1.7-.6-3-1.3-4.9-4.3-5.1-4.5-.1-.2-1.2-1.6-1.2-3.1s.8-2.2 1-2.5c.3-.3.6-.4.8-.4h.6c.2 0 .5 0 .7.5.3.7.9 2.2 1 2.4.1.2.1.4 0 .6-.1.2-.2.3-.4.5l-.5.6c-.2.2-.3.4-.1.7.2.3.9 1.5 1.9 2.4 1.3 1.2 2.4 1.5 2.7 1.7.3.2.5.1.7-.1l.9-1c.2-.3.5-.2.8-.1.3.1 2 1 2.3 1.1.3.2.5.2.6.3.1.2.1.9-.1 1.6z"/></svg>
              <div><strong>WhatsApp</strong><span>0434 538 142 (fastest response)</span></div>
            </a>
            <a class="contact-method" href="tel:0434538142">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
              <div><strong>Call or Text</strong><span>0434 538 142</span></div>
            </a>
            <a class="contact-method" href="mailto:xzavierdrivingschool@gmail.com">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 4h16a1 1 0 011 1v14a1 1 0 01-1 1H4a1 1 0 01-1-1V5a1 1 0 011-1zm1 2v.6l7 4.7 7-4.7V6H5zm14 2.3l-6.5 4.3a1 1 0 01-1 0L5 8.3V18h14V8.3z"/></svg>
              <div><strong>Email</strong><span>xzavierdrivingschool@gmail.com</span></div>
            </a>
            <a class="contact-method" target="_blank" rel="noopener" href="https://share.google/PSBVWeY83VacVhKtu">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6 6.6.7-5 4.4 1.5 6.5L12 16.8 6 19.6l1.5-6.5-5-4.4 6.6-.7z"/></svg>
              <div><strong>Google Business Profile</strong><span>4.9&#9733; &middot; 105+ verified reviews</span></div>
            </a>
            <a class="contact-method" target="_blank" rel="noopener" href="https://www.facebook.com/meddii.sha/">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1.5 8h1.8v2.2h-1.8V21h-2.4v-8.8H9.7V10h1.4V8.7c0-1.9 1-3 3.2-3h1.8v2.2h-1.2c-.6 0-1.4.2-1.4 1V10z"/></svg>
              <div><strong>Instructor Facebook</strong><span>Medii Sha, VicRoads ADI Accredited</span></div>
            </a>
          </div>
          <div class="info-card" style="margin-top:20px">
            <h3 style="margin-bottom:10px;color:var(--navy)">Service Areas</h3>
            <p style="font-size:.86rem;color:var(--muted);margin-bottom:10px">Lessons across Dandenong and South East Melbourne, with VicRoads test preparation for:</p>
            <ul class="bullet-list">
              <li><a href="drive-test-frankston.html">Frankston</a></li>
              <li><a href="drive-test-mooroolbark.html">Mooroolbark</a></li>
              <li><a href="drive-test-pakenham.html">Pakenham</a></li>
              <li><a href="drive-test-heatherton.html">Heatherton</a></li>
            </ul>
          </div>
        </div>

        <div class="tool-card" style="padding:30px">
          <h3 style="margin-bottom:6px">Send Us an Enquiry</h3>
          <p style="color:var(--muted);font-size:.86rem;margin-bottom:20px">Fill in your details and we&rsquo;ll reply by WhatsApp or email, usually within the hour.</p>
          <div id="pcFormWrap">
            <form id="pcForm" onsubmit="submitContactForm(event,'pc')">
              <div class="form-field">
                <label for="pcName">Full name</label>
                <input type="text" id="pcName" required placeholder="Your name">
              </div>
              <div class="form-field">
                <label for="pcPhone">Phone number</label>
                <input type="tel" id="pcPhone" required placeholder="04xx xxx xxx">
              </div>
              <div class="form-field">
                <label for="pcInterest">I&rsquo;m interested in</label>
                <select id="pcInterest">
                  <option>Single Lesson</option>
                  <option>5-Lesson Pass</option>
                  <option>Express Test Package</option>
                  <option>Ultimate Test Pass Pack</option>
                  <option>Gift Voucher</option>
                  <option>General enquiry</option>
                </select>
              </div>
              <div class="form-field">
                <label for="pcMessage">Message (optional)</label>
                <textarea id="pcMessage" rows="4" placeholder="Tell us a bit about what you need"></textarea>
              </div>
              <button type="submit" class="btn btn-red btn-block">Send Enquiry</button>
              <p class="form-note">Prefer WhatsApp? <a href="https://wa.me/61434538142" target="_blank" rel="noopener" style="color:var(--red);font-weight:700">Chat with us instantly &rarr;</a></p>
            </form>
          </div>
          <div class="form-success" id="pcFormSuccess">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm-1.2 14.4l-4.2-4.2 1.4-1.4 2.8 2.8 6-6 1.4 1.4z"/></svg>
            <h3 style="color:var(--navy);margin-bottom:8px">Thanks, we&rsquo;ll be in touch!</h3>
            <p style="color:var(--muted);font-size:.88rem">For a faster response, message us directly on <a href="https://wa.me/61434538142" target="_blank" rel="noopener" style="color:var(--red);font-weight:700">WhatsApp</a>.</p>
          </div>
        </div>
      </div>
    </div>
  </section>''',
])

contact_html = page_shell(
    title="Contact X Zavier Driving School | Book a Lesson | XDS",
    description="Contact X Zavier Driving School by WhatsApp, phone, email, or send an online enquiry. VicRoads ADI accredited instructors serving Dandenong and South East Melbourne.",
    depth=0,
    body_content=CONTACT_BODY,
    page_key="contact-us",
    breadcrumbs=[("Contact", None)],
)
open(os.path.join(OUT, "contact-us.html"), "w").write(contact_html)
print("contact-us.html written:", len(contact_html), "bytes")

# ============================================================
# GENERATE ALL COUNTRY-SPECIFIC PAGES
# ============================================================
for c in COUNTRIES:
    country_page(c)

# ============================================================
# AREA / SUBURB LANDING PAGES
# ============================================================
def suburb_page(suburb):
    slug = slugify(suburb)
    profile = SUBURB_PROFILES[suburb]
    centre_name, centre_href = SUBURB_TEST_CENTRE[suburb]
    cg = CENTRE_GEO[centre_name]
    centre_km = round(haversine_km(SUBURB_COORDS[suburb], (cg["lat"], cg["lon"])))
    nearest20 = nearest_n_suburbs(suburb, 5)
    wikidata = SUBURB_WIKIDATA.get(suburb)
    lat, lon = SUBURB_COORDS[suburb]
    map_query = suburb.replace(" ", "+") + "+VIC+Australia"

    is_own_centre = (suburb == centre_name)
    centre_line = (
        "VicRoads {c} ({addr}) is right here in {s}, so most local learners sit their test close to home.".format(c=centre_name, s=suburb, addr=cg["address"])
        if is_own_centre else
        "Most {s} learners sit their test at <a href=\"{href}\">VicRoads {c}</a> ({addr}), roughly {km} km away in a straight line.".format(s=suburb, href=centre_href, c=centre_name, addr=cg["address"], km=centre_km)
    )

    hero = '''<section class="page-hero">
    <div class="container">
      <h1>Driving Lessons in {suburb}</h1>
      <p>Driving lessons in {suburb} with pickup from home, school or work, and test preparation for VicRoads {centre}.</p>
      {byline}
    </div>
  </section>'''.format(suburb=suburb, byline=BYLINE, centre=centre_name)

    intro = '''<section class="block">
    <div class="container" style="max-width:800px">
      <p style="font-size:1rem;color:#334155">{intro}</p>
    </div>
  </section>'''.format(intro=profile["intro"])

    roads_html = "".join('<li>{0}</li>'.format(r) for r in profile["roads"])
    local_knowledge = '''<section class="block">
    <div class="container" style="max-width:800px">
      <div class="section-title"><h2>What You Will Practise in {suburb}</h2></div>
      <ul class="bullet-list">
        {roads}
      </ul>
    </div>
  </section>'''.format(suburb=suburb, roads=roads_html)

    centre_card = '''<section class="block block-alt">
    <div class="container">
      <div class="info-grid">
        <div class="info-card">
          <h2><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 00-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 00-7-7z"/></svg>Nearest VicRoads Test Centre</h2>
          <p style="font-size:.9rem;color:#334155">{centre_line}</p>
          <div style="margin-top:14px"><a href="{href}" class="tool-link">View the full {c} test centre guide &rarr;</a></div>
        </div>
        <div class="info-card">
          <h3 style="margin-bottom:10px">Our Tip for {suburb} Learners</h3>
          <p style="font-size:.9rem;color:#334155">{tip}</p>
        </div>
      </div>
    </div>
  </section>'''.format(centre_line=centre_line, href=centre_href, c=centre_name, suburb=suburb, tip=profile["tip"])

    lessons_section = '''<section class="block block-alt">
    <div class="container" style="max-width:800px">
      <div class="section-title"><h2>Lessons and Prices for {suburb} Learners</h2></div>
      <p style="font-size:.95rem;color:#334155;margin-bottom:12px">All our lessons are automatic, in a dual-control car, and focused on one thing: getting you through your VicRoads test. Our students have a 99% pass rate.</p>
      <ul class="bullet-list">
        <li><strong>Single lesson:</strong> $70, with pickup in {suburb}.</li>
        <li><strong>5-Lesson Pass:</strong> $325.</li>
        <li><strong>Express Test Package:</strong> $220, including use of our dual-control car for your test at VicRoads {c}.</li>
        <li><strong>Ultimate Test Pass Pack:</strong> $560.</li>
      </ul>
      <p style="font-size:.9rem;color:#334155;margin-top:12px">If you are under 21, VicRoads needs you to log 120 hours of supervised driving, including 20 hours at night, before your drive test. Lessons with us count towards those hours. VicRoads test and booking fees are paid separately. See <a href="index.html#packages">full package details</a>.</p>
    </div>
  </section>'''.format(suburb=suburb, c=centre_name)

    map_section = '''<section class="block">
    <div class="container">
      <div class="section-title"><h2>Map of {suburb}</h2></div>
      <div class="map-embed" style="border-radius:12px;overflow:hidden;box-shadow:0 6px 20px rgba(15,23,42,.1)">
        <iframe src="https://www.google.com/maps?q={q}&output=embed" width="100%" height="360" style="border:0;display:block" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="{suburb} service area map"></iframe>
      </div>
    </div>
  </section>'''.format(suburb=suburb, q=map_query)

    faq_extra = [
        ("Which VicRoads test centre will I be tested at from {suburb}?".format(suburb=suburb),
         centre_line + " You can book any centre you like, but it usually makes sense to test where you have practised."),
        ("How many lessons will I need?",
         "It depends on how much driving you have already done. After your first lesson in {suburb} we will tell you honestly what you need to work on and roughly how many lessons that will take.".format(suburb=suburb)),
        ("Can I use your car for my test?",
         "Yes. Our Express Test Package and Ultimate Test Pass Pack include use of our dual-control car for your test at VicRoads {c}.".format(c=centre_name)),
    ]
    nap_faq = nap_faq_section(suburb, extra_faqs=faq_extra)

    area_served_json = ", ".join('"{0}"'.format(n) for n in nearest20)
    sameas = ['"https://share.google/PSBVWeY83VacVhKtu"']
    if wikidata:
        sameas.append('"https://www.wikidata.org/wiki/{0}"'.format(wikidata))
    local_schema = '''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "DrivingSchool",
  "name": "X Zavier Driving School",
  "alternateName": "XDS",
  "telephone": "+61434538142",
  "email": "xzavierdrivingschool@gmail.com",
  "url": "https://drivetestvic.com.au/{href}",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "{addr}",
    "addressRegion": "VIC",
    "addressCountry": "AU"
  }},
  "geo": {{
    "@type": "GeoCoordinates",
    "latitude": {lat},
    "longitude": {lon}
  }},
  "description": "Driving lessons and VicRoads test preparation in {suburb}, servicing nearby South East Melbourne suburbs.",
  "areaServed": [{areas}],
  "sameAs": [{sameas}]
}}
</script>
'''.format(href=area_page_href(suburb), addr=NAP_ADDRESS, lat=lat, lon=lon, suburb=suburb,
           areas=area_served_json, sameas=", ".join(sameas))

    body = '\n  '.join([hero, intro, local_knowledge, centre_card, lessons_section, map_section, nap_faq])

    html = page_shell(
        title="Driving Lessons in {suburb} | X Zavier Driving School".format(suburb=suburb),
        description="Driving lessons in {suburb} with pickup included. What you will practise on local roads, and how we prepare you for VicRoads {c}.".format(suburb=suburb, c=centre_name),
        depth=0,
        body_content=body,
        page_key="area-" + slug,
        schema=local_schema,
        breadcrumbs=[("Areas We Serve", "index.html#areas"), (suburb, None)],
    )
    fname = area_page_href(suburb)
    open(os.path.join(OUT, fname), "w").write(html)
    print(fname, "written:", len(html), "bytes")


for s in AREA_SUBURBS:
    suburb_page(s)

# ============================================================
# SITEMAP.XML + ROBOTS.TXT
# Generated from the actual set of .html files written above, so it never
# drifts out of sync with the real page list (no hardcoded page names).
# ============================================================
import datetime
import glob

SITE_ROOT = "https://drivetestvic.com.au"

def build_sitemap_and_robots():
    html_files = sorted(
        os.path.basename(f) for f in glob.glob(os.path.join(OUT, "*.html"))
    )
    today = datetime.date.today().isoformat()

    def priority_for(fname):
        if fname == "index.html":
            return "1.0"
        if fname.startswith("drive-test-"):
            return "0.9"
        if fname.startswith("area-"):
            return "0.8"
        return "0.6"

    url_entries = []
    for fname in html_files:
        loc = SITE_ROOT + "/" + ("" if fname == "index.html" else fname)
        url_entries.append(
            "  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <priority>{priority}</priority>\n  </url>".format(
                loc=loc, lastmod=today, priority=priority_for(fname)
            )
        )

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(url_entries)
        + "\n</urlset>\n"
    )
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sitemap)
    print("sitemap.xml written:", len(sitemap), "bytes,", len(html_files), "urls")

    robots = (
        "User-agent: *\n"
        "Allow: /\n\n"
        "Sitemap: {root}/sitemap.xml\n".format(root=SITE_ROOT)
    )
    open(os.path.join(OUT, "robots.txt"), "w").write(robots)
    print("robots.txt written:", len(robots), "bytes")

build_sitemap_and_robots()
