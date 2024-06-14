import os
import requests
import numpy as np
import json

# Read Accept and USERNAME from web
Accept = os.getenv('UNSPLASH_Accept')
USERNAME = os.getenv('UNSPLASH_USERNAME')

# Check if Accept and USERNAME are set
if not Accept or not USERNAME:
    print("Please set the UNSPLASH_Accept and UNSPLASH_USERNAME environment variables.")
    exit()

PHOTOS_FILENAME = 'Data.json'

# Function to get all photos from Unsplash API with pagination
def get_unsplash_photos(username, Accept):
    url = f"https://api.unsplash.com/users/{username}/photos"
    all_photos = []
    page = 1
    per_page = 100

    while True:
        params = {
            'client_id': Accept,
            'page': page,
            'per_page': per_page,
            'stats': 'true'
        }
        response = requests.get(url, params=params)
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
    photos = get_unsplash_photos(USERNAME, Accept)
    if not photos:
        print("No photos retrieved. Please check your username and access key.")
        exit()
    save_photos_to_file(photos, PHOTOS_FILENAME)
    print("Fetched photos from Unsplash API and saved to Data.json")

# Sort photos by normalized score and display the results
sorted_photos = sorted(filtered_photos, key=lambda x: x['normalized_score'], reverse=True)
for photo in sorted_photos:
    print(f"Photo URL: https://unsplash.com/photos/{photo['id']}, Views: {photo['statistics']['views']['total']}, Downloads: {photo['statistics']['downloads']['total']}, Normalized Score: {photo['normalized_score']:.2f}")
