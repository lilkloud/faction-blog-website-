import os
import requests
from pathlib import Path

def download_image(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {url}")

def main():
    # Create images directory if it doesn't exist
    Path("app/static/images/categories").mkdir(parents=True, exist_ok=True)
    
    # Download beauty category image
    beauty_url = "https://images.unsplash.com/photo-1596462502278-27bfdc403348"
    download_image(beauty_url, "app/static/images/categories/beauty-category.jpg")
    
    # Download lifestyle category image
    lifestyle_url = "https://images.unsplash.com/photo-1556910639-8e360260247a"
    download_image(lifestyle_url, "app/static/images/categories/lifestyle-category.jpg")
    
    # Create a default avatar if it doesn't exist
    default_avatar = "app/static/images/default-avatar.png"
    if not os.path.exists(default_avatar):
        with open(default_avatar, 'wb') as f:
            f.write(b'')
        print(f"Created {default_avatar}")

if __name__ == "__main__":
    main()
