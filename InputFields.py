from UtilityFunctions import is_empty


def get_customer_name():
    """
    Prompts and validates the customer name input.

    output:
        A non-empty stripped string representing the customer's name.
    """
    customer_name = ""

    while is_empty(customer_name):
        try:
            customer_name = input("Customer Name: ").strip()
        except KeyboardInterrupt:
            print("Input interrupted by user")
        except Exception:
            print("An exception occured")

        if is_empty(customer_name):
            print("Name can't be empty")

    return customer_name


def get_medicine_id(raw_data):
    """
    Prompts and validates the medicine ID against available entries in raw_data.

    args:
        raw_data: A dictionary of medicine records returned by read_file.

    output:
        A valid integer ID that exists within the bounds of raw_data.
    """
    id = -1

    # Validate id
    while id > len(raw_data) or id <= 0:
        try:
            id = int(input("Medicine ID: "))
        except ValueError:
            print("ID Must be an integer") 
            continue 
        except KeyboardInterrupt:
            print("Input cancelled by user")
        except Exception:
            print("An exception occured")
        if id < 0:
            print("Invalid index")

    return id


def get_unit_type():
    """
    Prompts and validates the unit type input (strip or tablet).

    output:
        A valid unit type string from the allowed med_unit_type list.
    """
    med_unit_type = ["t", "s", "strip", "tablet", "strips", "tablets"]
    unit_type = ""

    # Validate Unit Type
    while unit_type not in med_unit_type:
        unit_type = input("Unit Type (Strip/Tablet): ").lower()
        if unit_type not in med_unit_type:
            print("Invalid Med Unit")

    return unit_type, med_unit_type


def get_quantity(tablet_quantity):
    """
    Prompts and validates the quantity input against the available tablet stock.

    args:
        tablet_quantity: The total number of tablets currently in stock for the selected medicine.

    output:
        A valid integer quantity that is non-negative and does not exceed available stock.
    """
    quantity = -1

    # Validate sufficient amount of quantity w.r.t unit type
    while quantity < 0 or quantity > tablet_quantity:
        try:
            quantity = int(input("Quantity: "))
        except ValueError:
            print("Quantity must be an integer value")
            continue
        except KeyboardInterrupt:
            print("Input interrputed by user")
            continue
        if quantity < 0 or quantity > tablet_quantity:
            print("Quantity not available")

    return quantity


def handle_strip_purchase(quantity, tablet_per_strip, unit_type):
    """
    Handles the strip purchase logic, including discount calculation and fallback to tablet purchase.

    args:
        quantity:        The number of units the customer wants to purchase.
        tablet_per_strip: The number of tablets contained in one strip for the selected medicine.
        unit_type:       The current unit type selected by the customer ('s', 'strip', or 'strips').

    output:
        A tuple (unit_type, discount) where:
            - unit_type is the (possibly updated) purchase unit type.
            - discount is a float discount value (0.5 if eligible) or None if not applicable.
    """
    discount = None

    if quantity / tablet_per_strip < 1:
        print("Insufficient number of tablets per strip, buy more tablets to make the purhcase or buy in tablets")
        discount = None
        try:
            opt = input("Do you wish to buy in tablets? (y/n): ").lower()
            opt = opt[0]
            while opt not in ["y", "n"]:
                print("Invalid input")
                opt = input("Do you wish to buy in tablets? (y/n): ").lower()
            if opt == "y":
                unit_type = "t"
        except KeyboardInterrupt:
            print("Input interrupted by user")
        except Exception:
            print("An exception occured")
    elif quantity / tablet_per_strip >= 2:
        discount = 0.5

    return unit_type, discount


def get_supplier_name():
    """
    Prompts and validates the supplier name input during a restock transaction.

    output:
        A non-empty stripped string representing the supplier's name.
    """
    supplier_name = ""

    while is_empty(supplier_name):
        try:
            supplier_name = input("Supplier Name: ").strip()
        except KeyboardInterrupt:
            print("Input interrupted by user")
        except Exception:
            print("An exception occured")

        if is_empty(supplier_name):
            print("Name can't be empty")

    return supplier_name


def get_restock_quantity():
    """
    Prompts and validates the restock quantity input.
    Unlike purchasing, there is no upper stock limit when restocking.

    output:
        A valid positive integer representing the number of tablets to restock.
    """
    quantity = -1

    while quantity <= 0:
        try:
            quantity = int(input("Restock Quantity (tablets): "))
        except ValueError:
            print("Quantity must be an integer value")
            continue
        except KeyboardInterrupt:
            print("Input interrupted by user")
            continue
        if quantity <= 0:
            print("Quantity must be greater than zero")

    return quantity


def select_domain():
    """
    Displays the main domain menu and prompts the user to select an operation.

    output:
        A string representing the user's choice: '1' for sell, '2' for restock, '3' to exit.
    """
    valid_options = ["1", "2", "3"]
    choice = ""

    print("="*40)
    print("Med Store Pvt Ltd — Main Menu")
    print("="*40)
    print("1. Sell Medicines")
    print("2. Restock Medicines")
    print("3. Exit")
    print("="*40)

    # Validate domain selection
    while choice not in valid_options:
        try:
            choice = input("Select an option (1/2/3): ").strip()
        except KeyboardInterrupt:
            print("Input interrupted by user")
        except Exception:
            print("An exception occured")
        if choice not in valid_options:
            print("Invalid option, please enter 1, 2, or 3")

    return choice


def add_to_cart(cont_options):
    """
    Prompts the user to decide whether to continue adding medicines to the cart.

    args:
        cont_options: A list of valid input strings (e.g., ['y', 'n', 'yes', 'no']).

    output:
        The first character of the user's choice as a lowercase string ('y' or 'n').
    """
    cont = ""

    while cont not in cont_options or is_empty(cont):
        try:
            cont = input("Add more medicines to cart (y/n): ").lower()
        except KeyboardInterrupt:
            print("Input interrupted by user")
        except Exception:
            print("An error occured")
        if cont not in cont_options:
            print("Invalid input")
        if is_empty(cont):
            print("Operation can't be left empty")

    return cont[0]