from email_validator import validate_email, EmailNotValidError
import phonenumbers, re, datetime

class PersonData:
    
    def __init__(self, name, address, dob, phone_number, email):
        self.name = name
        self.address = address
        self.dob = dob
        self.phone_number = phone_number
        self.email = email

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_dob(self):
        return self.dob

    def set_dob(self, dob):
        self.dob = dob

    def get_phone_number(self):
        return self.phone_number

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def __str__(self):
        return f"Summary for {self.name}:\nAddress: {self.address}\nDate of Birth: {self.dob}\nPhone Number: {self.phone_number}\nEmail: {self.email}\n"

# noinspection SpellCheckingInspection
def validate_name(check_name):
    name_pattern = r'^([A-Za-zÄÖÜäöüß]+(-[A-Za-zÄÖÜäöüß]+)?)\s+([A-Za-zÄÖÜäöüß]+(-[A-Za-zÄÖÜäöüß]+)?)$'
    if re.match(name_pattern, check_name, re.UNICODE):
        return capitalize_name(check_name)
    else:
        return False

def capitalize_name(name):
    def capitalize_hyphen(part):
        return '-'.join(word.capitalize() for word in part.split('-'))
    return ' '.join(capitalize_hyphen(part) for part in name.split())


# noinspection SpellCheckingInspection
def validate_address(check_address):
    address_pattern = r'^([A-Za-zäöüÄÖÜß\s-]+)\s+(\d+)(?:\s((?:Apt|Apartment|Top|Unit|Flat|/)\.?\s*\d+))?\s+(\d{4})\s+([A-Za-zäöüÄÖÜß\s.-]+)$'
    if re.match(address_pattern, check_address, re.UNICODE):
        return True
    else:
        return False

def validate_dob(dob):
    dob_pattern = r'^(0?[1-9]|[12][0-9]|3[01])\.(0?[1-9]|1[0-2])\.(19[2-9][0-9]|20[0-1][0-9]|202[0-4])$'
    dob = re.sub(r'[-/,_]', ".", dob)
    if re.match(dob_pattern, dob):
        try:
            day, month, year = map(int, dob.split('.'))
            return datetime.datetime(year, month, day)
        except ValueError:
            return False
    return False

def validate_phone_numbers(check_number):
    try:
        check_number = phonenumbers.parse(check_number)
        return phonenumbers.is_valid_number(check_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

def validate_email_address(email_address):
    try:
        email_address = validate_email(email_address).normalized
        return True, email_address
    except EmailNotValidError as e:
        print(f"Invalid email address: {str(e)}. Please try again.")
        return False

def input_cleaning(u_input):
    u_input = u_input.strip()
    u_input = re.sub(r'\s+', ' ', u_input)

    if re.search(r'\d+[\s./-]+\d+[\s./-]+\d+', u_input):
        u_input = re.sub(r'\s', '', u_input)
    return u_input

def show_info(dictionary, key_name):
    if key_name not in dictionary:
        return f"No entry found for {key_name}"

    dict_values = dictionary[key_name]
    result = [f" {key_name};",
              f"Address: {dict_values.get_address()}",
              f"Date of Birth: {dict_values.get_dob()}",
              f"Phone Number: {dict_values.get_phone_number()}",
              f"Email Address: {dict_values.get_email()}"]
    return '\n'.join(result)+'\n'
def edit_values():
    return

def change_values(objt):
    while True:
        number = input(
            "Please make a selection from to change from the following:\n1: Name\n2: Address\n3: Date of Birth\n4: Telephone Number\n5: Email Address\n6: Exit\nEnter your selection: ")
        if number == "1":
            name = capitalize_name(input_cleaning(input("Please enter a new name: ")))
            if validate_name(name):
                objt.set_name(name)
                print(f"New name is {name}.\n")
                continue
            else:
                print("Invalid name, please try again.")
        elif number == "2":
            address = input_cleaning(input("Please enter a new address: "))
            if validate_address(address):
                objt.set_address(address)
                print(f"New address is {address}.\n")
                continue
            else:
                print("Invalid address, please try again.")
        elif number == "3":
            dob = input_cleaning(input("Please enter a new date of birth: "))
            if validate_dob(dob):
                objt.set_dob(dob)
                print(f"New date of birth is {dob}.\n")
                continue
            else:
                print("Invalid date of birth, please try again.")
        elif number == "4":
            phone_number = input_cleaning(input("Please enter a new phone number including the area code: "))
            if validate_phone_numbers(phone_number):
                objt.set_phone_number(phone_number)
                print(f"New phone number is {phone_number}.\n")
                continue
            else:
                print("Invalid phone number, please try again.")
        elif number == "5":
            email = input_cleaning(input("Please enter a new address: "))
            if validate_email_address(email):
                objt.set_email(email)
                print(f"New email address is {email}.\n")
                continue
            else:
                print("Invalid address, please try again.")
        elif number == "6":
            return "6"

def confirm_info(input_object):
    while True:
        print(input_object)
        print("Press 1 to confirm and add to records.\nPress 2 to redo the entry.\nPress 3 to cancel and exit.\n ")
        confirm = input("Please enter your choice: ")
        if confirm == "1":
            return "add"
        elif confirm == "2":
            return "redo"
        elif confirm == "3":
            return "exit"
        else:
            print("Invalid choice. Please try again.")

'''
change values - done
filter - goes along with displaying filtered list, needs to be able to filter by type of thing, ie address or dob I believe. 
option to display full or filtered list - can display one full person, need to add functionality to display all data, and data filtered by name/address etc
'''
# noinspection SpellCheckingInspection
def main():
    questions = [
        "your first and last name: ",
        "your street and street number, followed by your postcode and city. e.g. Musterstraße 14 0123 Musterstadt: ",
        "your date of birth in the DD.MM.YYYY format: ",
        "your telephone number including the country code e.g. +43660123456: ",
        "your email address: "
    ]
    people_data = {}
    name, address, dob, phone_number, email = "","","","",""
    while True:
        print("Please enter one of the following:\nEnter \"1\" to input new information\nEnter \"2\" to view stored data\nEnter \"3\", to end.")
        user_input = input("Enter your choice: ").strip()

        if user_input == "3":
            break

        elif user_input == "2":
            if len(people_data) > 0:
                user_input = capitalize_name(input("Please enter a full name to see the relevant information: "))
                if user_input.strip() in people_data:
                    print(f"Information for {show_info(people_data, user_input.strip())}")
                    sel = input("Enter \"E\" to edit this information, or any key to continue back to the main menu: \n")
                    if sel.casefold() == "e":
                        old_name = person.get_name()
                        change_values(people_data[user_input])
                        if person.get_name() != old_name:
                            del people_data[old_name]
                            people_data[person.get_name()] = person
                    continue
                else:
                    print(f"{user_input} not in database.")
                    continue
            else:
                print(f"Database is empty, add information before querying")
            continue


        elif user_input == "1":
            for item in questions:
                while True:
                    user_input = input_cleaning(input(f"Please enter {item}"))
                    if user_input == "3":
                        break

                    if "name" in item:
                        corrected_name = validate_name(user_input)
                        if corrected_name:
                            if corrected_name in people_data:
                                print("This name already exists in the records. Please try again with a different name.")
                            else:
                                name = corrected_name
                                print(f"Valid name: {name}")
                                break
                        else:
                            print("Invalid name format. Please try again.")

                    elif "street" in item:
                        if validate_address(user_input):
                                address = user_input
                                print(f"Valid address: {address}")
                                break
                        else:
                            print("Invalid address format. Please try again")

                    elif "date of birth" in item:
                        if validate_dob(user_input):
                                dob = user_input
                                print(f"Valid dob: {dob}")
                                break
                        else:
                            print("Invalid date of birth. Please try again.")

                    elif "telephone" in item:
                        if validate_phone_numbers(user_input):
                            phone_number = user_input
                            print(f"Valid Phone Number: {phone_number}")
                            break
                        else:
                            print(f"Invalid phone number format. Please try again.")

                    elif "email" in item:
                        user_input = user_input.replace(' ', '')
                        if validate_email_address(user_input):
                                email = user_input
                                print(f"Valid Email: {email}\n")
                                break

                if user_input.strip() == "3":
                    break

            if user_input.strip() == "3":
                break
        else:
            print("Invalid input, please try again.\n")
            continue

        person=PersonData(name,address,dob,phone_number,email)
        while True:
            result = confirm_info(person)
            if result == "add":
                people_data[person.get_name()] = person
                print("Information entry complete.")
                break
            elif result == "redo":
                change_values(person)
                if change_values(person) == "6":
                    print("Information entry was not completed. Exiting.")
                    break
            elif result == "exit":
                print("Information entry not completed. Exiting.")
                break
            else:
                print("Invalid input, please try again.")

if __name__ == "__main__":
    main()