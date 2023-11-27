from bs4 import BeautifulSoup
import cfscrape
import csv
import time

import re
def get(url):
    return BeautifulSoup(cfscrape.create_scraper().get(url).text, 'lxml')

url="https://www.uklandandfarms.co.uk/rural-properties-for-sale/"
soup=get(url)
#print(soup)
while "403 Forbiddein" in soup.text:
    print("Forbidden....Trying again in 10 seconds")
    time.sleep(10)
    soup=get(url)
def total_pages():
    pages=soup.find("div",id="SearchPage")("a")
    text=pages[-1].get("onclick")
    text = 'onPagerClick(255);return false;'
    pattern = r'onPagerClick\((\d+)\);'

    # Use regex to find and capture the numeric value
    match = re.search(pattern, text)

    # Extract the captured number if a match is found
    if match:
        page_number = int(match.group(1))
        print("Number inside onPagerClick:", page_number)
    else:
        print("No number found inside onPagerClick.")
    return page_number

def scrape(soup):
    properties=soup.find("div",id="propertyList")
    items=properties.find("ul")("li")
    for item in items:
        url=item.find("a")["href"]
        heading=item.find("h3")
        description=item.find("p").get_text()
        # Define regex patterns for price, area, and location
        price_pattern = r'£([\d,]+)'
        area_pattern = r'([\d.]+) acres'
        location_pattern = r', (.+)$'  
        input_string=heading.get_text()
        # Use regex to find matches
        price_match = re.search(price_pattern, input_string)
        area_match = re.search(area_pattern, input_string)
        location_match = re.search(location_pattern, input_string)

        # Extract the values if matches are found
        price = price_match.group(1) if price_match else None
        area = area_match.group(1) if area_match else None
        location = location_match.group(1) if location_match else None

        # Print the extracted values
        print("Price:", price)
        print("Area:", area)
        print("Location:", location)
        data={
        "Location":location,
        "Area":area,
        "PriceEUR":price,
        "Description":description,
        "URL":url
        }
        property_data_list.append(data)

# Create a list to store property data as dictionaries
property_data_list = []
for i in range(1,total_pages()):
    url="https://www.uklandandfarms.co.uk/rural-properties-for-sale/page-{i}/"
    while "403 Forbiddein" in soup.text:
        print("Forbidden....Trying again in 10 seconds")
        time.sleep(10)
        soup=get(url)
    scrape(soup)
    time.sleep(10)
csv_filename = "property_data.csv"

# Write the property data to a CSV file
with open(csv_filename, mode='w', newline='') as csv_file:
    fieldnames = ["Location", "Area", "PriceEUR", "Description", "URL"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write the property data rows
    for property_data in property_data_list:
        writer.writerow(property_data)

print(f"Data has been saved to {csv_filename}")




