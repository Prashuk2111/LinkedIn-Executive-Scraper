import pandas as pd
import requests
import time
import random


# # Path to the Excel file (update if needed)
# excel_file_path = "All-Sectors-Companies-Tabs=3300.xlsx"
# # Path for the output CSV file
# csv_file_path = "All-Sectors-Companies-Tabs.csv"

# # Read the Excel file
# df = pd.read_excel(excel_file_path)

# # Write the DataFrame to a CSV file without the index column
# df.to_csv(csv_file_path, index=False)

# # print(f"CSV file saved as {csv_file_path}")

# ---------------------------- CONFIG ----------------------------
CSV_FILE_PATH = "All-Other-Companies.csv"  # Input CSV file with company names
OUTPUT_CSV = "executive_profiles_all.csv"               # Output CSV file to save results
NUM_RESULTS = 5                                     # Number of results to fetch per company
MAX_RETRIES = 3                                     # Number of attempts per search before recording an error
EXECUTIVE_KEYWORDS = '"CEO" OR "CIO" OR "CTO" OR "COO" OR "CMO" OR "VP" OR "Vice President" OR "Senior Vice President" OR "Director" OR "Sr. Director" OR "Executive Director OR "Chief Data Officer" OR "VP Data"'
MIN_DELAY = 1                                    # Minimum random delay in seconds between companies
MAX_DELAY = 4                                     # Maximum random delay in seconds between companies

# Google Custom Search API settings
API_KEY = "AIzaSyC75wVl0LxgpPN8gwovgLhcXkd9cps5mxM"  # Your Custom Search API key
CSE_ID = "3561b671f01834758"                           # Your Custom Search Engine ID
# ----------------------------------------------------------------

def random_delay():
    """Sleep for a random delay between MIN_DELAY and MAX_DELAY seconds."""
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    print(f"⏳ Waiting for {delay:.2f} seconds...\n")
    time.sleep(delay)

def load_company_names(filepath):
    """Load and return a list of company names from a CSV file."""
    try:
        df = pd.read_csv(filepath)
        companies = df['Company Name'].dropna().tolist()
        return companies
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return []

def google_search(query, api_key, cse_id, num_results=5):
    """Perform a Google Custom Search and return the list of URLs."""
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "num": num_results
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    results = response.json()
    # Extract URLs from search results
    urls = [item["link"] for item in results.get("items", [])]
    return urls

def search_executives(companies, api_key, cse_id):
    """Search for LinkedIn profiles for each company using Google Custom Search API."""
    results = []
    
    for index, company in enumerate(companies):
        # Build the query to target LinkedIn profiles for top executives
        query = f'site:linkedin.com/ "{company}" ({EXECUTIVE_KEYWORDS})'
        print(f"[{index+1}/{len(companies)}] 🔍 Searching for executives at: {company}")
        
        # Retry logic with exponential backoff
        for attempt in range(MAX_RETRIES):
            try:
                search_results = google_search(query, api_key, cse_id, num_results=NUM_RESULTS)
                for url in search_results:
                    results.append({
                        'Company Name': company,
                        'LinkedIn URL': url
                    })
                # Break out if successful
                break
            except Exception as e:
                wait_time = 5 * (attempt + 1)
                print(f"⚠️  Attempt {attempt+1} failed for '{company}': {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                if attempt == MAX_RETRIES - 1:
                    results.append({
                        'Company Name': company,
                        'LinkedIn URL': f'Error: {str(e)}'
                    })
        random_delay()
    
    return results

def save_results(results, output_path):
    """Save the search results to a CSV file."""
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)
    print(f"\n✅ Search completed. Results saved to: '{output_path}'")

# ---------------------------- MAIN ----------------------------
if __name__ == "__main__":
    print("🚀 Starting Executive Finder using Google Custom Search API...\n")

    companies = load_company_names(CSV_FILE_PATH)
    if not companies:
        print("❌ No companies to process.")
        exit()

    exec_results = search_executives(companies, API_KEY, CSE_ID)
    save_results(exec_results, OUTPUT_CSV)