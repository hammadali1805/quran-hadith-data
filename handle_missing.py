import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# Load the JSON file
def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Save the JSON file
def save_data(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Find missing IDs and IDs with incomplete data
def find_missing_and_incomplete_ids(data, start_id, end_id):
    existing_ids = {entry['id'] for entry in data}
    complete_data_ids = {entry['id'] for entry in data if all(entry.values())}

    missing_ids = set(range(start_id, end_id + 1)) - existing_ids
    incomplete_ids = existing_ids - complete_data_ids

    return missing_ids, incomplete_ids

# Set up Selenium WebDriver options
def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

# Scrape a single hadith
def scrape_hadith(driver, i):
    base_url = "https://sunnah.com/muslim:"
    book_name = "Sahih Muslim"
    url = f"{base_url}{i}"
    hadith_data = None

    try:
        driver.get(url)
        time.sleep(2)  # Allow time for the page to load dynamically

        try:
            # Locate the English hadith container
            hadith_container = driver.find_element(By.CLASS_NAME, "english_hadith_full")

            # Extract narrator
            narrator_element = hadith_container.find_element(By.CLASS_NAME, "hadith_narrated")
            narrator = narrator_element.text.replace("Narrated", "").strip(':').strip()

            # Extract hadith text
            text_element = hadith_container.find_element(By.CLASS_NAME, "text_details")
            hadith_text = text_element.text.strip()

            # Prepare the data
            hadith_data = {
                "id": i,
                "narrator": narrator,
                "text": hadith_text,
                "book": book_name
            }
            print(f"Scraped hadith {i}")
        except NoSuchElementException:
            print(f"No hadith found for id {i}")

    except Exception as e:
        print(f"Error scraping hadith {i}: {e}")

    return hadith_data

# Scrape and update missing and incomplete IDs
def scrape_missing_and_incomplete(file_path, start_id, end_id):
    data = load_data(file_path)
    missing_ids, incomplete_ids = find_missing_and_incomplete_ids(data, start_id, end_id)
    
    print(f"Missing IDs: {missing_ids}")
    print(f"Incomplete IDs: {incomplete_ids}")

    driver = create_driver()
    try:
        for i in missing_ids.union(incomplete_ids):
            new_data = scrape_hadith(driver, i)
            if new_data:
                data = [entry for entry in data if entry['id'] != i]  # Remove old entry if it exists
                data.append(new_data)
    finally:
        driver.quit()

    save_data(data, file_path)
    print("Missing and incomplete IDs processed and updated.")

if __name__ == "__main__":
    file_path = "hadiths.json"  # Path to the JSON file
    start_id = 1  # Adjust according to your dataset
    end_id = 3033  # Adjust according to your dataset

    scrape_missing_and_incomplete(file_path, start_id, end_id)
