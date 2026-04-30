from datetime import datetime as dt
from UtilityFunctions import is_empty
import math

path = "medicine_info.txt"

def read_file(path):
    """
    Reads a given file and returns the contents of the file in a dictionary format 

    args: 
        path : a string which contains the file path of the file which is to be read
    
    returns:
        med_info : a dictionary with indexes such as 1, 2, 3 as keys and medicine information as values in a list
                example: 1 : [name, brand_name, quantity, rate per strip, rate per tablet, number of tablet per strip]
    """
    try:
        f = open(path, "r")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return {}
    lines = f.readlines()
    f.close()
    med_info = {} # Stores the med information in the format 1 : [med information]
    idx = 0 # Stores the index for medicine information 
    for line in lines:
        idx += 1
        line = line.replace("\n", " ") # Replace new line character and store it in line for parsing later on
        content = line.split(",")
        med_name = content[0]
        brand_name = content[1]
        med_quantity_tablets = int(content[2])
        rate_tablet = float(content[3])
        rate_strip = float(content[4])
        num_tablet_per_strip = int(content[5])
        med_info[idx] = [med_name, brand_name, med_quantity_tablets, rate_tablet, rate_strip, num_tablet_per_strip]
    return med_info

raw_data = read_file(path)

def display(display_content):
    """
    Takes raw data as input from medicine_info.txt and displays the data in a tabular format 

    args: 
    display_content: A dictionary that contains raw medicine information in the format 1 : [
    med information] which is returned by the read_file function. This is passed as an argument to the display function to display 
    the contents of the file in a tabular format. This is done to keep the code modular and to allow for better readability and 
    maintainability of the code by keeping the logic of reading the file and displaying the contents
    inside another independent function 

    output: 
        Output of medicine information in a tabular format
    """

    if display_content is None:
        print("No Data To Display")
        return

    print("-"*146)
    print(f"{"S.N.":<10}|{"Meidicine Name":30}|{"Brand Name":<20}|{"Quantity (Tablets)":<20}|{"Rate (Tablet)":<20}|{"Rate(Strip)":<20}|{"Tablet Per Strip":<20}|")
    print("-"*10 + "|" + "-" *30 + "|" + "-" *20 + "|" + "-" *20 + "|" + "-" *20 + "|" + "-" *20 + "|" + "-" * 20 + "|")
    for key, values in display_content.items():
        print(f"{key:<10}|{values[0]:<30}|{values[1]:<20}|{values[2]:<20}|{values[3]:<20}|{values[4]:<20}|{values[5]:<20}|")
        print("-"*10 + "|" + "-" *30 + "|" + "-" *20 + "|" + "-" *20 + "|" + "-" *20 + "|" + "-" *20 + "|" + "-" * 20 + "|")
    


display(raw_data)

# Main 
med_unit_type = ["t", "s"]
customer_name = ""
while is_empty(customer_name):
    customer_name = input("Customer Name: ").strip()

    if is_empty(customer_name):
        print("Name can't be empty")

def main():
    """Function that contains the main module of the function"""
    id = -1
    unit_type = ""
    quantity = -1

    # Validate id
    while id > len(raw_data) or id < 0 or type(id) == str:
        try:
            id = int(input("Medicine ID: "))
        except ValueError:
            print("ID Must be an integer") 
            continue 
        if id < 0:
            print("Invalid index")     

    # Validate Unit Type
    while unit_type not in med_unit_type:
        unit_type = input("Unit Type (Strip/Tablet): ").lower()
        unit_type = unit_type[0]
        if unit_type[0] not in med_unit_type:
            print("Invalid Med Unit")
    
    t = raw_data.get(id)
    tablet_quantity = t[2]
    tablet_per_strip = t[5]
    
    while quantity < 0 or quantity > tablet_quantity or type(quantity) == str:
        try:
            quantity = int(input("Quantity: "))
        except ValueError:
            print("Quantity must be an integer value")
        if quantity < 0 or quantity > tablet_quantity:
            print("Quantity not available")
        if unit_type == "s":
            if quantity / tablet_per_strip < 0:
                print("Insufficient number of tablets per strip, buy more tablets to make the purhcase or buy in tablets")
                opt = input("Do you wish to buy in tablets? (y/n)").lower()
                opt = opt[0]
                while opt not in ["y", "n"]:
                    print("Invalid input")
                    opt = input("Do you wish to buy in tablets? (y/n)").lower()
                if opt == "y":
                    pass


main()
    
        


        
    
    


        

