#!/usr/bin/env python3 

import csv

# Prompt the user for each argument
url = input("Enter the URL: ")
model = input("Enter the model: ")
year = input("What year is the vehicle?:")
price = input("Enter the price: ")
mileage = input("Enter the mileage: ")
trim = input("Enter the trim: ")
dealer = input("Enter the dealer name: ")
features = input("Enter the features (comma separated): ")
favorite = input("Is it your favorite? (True or False): ") or False

# Create a dictionary of the arguments
kwargs = {'url': url, 'model': model, 'price': price, 'mileage': mileage, 'trim': trim, 'dealer': dealer, 'features': features, 'favorite': favorite, 'year': year}

# Write the dictionary to a CSV file
with open('cars.csv', 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=kwargs.keys())
    if csvfile.tell() == 0:
        writer.writeheader()
    writer.writerow(kwargs)

# Append the dictionary to a log file
with open('cars.log', 'a') as logfile:
    for key, value in kwargs.items():
        logfile.write(f'{key}={value}\n')
