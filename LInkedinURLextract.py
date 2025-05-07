import requests
import csv
import time
import random
from bs4 import BeautifulSoup

# File paths
input_file = "executive_profiles.csv"         # CSV file containing LinkedIn URLs and company names
output_file = "linkedin_profiles_extracted.csv" # CSV file to save extracted data

# Custom headers to mimic a browser request.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

profiles_data = []

# Read URLs and company names from the input CSV file.
with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Retrieve URL and company from the CSV row.
        linkedin_url = row.get("linkedin_url") or row.get("LinkedIn URL") or ""
        company = row.get("company") or row.get("Company") or ""
        
        # Clean up the URL and fix its format if missing scheme.
        linkedin_url = linkedin_url.strip()
        if linkedin_url and not linkedin_url.startswith("http"):
            linkedin_url = "https://" + linkedin_url
        
        # Skip rows with an invalid URL.
        if not linkedin_url.startswith("http"):
            print("Skipping invalid URL:", linkedin_url)
            continue
        
        print("Processing:", linkedin_url)
        try:
            response = requests.get(linkedin_url, headers=headers)
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract the full name from an <h1> element.
                name_element = soup.find('h1')
                if name_element:
                    full_name = name_element.get_text(strip=True)
                    name_parts = full_name.split()
                    first_name = name_parts[0] if name_parts else None
                    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else None
                else:
                    first_name = last_name = None

                # Append the extracted data, copying company name directly from the CSV.
                profiles_data.append({
                    "first_name": first_name,
                    "last_name": last_name,
                    "company": company,
                    "linkedin_url": linkedin_url,
                })
            else:
                print(f"Failed to retrieve {linkedin_url} Status code: {response.status_code}")
        except Exception as e:
            print(f"Error processing {linkedin_url} Error: {e}")

        # Add a random delay between requests to reduce the chance of being blocked.
        sleep_time = random.uniform(3, 7)  # Random delay between 3 and 7 seconds.
        print(f"Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

# Write the extracted data into a CSV file.
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["first_name", "last_name", "company", "linkedin_url"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(profiles_data)

print("Data extraction complete. Results saved to", output_file)