import os
from dotenv import load_dotenv
import requests
import csv
import time

# Load environment variables from .env file
load_dotenv()

# Test env vars load properly
# print("PETFINDER_API_KEY:", os.environ.get("PETFINDER_API_KEY"))
# print("PETFINDER_API_SECRET:", os.environ.get("PETFINDER_API_SECRET"))

# Securely get API credentials from environment variables
CLIENT_ID = os.environ.get("PETFINDER_API_KEY")
CLIENT_SECRET = os.environ.get("PETFINDER_API_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Please set the PETFINDER_API_KEY and PETFINDER_API_SECRET environment variables.")

def get_access_token(client_id, client_secret):
    """Obtain an OAuth2 access token from the Petfinder API."""
    auth_url = "https://api.petfinder.com/v2/oauth2/token"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    response = requests.post(auth_url, data=auth_data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    token_info = response.json()
    return token_info["access_token"]

def get_organizations(access_token):
    """Retrieve organizations (shelters) from the Petfinder API using pagination."""
    headers = {"Authorization": f"Bearer {access_token}"}
    base_url = "https://api.petfinder.com/v2/organizations"
    
    organizations = []
    page = 1
    while True:
        params = {"page": page}
        print(f"Fetching page {page}...")
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # If no organizations are returned, exit the loop
        if not data.get("organizations"):
            break

        organizations.extend(data["organizations"])
        
        # Check pagination info to see if we've reached the last page
        pagination = data.get("pagination", {})
        total_pages = pagination.get("total_pages", page)
        if page >= total_pages:
            break
        
        page += 1
        time.sleep(0.2)  # Optional: be polite to the API server
    
    return organizations

def write_csv(organizations, filename="shelters.csv", folder="exports"):
    # Create the folder if it doesn't already exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Construct the full file path
    file_path = os.path.join(folder, filename)

    """Write the organizations data to a CSV file."""
    fieldnames = [
        "id",
        "name",
        "address",  # street address
        "city",
        "state",
        "postcode", # zip code
        "phone",
        "email",
        "website",
        "adoption_url"
    ]
    
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for org in organizations:
            address_info = org.get("address", {})
            writer.writerow({
                "id": org.get("id", ""),
                "name": org.get("name", ""),
                "address": address_info.get("address1", ""),
                "city": address_info.get("city", ""),
                "state": address_info.get("state", ""),
                "postcode": address_info.get("postcode", ""),
                "phone": org.get("phone", ""),
                "email": org.get("email", ""),
                "website": org.get("url", ""),
                "adoption_url": org.get("adoption_url", "")
            })

def main():
    try:
        print("Obtaining access token...")
        token = get_access_token(CLIENT_ID, CLIENT_SECRET)
        print("Access token obtained.\n")
        
        print("Fetching organizations from Petfinder...")
        organizations = get_organizations(token)
        print(f"Retrieved {len(organizations)} organizations.\n")
        
        print("Writing data to CSV...")
        write_csv(organizations) # CSV file will be created in the 'exports' folder
        print("CSV export complete: shelters.csv")
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
