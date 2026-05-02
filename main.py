import os
from datetime import datetime as dt
from UtilityFunctions import is_empty, display
from FileOperations import read_file, generate_invoice, generate_restock_invoice, update_inventory
from InputFields import get_customer_name, get_medicine_id, get_unit_type, get_quantity, handle_strip_purchase, add_to_cart, get_supplier_name, get_restock_quantity, select_domain

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


def restock():
    """Handles the restocking flow for a single medicine entry."""

    display(raw_data)

    supplier_name = get_supplier_name()
    id = get_medicine_id(raw_data)
    unit_type, _ = get_unit_type()

    t = raw_data.get(id)
    med_brand = t[1]
    med_name = t[0]

    quantity = get_restock_quantity()

    # Add restocked quantity back into stock
    raw_data[id][2] += quantity

    return [supplier_name, id, med_name, med_brand, unit_type, quantity]


opt = ["y", "n", "yes", "no"]
while True:
    domain = select_domain()

    if domain == "3":
        print("Thank you for using Med Store Pvt Ltd. Goodbye!")
        break

    med_info = []
    transaction_type = "sale" if domain == "1" else "restock"

    while True:
        if transaction_type == "sale":
            med_info.append(main()) # Store the contents from main to med_info to be used in other functions
        else:
            med_info.append(restock()) # Store restock entries to be passed to generate_invoice

        print(f"Items in cart \n{med_info}")

        cont = add_to_cart(opt)
        if cont != opt[0]:
            dot = dt.now()
            if transaction_type == "sale":
                print("Thank you for choosing Med Store Pvt Ltd. We hope to see you again :D")
                generate_invoice(med_info, dot, path)
            else:
                print("Restock complete. Inventory has been updated.")
                generate_restock_invoice(med_info, dot, path)
            break