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

def display():
    """
    Chains the function from read file to display the contents of the file 

    args: None

    output: 
        Output of medicine information in a tabular format
    """
    display_content = read_file(path)

    print(f"{"S.N.":<10}|{"Meidicine Name":30}|{"Brand Name":<20}|{"Quantity (Tablets)":<20}|{"Rate (Tablet)":<20}|{"Rate(Strip)":<20}|{"Tablet Per Strip":<20}")
    print("-"*140)
    for key, values in display_content.items():
        print(f"{key:<10}|{values[0]:<30}|{values[1]:<20}|{values[2]:<20}|{values[3]:<20}|{values[4]:<20}|{values[5]:<20}")
        print("-"*130)
    


display()


        

