# 🔍 LinkedIn Executive Scraper

This project is designed to find and extract executive LinkedIn profiles for a list of companies by:
1. Searching Google using company names and executive keywords.
2. Extracting top 5 LinkedIn profile URLs per company.
3. Parsing and cleaning name, company, and LinkedIn URL data.

---

## 📂 Folder Structure

- `GoogleScrapforURLs.py` – uses Google CSE API to search LinkedIn URLs for executives
- `linkedinurlextract.py` – extracts clean name, company, and LinkedIn URL from results
- `all-other-companies.csv` – input file with company names
- `executive_profiles_all.csv` – output with top 5 LinkedIn URLs per company
- `linkedin_profiles_extracted.csv` – final structured data with names and LinkedIn links

---

## 🔁 Workflow

### 1. `GoogleScrapforURLs.py`
- Reads `all-other-companies.csv` (list of companies)
- Searches Google with each company name + LinkedIn + executive keywords: “CEO” OR “CIO” OR “CTO” OR “COO” OR “CMO” OR “VP” OR
“Vice President” OR “Senior Vice President” OR “Director” OR
“Sr. Director” OR “Executive Director” OR “Chief Data Officer” OR “VP Data”


- Extracts top 5 profile URLs per company
- Stores results in `executive_profiles_all.csv`

> 🔑 Requires: Google Custom Search API key and CSE ID

---

### 2. `linkedinurlextract.py`
- Reads `executive_profiles_all.csv`
- Extracts:
- Company name
- First name
- Last name
- LinkedIn URL
- Stores structured output in `linkedin_profiles_extracted.csv`

---

## 📊 Output Summary

- `executive_profiles_all.csv`: Raw Google search results with LinkedIn profile links
- `linkedin_profiles_extracted.csv`: Clean and structured executive data

---

## 🚀 Run Order

```bash
python GoogleScrapforURLs.py
python linkedinurlextract.py
