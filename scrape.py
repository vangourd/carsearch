#!/usr/bin/env python3

import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import csv
import re

def parse_carsdotcom(soup):
    # Extract the listing title and split it into components
    title = soup.select_one('.listing-title').text.strip()
    year = title.split(' ')[0]
    manufacturer = title.split(' ')[1]
    model = title.split(' ')[2]
    trim = ' '.join(title.split(' ')[3:])

    # Extract the mileage
    mileage = soup.select_one('.listing-mileage').text.strip()

    # Extract the price
    price = re.sub(r"[^\d]", "", soup.select_one('.primary-price').text.strip())

    dealer = soup.select_one('.seller-name').text.strip()

    # Return the extracted fields as a tuple
    return {
        'year': year, 
        'manufacturer': manufacturer, 
        'model': model, 
        'trim': trim, 
        'mileage': mileage, 
        'price': price, 
        'dealer': dealer
    }

def main():
    # Define the list of supported car sites and their corresponding parser functions
    car_sites = {
        'cars.com': parse_carsdotcom,
        # Add more car sites and parser functions as needed
    }

    # Prompt the user for a url to scrape
    url = input('Enter the url to scrape: ')

    # Extract the base domain from the url
    parsed_url = urlparse(url)
    base_domain = parsed_url.netloc.split('.')[-2] + '.' + parsed_url.netloc.split('.')[-1]

    # Check if the base domain is supported by a parser function
    if base_domain in car_sites:
        # Call the appropriate parser function for the car site
        parser_function = car_sites[base_domain]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        results_dict = parser_function(soup)
        results_dict['url'] = url
        print(results_dict.keys())
        with open('cars.csv', 'a', newline='') as csvfile:
            fieldnames = results_dict.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write headers if the file is empty
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow({
                'year': results_dict.get('year'), 
                'manufacturer': results_dict.get('manufacturer'), 
                'model': results_dict.get('model'), 
                'trim': results_dict.get('trim'), 
                'mileage': results_dict.get('mileage'), 
                'price': results_dict.get('price'), 
                'dealer': results_dict.get('dealer'),
                'url': results_dict.get('url'),
            })

        print('Data written to car_data.csv')
    else:
        print('Unsupported car site')



main()