# Import libraries
import argparse, json, math, sys, time, urllib.request

# Earth radius (km)
EARTH_RADIUS = 6373.0

# Server endpoint
SAFEWAY_ENDPOINT = 'https://s3-us-west-2.amazonaws.com/mhc.cdn.content/vaccineAvailability.json'

def coord_dist(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float-like
        (lat, long)
    destination : tuple of float-like
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = ("48.1372", "11.5756")  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = (float(c) for c in origin)
    lat2, lon2 = (float(c) for c in destination)
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def check_availability(coords, max_dist=20):
    """Check availability based on your location coords (lat, long) and a maximum distance you
    are willing to go (20km by default)"""
    # Get data
    data = json.loads(urllib.request.urlopen(SAFEWAY_ENDPOINT).read())

    # Filter data to available sites
    data = filter(lambda site: site['availability'] != 'no', data)

    # Filter data to distance
    data = filter(lambda site: coord_dist(coords, (site['lat'], site['long'])) < max_dist, data)

    # Return data
    return list(data)


if __name__ == '__main__':
    # Get arguments
    parser = argparse.ArgumentParser(description="Check for vaccine availability near you.")
    parser.add_argument("latitude", help="your latitude")
    parser.add_argument("longitude", help="your longitude")
    parser.add_argument("--max-distance", type=int, default=20, help="max distance to check (km)")
    parser.add_argument("--check-interval", type=int, default=10, help="check interval (seconds)")
    parser.add_argument("--check-once", action="store_true", help="check for availability only once, then exit")
    args = parser.parse_args()

    # Monitor
    while True:
        data = check_availability((args.latitude, args.longitude), max_dist=args.max_distance)
        if not data:
            print("No vaccines near you right now, sorry.")
        for slot in data:
            print(f"Vaccine available near you! To book, go to: {slot['coach_url']}\a\a\a\a\a")
        if args.check_once:
            exit(0)
        time.sleep(args.check_interval)
