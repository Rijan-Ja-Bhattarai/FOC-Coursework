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
        if id < 0 or id > len(raw_data.keys()):
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
            - discount is a float discount value (5% if eligible) or None if not applicable.
    """
    discount = None

    if quantity < 1:
        print("Invalid Quantity")
        
    elif quantity == 1:
        print("Buy 1 more strip for 5% discount :D")
        response = ""
        opt = ["y", "n", "yes", "no"]


        # Ask the user to buy 1 more to boost sales by providing discount
        while response not in opt:
            try:
                response = input("Do you wish to buy 1 more strip (y/n): ").lower()
                response = response[0]
                try:
                    if int(response) > 2:
                        print("Invalid input")
                    elif int(response) != 0:
                        response = opt[1]
                        quantity *= tablet_per_strip
                        break
                    else:
                        response = opt[0]
                        quantity += 1
                        quantity *= tablet_per_strip
                        discount = 0.05
                        break
                except ValueError:
                    continue
            except KeyboardInterrupt:
                print("Input interrupted by user")
    else:
        quantity *= tablet_per_strip

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

    
    BANNER = """                                                                                                                                                                    
                                                               dddddddd                                                                                               
MMMMMMMM               MMMMMMMM                                d::::::d   SSSSSSSSSSSSSSS      tttt                                                                   
M:::::::M             M:::::::M                                d::::::d SS:::::::::::::::S  ttt:::t                                                                   
M::::::::M           M::::::::M                                d::::::dS:::::SSSSSS::::::S  t:::::t                                                                   
M:::::::::M         M:::::::::M                                d:::::d S:::::S     SSSSSSS  t:::::t                                                                   
M::::::::::M       M::::::::::M    eeeeeeeeeeee        ddddddddd:::::d S:::::S        ttttttt:::::ttttttt       ooooooooooo   rrrrr   rrrrrrrrr       eeeeeeeeeeee    
M:::::::::::M     M:::::::::::M  ee::::::::::::ee    dd::::::::::::::d S:::::S        t:::::::::::::::::t     oo:::::::::::oo r::::rrr:::::::::r    ee::::::::::::ee  
M:::::::M::::M   M::::M:::::::M e::::::eeeee:::::ee d::::::::::::::::d  S::::SSSS     t:::::::::::::::::t    o:::::::::::::::or:::::::::::::::::r  e::::::eeeee:::::ee
M::::::M M::::M M::::M M::::::Me::::::e     e:::::ed:::::::ddddd:::::d   SS::::::SSSSStttttt:::::::tttttt    o:::::ooooo:::::orr::::::rrrrr::::::re::::::e     e:::::e
M::::::M  M::::M::::M  M::::::Me:::::::eeeee::::::ed::::::d    d:::::d     SSS::::::::SS    t:::::t          o::::o     o::::o r:::::r     r:::::re:::::::eeeee::::::e
M::::::M   M:::::::M   M::::::Me:::::::::::::::::e d:::::d     d:::::d        SSSSSS::::S   t:::::t          o::::o     o::::o r:::::r     rrrrrrre:::::::::::::::::e 
M::::::M    M:::::M    M::::::Me::::::eeeeeeeeeee  d:::::d     d:::::d             S:::::S  t:::::t          o::::o     o::::o r:::::r            e::::::eeeeeeeeeee  
M::::::M     MMMMM     M::::::Me:::::::e           d:::::d     d:::::d             S:::::S  t:::::t    tttttto::::o     o::::o r:::::r            e:::::::e           
M::::::M               M::::::Me::::::::e          d::::::ddddd::::::ddSSSSSSS     S:::::S  t::::::tttt:::::to:::::ooooo:::::o r:::::r            e::::::::e          
M::::::M               M::::::M e::::::::eeeeeeee   d:::::::::::::::::dS::::::SSSSSS:::::S  tt::::::::::::::to:::::::::::::::o r:::::r             e::::::::eeeeeeee  
M::::::M               M::::::M  ee:::::::::::::e    d:::::::::ddd::::dS:::::::::::::::SS     tt:::::::::::tt oo:::::::::::oo  r:::::r              ee:::::::::::::e  
MMMMMMMM               MMMMMMMM    eeeeeeeeeeeeee     ddddddddd   ddddd SSSSSSSSSSSSSSS         ttttttttttt     ooooooooooo    rrrrrrr                eeeeeeeeeeeeee                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
"""
    ART = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⠛⠛⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠋⠉⠀⠀⠉⠙⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣶⣶⠀⠀⣶⣶⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⠛⠃⠈⠻⠿⣶⣶⠿⠟⠁⠘⠛⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣀⣀⣀⣀⠀⣿⣀⣋⣸⣷⣆⣀⣀⣰⣾⣇⣙⣀⣿⠀⣀⣀⣀⣀⡀⠀⠀
⠀⠀⢸⡏⢉⠉⣿⠀⣿⠉⡉⢹⣿⡏⢉⡉⢹⣿⡏⢉⠉⣿⠀⣿⠉⡉⢹⡇⠀⠀
⠀⠀⢸⡇⣿⠀⣿⠀⣿⠀⣿⢸⣿⡇⢸⡇⢸⣿⡇⣿⠀⣿⠀⣿⠀⣿⢸⡇⠀⠀
⠀⠀⢸⣇⣈⣀⣿⠀⣿⣀⣁⣸⣿⣇⣈⣁⣸⣿⣇⣈⣀⣿⠀⣿⣀⣁⣸⡇⠀⠀
⠀⠀⢸⡏⣩⠉⣿⠀⣿⠉⣍⢹⣿⡏⢩⡍⢹⣿⡏⣩⠉⣿⠀⣿⠉⣍⢹⡇⠀⠀
⠀⠀⢸⡇⣿⠀⣿⠀⣿⠀⣿⢸⣿⡇⢸⡇⢸⣿⡇⣿⠀⣿⠀⣿⠀⣿⢸⡇⠀⠀
⠀⠀⢸⣧⣤⣤⣿⠀⣿⣤⣤⣼⣿⣧⣤⣤⣼⣿⣧⣤⣤⣿⠀⣿⣤⣤⣼⡇⠀⠀
⠀⠀⢸⡇⢤⠀⣿⠀⣿⠀⡤⢸⡇⢠⣤⣤⡄⢸⡇⢤⠀⣿⠀⣿⠀⡤⢸⡇⠀⠀
⠀⠀⢸⣷⣶⣶⣿⠀⣿⣶⣶⣾⡇⢸⣿⣿⡇⢸⣷⣶⣶⣿⠀⣿⣶⣶⣾⡇⠀⠀
⠀⠀⠈⠉⠉⠉⠉⠀⠉⠉⠉⠉⠁⠈⠉⠉⠁⠈⠉⠉⠉⠉⠀⠉⠉⠉⠉⠁⠀⠀
""".splitlines()

    MENU = [
    "\t   Med Store Pvt Ltd",
    "=" * 30,
    "",
    "  [ 1 ]  Sell Medicines",
    "  [ 2 ]  Restock Medicines",
    "  [ 3 ]  Exit",
    "",
    "=" * 30]

    # Print the banner
    print(BANNER)
    # Center the menu vertically against the art
    height = max(len(ART), len(MENU))
    art_lines = center_lines(ART, height)
    menu_lines = center_lines(MENU, height)

    art_width = max(len(line) for line in ART)

    for a, m in zip(art_lines, menu_lines):
        print(f"  {a:<{art_width}}    {m}")

    valid_options = ["1", "2", "3"]
    choice = ""
    while choice not in valid_options:
        try:
            choice = input("Select an option (1/2/3): ").strip()
        except KeyboardInterrupt:
            print("Input interrupted by user")
        except Exception:
            print("An exception occurred")
        if choice not in valid_options:
            print("  Invalid option, please enter 1, 2, or 3")
    return choice

def center_lines(lines, height):
    """Return a list of length 'height' with 'lines' vertically centered."""
    top = (height - len(lines)) // 2
    bottom = height - len(lines) - top
    return [""] * top + lines + [""] * bottom


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