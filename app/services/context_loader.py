import json
import os

# Load the cleaned scraped content
DATA_PATH = os.getenv("SCRAPED_DATA_PATH", "est_content.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    scraped_data = json.load(f)

# Turn into a list of (url, text)
documents = [(items["source"], items["content"]) for items in scraped_data]
#print(documents[0])  # Print the first document for verification