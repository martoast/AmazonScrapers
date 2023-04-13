from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os
import re
from dotenv import load_dotenv

load_dotenv()

# Set up the Chrome browser driver
driver = webdriver.Chrome()

# Navigate to the login page
driver.get('https://panel.bookzpro.com/login')

# Wait for the login page to load
time.sleep(2)

# Fill in the login form fields
username_field = driver.find_element(By.ID, 'input-0')
password_field = driver.find_element(By.ID, 'input-2')

username_field.send_keys(os.environ.get('BOOKZ_USER'))
password_field.send_keys(os.environ.get('BOOKZ_PASS'))


login_button = driver.find_element(By.CLASS_NAME, 'v-btn--block')
login_button.click()

# Wait for the page to load after logging in
time.sleep(5)

driver.get('https://panel.bookzpro.com/bookzy/WEB_DEVICE_ID/scan')

# Wait for the login page to load
time.sleep(2)


with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(['ASIN', 'Used', 'New', 'ListPrice' ])

    # Read the codes from the CSV file
    with open('asins.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            asin = row[0]
            try:

                search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'bookzy-search-input')))

                # Type the search query and press Enter
                search_query = asin
                search_box.send_keys(search_query)
                search_box.send_keys(Keys.RETURN)

                time.sleep(3)
                
                 # Wait for the pricing area to be visible
                pricing_area = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'bb-prices-area')))

                # Find the elements for the Used Buy Box, New Buy Box, and List Price
                price_elements = pricing_area.find_elements(By.CLASS_NAME, 'stat-box-value.bb.mx-2')

                # Extract the text from each element
                used_buy_box_text = price_elements[0].text

                # Remove (U) or (V) label from text using regular expression
                used_buy_box = re.sub(r'\((U|V)\)', '', used_buy_box_text).strip()
                new_buy_box = price_elements[1].text
                list_price = price_elements[2].text

                # Write the data to the output file
                writer.writerow([asin, used_buy_box, new_buy_box, list_price])
            except:
                print("No Results found for this ASIN.")
                continue

# Close the browser window
driver.quit()
