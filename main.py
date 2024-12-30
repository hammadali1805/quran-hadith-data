from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# Define the base URL and book name
base_url = "https://sunnah.com/bukhari:"
book_name = "Sahih al-Bukhari"

# Initialize the data list
hadiths_data = []

try:
    # Start iterating over the hadiths
    i = 1
    while True:
        url = f"{base_url}{i}"
        driver.get(url)
        time.sleep(5)  # Allow time for the page to load dynamically

        try:
            # Locate the English hadith container
            hadith_container = driver.find_element(By.CLASS_NAME, "english_hadith_full")

            # Extract narrator
            narrator_element = hadith_container.find_element(By.CLASS_NAME, "hadith_narrated")
            narrator = narrator_element.text.replace("Narrated", "").strip(':').strip()

            # Extract hadith text
            text_element = hadith_container.find_element(By.CLASS_NAME, "text_details")
            hadith_text = text_element.text.strip()

            # Append the data
            hadiths_data.append({
                "id": i,
                "narrator": narrator,
                "text": hadith_text,
                "book": book_name
            })
            print(f"Scraped hadith {i}")
        except NoSuchElementException:
            print(f"No hadith found for id {i}. Stopping.")
            break

        # Increment the counter
        i += 1

finally:
    # Close the WebDriver
    driver.quit()

# Save the data to a JSON file
with open("hadiths.json", "w", encoding="utf-8") as f:
    json.dump(hadiths_data, f, ensure_ascii=False, indent=4)

print(f"Scraping completed {len(hadiths_data)}. Data saved to hadiths.json")
