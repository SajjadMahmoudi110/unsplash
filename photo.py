def get_unsplash_photos(username, access_key):
    url = f"https://api.unsplash.com/users/{username}/photos"
    all_photos = []
    page = 1
    per_page = 30

    while True:
        params = {
            'client_id': access_key,
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
