import os
import random 
from UtilityFunctions import calc_invoice

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
    except Exception as e:
        print(e)
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


def generate_invoice(med_info, date_of_transaction, path):
    raw_data = read_file(path)
    total_cost = calc_invoice(med_info, raw_data)
    output_path = os.path.abspath("invoice.txt")
    try:
        f = open(output_path, "a+")
    except Exception as e:
        print(e)
        return

    f.write("="*60 + "\n")
    f.write(f"Bill Number: {random.randint(100000, 9999999)}\n")
    f.write(f"Med Store Pvt Ltd — Invoice\n")
    f.write(f"Date: {date_of_transaction}\n")
    f.write("="*60 + "\n")

    for item in med_info:  
        c_name    = item[0]
        med_name  = item[2]
        med_brand = item[3]
        unit_type = "Tablet(s)" if item[4] == "t" else "Strip(s)"
        quantity  = item[5]

        f.write(f"  Customer : {c_name}\n")
        f.write(f"  Medicine : {med_name} ({med_brand})\n")
        f.write(f"  Quantity : {quantity} {unit_type}\n")
        f.write("-"*60 + "\n")

    f.write(f"TOTAL: Rs. {total_cost:.2f}\n")
    f.write("="*60 + "\n\n")

    print(f"Invoice created at {output_path}")
    f.close()
