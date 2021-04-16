# Safeway-Vax-Checker
A script to check for COVID-19 vaccine availability at a Safeway near you.

## Usage
`usage: vax-check.py [-h] [--max-distance MAX_DISTANCE] [--check-interval CHECK_INTERVAL] [--check-once] latitude longitude`

Check interval is in seconds (default: 10s), max distance is in kilometers (default: 20km)

Works with Python 2 or 3, no dependencies!

Example:
`python vax-check.py 37.40295 -122.11532 --max-distance 20`
