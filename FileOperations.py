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


def generate_restock_invoice(med_info, date_of_transaction, path):
    """
    Generates a VAT invoice for a restock transaction.
    A single invoice is produced per transaction, even if multiple medicines are restocked.
    The inventory file is also updated to reflect the new stock levels.
 
    Args:
        med_info:             List of restock entries, each containing supplier and medicine details.
        date_of_transaction:  Datetime of the transaction from the datetime library.
        path:                 Path to the original inventory file, used to read current rates.
    Output:
        Appends a formatted VAT invoice to restock_invoice.txt and updates medicine_info.txt.
    """
    raw_data = read_file(path)
    total_cost = calc_invoice(med_info, raw_data)
    output_path = "restock_invoice.txt"
 
    try:
        f = open(output_path, "a+")
    except Exception as e:
        print(e)
        return
 
    # Invoice header — supplier name taken from the first entry as it is shared across the transaction
    supplier_name = med_info[0][0]
    f.write("=" * 70 + "\n")
    f.write(f"Med Store Pvt Ltd — VAT Invoice / Restock Receipt\n")
    f.write(f"Bill Number : {random.randint(100000, 9999999)}\n")
    f.write(f"Date        : {date_of_transaction}\n")
    f.write(f"Supplier    : {supplier_name}\n")
    f.write("=" * 70 + "\n")
 
    # Column headers for itemized medicine list
    f.write(f"  {'Medicine':<25}{'Brand':<20}{'Quantity':<18}{'Rate':>8}{'Amount':>12}\n")
    f.write("-" * 70 + "\n")
 
    for item in med_info:
        med_name = item[2]
        med_brand = item[3]
        unit_type = item[4]
        quantity = item[5]
        medication = raw_data.get(item[1])
 
        # Resolve rate and display label based on unit type
        if unit_type == "s":
            rate = medication[4]
            unit_label = f"{quantity} Strip(s)"
        else:
            rate = medication[3]
            unit_label = f"{quantity} Tablet(s)"
 
        amount = quantity * rate
 
        f.write(f"{med_name:<25}{med_brand:<20}{unit_label:<18}Rs.{rate:>6.2f}  Rs.{amount:>8.2f}\n")
 
    f.write("-" * 70 + "\n")
    f.write(f"{'TOTAL RESTOCKED VALUE':>58}  Rs.{total_cost:>8.2f}\n")
    f.write("=" * 70 + "\n\n")
    f.close()
 
    # Update the inventory file to reflect restocked quantities
    update_inventory(raw_data, path)
    print(f"Restock invoice created at {output_path}")
 
 
def generate_invoice(med_info, date_of_transaction, path):
    """
    Function to create invoice when the user is selling medicines.
 
    Args:
        med_info:             List of medicine information that is used for data.
        date_of_transaction:  Time of transaction used from datetime library.
        path:                 Original data file path.
    Output:
        Appends a formatted invoice to invoice.txt.
    """
    raw_data = read_file(path)
    total_cost = calc_invoice(med_info, raw_data)
    output_path = "invoice.txt"
 
    try:
        f = open(output_path, "a+")
    except Exception as e:
        print(e)
        return
 
    f.write("=" * 60 + "\n")
    f.write(f"Bill Number: {random.randint(100000, 9999999)}\n")
    f.write(f"Med Store Pvt Ltd — Invoice\n")
    f.write(f"Date: {date_of_transaction}\n")
    f.write("=" * 60 + "\n")
 
    for item in med_info:
        c_name    = item[0]
        med_name  = item[2]
        med_brand = item[3]
        unit_type = "Tablet(s)" if item[4] == "t" else "Strip(s)"
        quantity  = item[5]
 
        f.write(f"  Customer : {c_name}\n")
        f.write(f"  Medicine : {med_name} ({med_brand})\n")
        f.write(f"  Quantity : {quantity} {unit_type}\n")
        f.write("-" * 60 + "\n")
 
    f.write(f"TOTAL: Rs. {total_cost:.2f}\n")
    f.write("=" * 60 + "\n\n")
    print(f"Invoice created at {output_path}")
    f.close()



def update_inventory(raw_data, path):
    """
    Writes the current state of raw_data back to the inventory file,
    persisting any stock changes (additions from restock or deductions from sales).
 
    Args:
        raw_data: The in-memory dictionary of medicine records to be saved.
        path:     Path to the original inventory file to overwrite.
    Output:
        Overwrites medicine_info.txt with updated stock quantities.
 
    Note:
        This function assumes each record in the file is stored as a
        comma-separated line in the format:
            id,medicine_name,brand_name,quantity,tablet_rate,strip_rate,tablets_per_strip
        Adjust the write format below if your file uses a different structure.
    """
    try:
        f = open(path, "w")
    except Exception as e:
        print(e)
        return
 
    for key, values in raw_data.items():
        # Reconstruct each line to match the original file format
        line = f"{key},{values[0]},{values[1]},{values[2]},{values[3]},{values[4]},{values[5]}\n"
        f.write(line)
 
    f.close()
 
