import os
import requests
import json
import numpy as np

# Read environment variables for Unsplash API access
ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
USERNAME = os.getenv('UNSPLASH_USERNAME')

# Proxy settings (if required)
http_proxy = "http://10.10.1.10:3128"
https_proxy = "https://10.10.1.11:1080"
ftp_proxy = "ftp://10.10.1.10:3128"

proxies = {
    "http": http_proxy,
    "https": https_proxy,
    "ftp": ftp_proxy
}

# Check if ACCESS_KEY and USERNAME are set
if not ACCESS_KEY or not USERNAME:
    print("Please set the UNSPLASH_ACCESS_KEY and UNSPLASH_USERNAME environment variables.")
    exit()

PHOTOS_FILENAME = 'Data.json'

# Function to get all photos from Unsplash API with pagination
def get_unsplash_photos(username, access_key):
    url = f"https://api.unsplash.com/users/{username}/photos"
    all_photos = []
    page = 1
    per_page = 30  # Unsplash API allows a maximum of 30 per page

    headers = {
        'Authorization': f'Client-ID {access_key}'
    }

    while True:
        params = {
            'page': page,
            'per_page': per_page
        }
        response = requests.get(url, headers=headers, params=params, proxies=proxies)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        photos = response.json()
        if not photos:
            break

        all_photos.extend(photos)
        page += 1

    return all_photos

# Function to save photos to a file
def save_photos_to_file(photos, filename):
    with open(filename, 'w') as f:
        json.dump(photos, f, indent=4)

# Function to load photos from a file
def load_photos_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Load or fetch photos
if os.path.exists(PHOTOS_FILENAME):
    photos = load_photos_from_file(PHOTOS_FILENAME)
    print("Loaded photos from Data.json")
else:
    photos = get_unsplash_photos(USERNAME, ACCESS_KEY)
    if not photos:
        print("No photos retrieved. Please check your username and access key.")
        exit()
    save_photos_to_file(photos, PHOTOS_FILENAME)
    print("Fetched photos from Unsplash API and saved to Data.json")

# Add normalized score if not present
for photo in photos:
    if 'normalized_score' not in photo:
        photo['normalized_score'] = np.random.rand() 

# Sort photos by normalized score and display the results
sorted_photos = sorted(photos, key=lambda x: x['normalized_score'], reverse=True)
for photo in sorted_photos:
    print(f"Photo URL: https://unsplash.com/photos/{photo['id']}, Views: {photo['views']['total']}, Downloads: {photo['downloads']['total']}, Normalized Score: {photo['normalized_score']:.2f}")
