import os
import shutil
from pathlib import Path

def setup_images():
    # Create directories if they don't exist
    Path("app/static/profile_pics").mkdir(parents=True, exist_ok=True)
    Path("app/static/images/categories").mkdir(parents=True, exist_ok=True)
    
    # Create default profile picture if it doesn't exist
    default_profile_pic = "app/static/profile_pics/default.jpg"
    if not os.path.exists(default_profile_pic):
        with open(default_profile_pic, 'wb') as f:
            f.write(b'')
    
    # Create default category images using existing images
    default_bg = "app/static/images/default-bg.jpg"
    default_post = "app/static/images/default-post.jpg"
    
    # Create copies with different names for categories
    for category in ['beauty', 'lifestyle']:
        dest = f"app/static/images/categories/{category}-category.jpg"
        if not os.path.exists(dest):
            shutil.copy2(default_bg, dest)
    
    # Ensure hero-bg.jpg exists
    if not os.path.exists("app/static/images/hero-bg.jpg"):
        shutil.copy2(default_bg, "app/static/images/hero-bg.jpg")
    
    # Ensure fashion-category.jpg exists
    if not os.path.exists("app/static/images/fashion-category.jpg"):
        shutil.copy2(default_post, "app/static/images/fashion-category.jpg")

if __name__ == "__main__":
    setup_images()
