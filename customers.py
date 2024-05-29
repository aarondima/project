import csv
customers = []
    
with open("data/customers.csv", newline= '') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        customer = {'name': row['name'], 'phone': row['phone']}
        customers.append(customer)
    for customer in customers:
        print(customer)