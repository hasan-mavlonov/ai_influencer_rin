from instagrapi import Client
from dotenv import load_dotenv
import os
import time

load_dotenv()

username = os.getenv("INSTA_USERNAME")
password = os.getenv("INSTA_PASSWORD")

def login():
    cl = Client()
    cl.login(username, password)
    print(f"✅ Logged in as {username}")
    return cl


def post_to_instagram(image_path: str, caption: str):
    cl = login()
    try:
        media = cl.photo_upload(image_path, caption)
        print(f"✅ Successfully posted to Instagram: {media.dict().get('code')}")
        return media
    except Exception as e:
        print("❌ Error posting:", e)
    finally:
        time.sleep(3)
        cl.logout()
