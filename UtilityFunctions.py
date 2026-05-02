def is_empty(input_field):
    """
    Checks the length of input field 

    args:
        input field : Takes the argument of an input field 
    
    Output: 
        Either true or false depending on length is equal to 0 or not
    """

    if (len(input_field) == 0):
        return True
    else:
        return False
    


def calc_invoice(med_info, raw_data):
    """
    Function to calculate total cost of purchased or restocked drugs.

    Args:
        med_info:  List of medicine information for data retrieval.
        raw_data:  Data from original medicine information file.
    Returns:
        Total cost of the transaction as a float.
    """
    total_cost = 0
    for item in med_info:
        medication = raw_data.get(item[1])
        unit_type = item[4]
        quantity = item[5]

        # Use strip rate for strip purchases, tablet rate otherwise
        if unit_type == "s":
            cost = quantity * medication[4]
        else:
            cost = quantity * medication[3]

        # Discount is only present on sale entries
        if len(item) > 6:
            cost *= 1 - item[6]

        total_cost += cost
    return total_cost
    

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
 
