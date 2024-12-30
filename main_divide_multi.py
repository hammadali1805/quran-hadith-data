from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import time
from multiprocessing import Process, Manager

# Set up Selenium WebDriver options
def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

# Define the base URL and book name
base_url = "https://sunnah.com/muslim:"
book_name = "Sahih Muslim"

# Function to scrape a range of hadiths using a single driver
def scrape_hadiths(driver, task_range, result_list):
    for i in task_range:
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

                # Append the data to the shared list
                result_list.append(hadith_data)
            except NoSuchElementException:
                print(f"No hadith found for id {i}")

        except Exception as e:
            print(f"Error scraping hadith {i}: {e}")

# Function to manage a single browser instance and its assigned tasks
def process_task(task_range, result_list):
    driver = create_driver()
    try:
        scrape_hadiths(driver, task_range, result_list)
    finally:
        driver.quit()

if __name__ == "__main__":
    # Define range of hadiths to scrape
    start_id = 1
    end_id = 3033  # Change this to the desired maximum id
    num_processes = 20

    # Create ranges for each process
    task_ranges = [
        range(start_id + i * (end_id - start_id + 1) // num_processes,
              start_id + (i + 1) * (end_id - start_id + 1) // num_processes)
        for i in range(num_processes)
    ]

    # Manager list to collect results
    manager = Manager()
    result_list = manager.list()

    # Create and start processes
    processes = []
    for task_range in task_ranges:
        p = Process(target=process_task, args=(task_range, result_list))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Save the data to a JSON file
    with open("hadiths.json", "w", encoding="utf-8") as f:
        json.dump(list(result_list), f, ensure_ascii=False, indent=4)

    print(f"Scraping completed {len(list(result_list))}. Data saved to hadiths.json")
