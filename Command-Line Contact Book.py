import json
import re
import csv

# File paths for storing data 
jsonFile="data.json"
csvFile="contacts.csv"

def conDetails():
    # Add a new contact
    Name=input("Enter the name:- ")
    Number=input("Enter the Phone Number:- ")
    Mail=input("Enter the Email:- ")
    Address=input("Enter the Address:- ")

    # Validate phone and email
    if not re.fullmatch(r"\d{10}", Number):
        print("Invalid phone number")
        return
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", Mail):
        print("Invalid Email.")
        return

    # Creating new contact
    Contact={
    "name":Name,
    "number":Number,
    "mail":Mail,
    "address":Address
    }

    # Load existing contacts and append new contact
    data=loadContact()
    data.append(Contact)

    # Save updated list of contact
    saveContact(data)
    print("Contact saved")

# Function to read existing contacts
def loadContact():
    try:
        # Try to open and load existing contact data from JSON file
        with open(jsonFile, "r") as file:
            data = json.load(file)
        # Remember The data is a list
            if not isinstance(data, list):
                print("Corrupted data file. Resetting contacts.")
                return []
            return data
    except FileNotFoundError:
        # Return an empty list if file doesn't exist
        return []
    except json.JSONDecodeError:
        # Handle JSON corruption
        print("JSON decoding failed. Resetting contacts.")
        return []


# Function to save contacts
def saveContact(data):
    # Write contact list to JSON file
    with open(jsonFile,"w") as file:
        json.dump(data, file, indent=4)

# Function to view all contacts
def view():
    # View all contacts
    data=loadContact()
    if not data:
        print("No contact found.")
        return
    # Print each contact
    print("\nSaved contacts:")
    for contact in data:
        print(f"Name:- {contact['name']}, Phone:- {contact['number']}, Email:- {contact['mail']}, Address:- {contact['address']}")

# Function to search contact by name
def searchContact():
    sName=input("Enter name to search:- ").lower()
    data=loadContact()
    # Search for matching names
    found=[c for c in data if c["name"].lower()==sName]
    if found:
        for contact in found:
            print(f"found: Name:- {contact['name']}, Phone:- {contact['number']}, Email:- {contact['mail']}, Address:- {contact['address']}")
    else:
        print("Contact not found")

# Function to edit a contact
def editContact():
    eName = input("Enter name to edit: ").lower()
    data = loadContact()
    for contact in data:
        if contact["name"].lower() == eName:
            # Allow user to update or keep existing values
            contact["name"] = input("Enter new name:- ") or contact["name"]
            contact["number"] = input("Enter new phone number:- ") or contact["number"]
            contact["mail"] = input("Enter new email:- ") or contact["mail"]
            contact["address"] = input("Enter new address:- ") or contact["address"]
            # Save updated data
            saveContact(data)
            print("Contact updated")
            return
    print("Contact not found!")

# Function to delete a contact
def deleteContact():
    dName=input("Enter name to delete:- ").lower()
    data=loadContact()
    # Filter out the contact to delete
    nContact=[c for c in data if c["name"].lower()!=dName]
    if len(nContact)==len(data):
        print("Contact not found")
    else:
        saveContact(nContact)
        print("Contact deleted")

# Export into CSV file
def exportToCSV():
    data=loadContact()
    if not data:
        print("No contact to export.")
        return
    # Create and write to CSV file
    with open (csvFile,"w", newline="") as csvfile:
        fieldNames=["name","number","mail","address"]
        writer=csv.DictWriter(csvfile, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Contacts exported to {csvFile}")

# Using while function for exiting Program
def main():
    while True:
        print("""
1. Add Content
2. View Content
3. Search Content
4. Edit Content
5. Delete Content
6. Export to CSV
7. exit\n""")
        try:
            choice = int(input("Enter your choice:- "))     #Input must be a number
        except ValueError:
            print("Please enter a valid number.")
            continue  
            
        # Match user choice with corresponding function
        match choice:
            case 1:
                conDetails()
            case 2:
                print("All Contents\n")
                view()
            case 3:
                searchContact()
            case 4:
                editContact()
            case 5:
                deleteContact()
            case 6:
                exportToCSV()
            case 7:
                print("Exiting contact book...")
                break
            case _:
                print("Invalid input")

# Run the program
main()
