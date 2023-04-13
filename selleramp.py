from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os
from dotenv import load_dotenv

load_dotenv()

# Set up the Chrome browser driver
driver = webdriver.Chrome()

# Navigate to the login page
driver.get('https://sas.selleramp.com/site/login')

# Wait for the login page to load
time.sleep(2)

# Fill in the login form fields
username_field = driver.find_element(By.ID, 'loginform-email')
password_field = driver.find_element(By.ID, 'loginform-password')

username_field.send_keys(os.environ.get('SELLERAMP_USER'))
password_field.send_keys(os.environ.get('SELLERAMP_PASS'))


login_button = driver.find_element(By.NAME, 'login-button')
login_button.click()

# Wait for the page to load after logging in
time.sleep(5)

with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(['ASIN', 'ROI', 'Alert', 'BSR', 'Est. Sales', 'Max Cost', 'Cost Price', 'Sales Price', 'Profit', 'Profit Margin', 'Breakeven'])

    # Read the codes from the CSV file
    with open('asins.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            asin = row[0]

            # Navigate to the page with the data you want to scrape
            driver.get('https://sas.selleramp.com/sas/lookup?SasLookup%5Bsearch_term%5D=' + asin)

            try:
                # Wait for the Qi ROI element to be visible
                qi_alert_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'qi-alert-not')))

                qi_alert_value = qi_alert_element.text


                qi_salespermo_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'estimated_sales_per_mo')))

                qi_salespermo_value = qi_salespermo_element.text


                qi_bsr_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'qi-bsr')))

                qi_bsr_value = qi_bsr_element.text


                qi_maxcost_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'qi-max-cost')))

                qi_maxcost_value = qi_maxcost_element.text


                qi_costprice_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'cost')))

                qi_costprice_value = qi_costprice_element.get_attribute('value')


                qi_salesprice_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'sale_price')))

                qi_salesprice_value = qi_salesprice_element.get_attribute('value')


                qi_profit_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'qi-profit')))

                qi_profit_value = qi_profit_element.text


                qi_profitmargin_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'qi-profit-margin')))

                qi_profitmargin_value = qi_profitmargin_element.text



                qi_roi_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'qi-roi')))

                qi_roi_value = qi_roi_element.text


                qi_breakeven_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'qi-breakeven')))

                qi_breakeven_value = qi_breakeven_element.text

                try:
                    float(qi_roi_value.strip("%"))
                    print(asin, qi_roi_value, qi_alert_value, qi_bsr_value, qi_salespermo_value, qi_maxcost_value,  qi_costprice_value, qi_salesprice_value, qi_profit_value, qi_profitmargin_value, qi_breakeven_value)
                    writer.writerow([asin, qi_roi_value, qi_alert_value, qi_bsr_value, qi_salespermo_value, qi_maxcost_value,  qi_costprice_value, qi_salesprice_value, qi_profit_value, qi_profitmargin_value, qi_breakeven_value])
                except ValueError:
                    print("qi_roi_value is not a float")
            except:
                print("No Results found for this ASIN.")
                continue

# Close the browser window
driver.quit()


# Read the output CSV file into a list of dictionaries
with open('output.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Sort the list of dictionaries by the qi_roi_value (in descending order)
data = sorted(data, key=lambda x: float(x['ROI'].strip('%')), reverse=True)

# Write the sorted data to the output CSV file
with open('output_sorted.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['ASIN', 'ROI', 'Alert', 'BSR', 'Est. Sales', 'Max Cost', 'Cost Price', 'Sales Price', 'Profit', 'Profit Margin', 'Breakeven'])

    # Write the data rows
    for row in data:
        writer.writerow([row['ASIN'], row['ROI'], row['Alert'], row['BSR'], row['Est. Sales'], row['Max Cost'], row['Cost Price'], row['Sales Price'], row['Profit'], row['Profit Margin'], row['Breakeven']])
