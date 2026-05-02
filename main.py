import os
from datetime import datetime as dt
from FileOperations import read_file, generate_invoice
from InputFields import get_customer_name, get_medicine_id, get_unit_type, get_quantity, handle_strip_purchase, add_to_cart
from UtilityFunctions import display


path = os.path.abspath("medicine_info.txt")
raw_data = read_file(path)

# Main 
def main():
    """Main Function"""

    display(raw_data)

    customer_name = get_customer_name()
    id = get_medicine_id(raw_data)
    unit_type, med_unit_type = get_unit_type()

    t = raw_data.get(id)
    tablet_quantity = t[2]
    tablet_per_strip = t[5]
    med_brand = t[1]
    med_name = t[0]

    quantity = get_quantity(tablet_quantity)

    discount = None
    if unit_type in [med_unit_type[1], "strip", "strips"]:
        unit_type, discount = handle_strip_purchase(quantity, tablet_per_strip, unit_type)

    # Deduct purchased quantity from stock regardless of unit type
    raw_data[id][2] -= quantity

    # Only append discount to the result if one was applied
    result = [customer_name, id, med_name, med_brand, unit_type, quantity]
    if discount is not None:
        result.append(discount)
    return result


med_info = []
opt = ["y", "n", "yes", "no"]
while True:
    med_info.append(main()) # Store the contents from main to med_info to be used in other functions
    print(f"Items in cart \n{med_info}")

    cont = add_to_cart(opt)
    if cont != opt[0]:
        print("Thank you for choosing Med Store Pvt Ltd. We hope to see you again :D")
        dot = dt.now()
        generate_invoice(med_info, dot)
        break