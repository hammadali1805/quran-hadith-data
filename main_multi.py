from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import time
from multiprocessing import Pool, Manager

# Set up Selenium WebDriver options
def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

# Define the base URL and book name
base_url = "https://sunnah.com/bukhari:"
book_name = "Sahih al-Bukhari"

# Function to scrape a single hadith
def scrape_hadith(i):
    driver = create_driver()
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

    finally:
        driver.quit()

    return hadith_data

# Multiprocessing function
def scrape_hadiths_in_range(start, end):
    with Pool(10) as pool:  # Use 10 processes
        results = pool.map(scrape_hadith, range(start, end + 1))
    return [r for r in results if r is not None]

if __name__ == "__main__":
    # Define range of hadiths to scrape
    start_id = 1
    end_id = 7563  # Change this to the desired maximum id

    # Use a Manager list to store results
    hadiths_data = scrape_hadiths_in_range(start_id, end_id)

    # Save the data to a JSON file
    with open("hadiths.json", "w", encoding="utf-8") as f:
        json.dump(hadiths_data, f, ensure_ascii=False, indent=4)

    print("Scraping completed. Data saved to hadiths.json")
