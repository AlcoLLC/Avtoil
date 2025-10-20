import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import time

JSON_KEY_FILE = 'avtoil-475708-217f43591fff.json'
API_SCOPE = 'https://www.googleapis.com/auth/indexing'
ENDPOINT = 'https://indexing.googleapis.com/v3/urlNotifications:publish'

SITE_DOMAIN = "https://avtoil.de" 

LANGUAGE_PREFIX = "" 

STATIC_PATHS = [
    "/",
    "/submit-review/", 
    "/about/",
    "/brands/",
    "/contact/", 
    "/faq/",
    "/news/",
    "/partnership/",
    "/product/",
    "/search/",
    "/services/",
]

def get_credentials():
    try:
        creds = service_account.Credentials.from_service_account_file(
            JSON_KEY_FILE, scopes=[API_SCOPE])
        if not creds.valid:
            creds.refresh(Request())
        return creds
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

def submit_url_to_google(url_to_submit, credentials):
    session = requests.Session()
    session.auth = (f"Bearer {credentials.token}")
    
    payload = {
        "url": url_to_submit,
        "type": "URL_UPDATED"
    }

    try:
        response = session.post(ENDPOINT, json=payload)
        response.raise_for_status()
        return True

    except requests.exceptions.HTTPError as e:
        return False
    except Exception as e:
        return False

if __name__ == "__main__":
    creds = get_credentials()
    
    if creds:
        full_urls = [f"{SITE_DOMAIN}{LANGUAGE_PREFIX}{path}" for path in STATIC_PATHS]
        
        for i, url in enumerate(full_urls):
            print(f"[{i+1}/{len(full_urls)}] Gönderiliyor...")
            submit_url_to_google(url, creds)
            time.sleep(0.2)
        print("\nStatik URL gönderme işlemi tamamlandı.")