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

    def set_name(self, name, people_data):
        try:
            if capitalize_name(name) in people_data:
                raise ValueError("This name already exists in the records. Please try again.")
            if not validate_name(name):
                raise ValueError("Invalid name format. Please try again.")
            self.name = capitalize_name(name)
            return True
        except ValueError as e:
            print(f"Error setting name: {e}")
            return False

    def get_address(self):
        return self.address

    def set_address(self, address):
        try:
            if not validate_address(address):
                raise ValueError("Invalid address format. Please try again")
            self.address = address
            return True
        except ValueError as e:
            print(f"Error setting address: {e}")
            return False

    def get_dob(self):
        return self.dob

    def set_dob(self, dob):
        try:
            validated_dob = validate_dob(dob)
            self.dob = validated_dob
            return True
        except ValueError as e:
            print(f"Error setting date of birth: {e}")
            return False

    def get_phone_number(self):
        return self.phone_number

    def set_phone_number(self, phone_number):
        try:
            if not validate_phone_numbers(phone_number):
                raise ValueError("Invalid phone number. Please try again.")
            self.phone_number = phone_number
            return True
        except ValueError as e:
            print(f"Error setting phone number: {e}")
            return False

    def get_email(self):
        return self.email

    def set_email(self, email):
        try:
            valid, result = validate_email_address(email)
            if not valid:
                raise ValueError(result)
            self.email = email
            return True
        except ValueError as e:
            print(f"Error setting email: {e}")
            return False

    def __str__(self):
        return f"Summary for {self.name}:\nAddress: {self.address}\nDate of Birth: {self.dob}\nPhone Number: {self.phone_number}\nEmail: {self.email}\n"

# noinspection SpellCheckingInspection
def validate_name(check_name):
    name_pattern = r'^([A-Za-zÄÖÜäöüß]+(-[A-Za-zÄÖÜäöüß]+)?)\s+([A-Za-zÄÖÜäöüß]+(-[A-Za-zÄÖÜäöüß]+)?)$'
    if re.match(name_pattern, check_name, re.UNICODE):
        return True
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
            validated_dob = datetime.datetime(year, month, day)
            return validated_dob.strftime("%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date (e.g., 30th of February). Please try again.")
    raise ValueError("Date format is incorrect. Please try again")

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
        return False, str(e)

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

def change_values(objt, people_data):
    while True:
        number = input(
            "Please make a selection from to change from the following:\n1: Name\n2: Address\n3: Date of Birth\n4: Telephone Number\n5: Email Address\n6: Exit\nEnter your selection: ")
        if number == "6":
            return "6"

        elif number == "1":
            name = input_cleaning(input("Please enter a new name: "))
            if objt.set_name(name, people_data):
                print(f"New name is {objt.get_name()}.\n")
                continue
            else:
                print("Name change failed. Please try again.")

        elif number == "2":
            address = input_cleaning(input("Please enter a new address: "))
            if objt.set_address(address):
                print(f"New address is {objt.get_address()}.\n")
                continue
            else:
                print("Address change failed. Please try again.")

        elif number == "3":
            dob = input_cleaning(input("Please enter a new date of birth: "))
            if objt.set_dob(dob):
                print(f"New date of birth is {objt.get_dob()}.\n")
                continue
            else:
                print("D.O.B change failed. Please try again.")

        elif number == "4":
            phone_number = input_cleaning(input("Please enter a new phone number including the area code: "))
            if objt.set_phone_number(phone_number):
                print(f"New phone number is {objt.get_phone_number()}.\n")
                continue
            else:
                print("Phone number change failed. Please try again.")

        elif number == "5":
            email = input_cleaning(input("Please enter a new email address: "))
            if objt.set_email(email):
                print(f"New email address is {objt.get_email()}.\n")
                continue
        else:
            print("Email address change failed. Please try again.")

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

def filter_view(i, dictionary):
    if i == "1":
        print("Stored names:")
        print(*(item.get_name() for item in dictionary.values()))
    elif i == "2":
        print("Stored addresses:")
        print(*(item.get_address() for item in dictionary.values()))
    elif i == "3":
        print("Stored dates of birth:")
        print(*(item.get_dob() for item in dictionary.values()))
    elif i == "4":
        print("Stored phone numbers:")
        print(*(item.get_phone_number() for item in dictionary.values()))
    elif i == "5":
        print("Stored email addresses:")
        print(*(item.get_email() for item in dictionary.values()))
    else:
        print("Invalid input, please try again.")

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
    person = PersonData("", "", "", "", "")
    while True:
        print("Please enter one of the following:\nEnter \"1\" to input new information\nEnter \"2\" to view stored data\nEnter \"3\", to edit stored data\nEnter \"4\" to exit.")
        user_input = input("Enter your choice: ").strip()

        if user_input == "4":
            break

        elif user_input == "3":
            if len(people_data) > 0:
                while True:
                    user_input = capitalize_name(input("Please enter a full name to edit the relevant information or enter \"4\" to return to the main menu\nEnter your input now: "))
                    if user_input == "4":
                        break
                    elif user_input.strip() in people_data:
                        old_name = person.get_name()
                        change_values(people_data[user_input], people_data)
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

        elif user_input == "2":
            if len(people_data) > 0:
                while True:
                    user_input = input("Enter \"1\" to select a person to view.\nEnter \"2\" to view everyone based on a catagory.\nEnter \"3\" to view all data\nEnter \"4\"to quit\nEnter your input now: ")
                    if user_input == "4":
                        return
                    elif user_input == "3":
                        for items in people_data.values():
                            print(items)
                    elif user_input == "2":
                        while True:
                            user_input = input("Please choose a catagory to view from the following:\n1 for name.\n2 for address.\n3 for date of birth\n4 for phone number.\n5 for email address.\n6 to exit.\nEnter you input now: ")
                            if user_input == "6":
                                break
                            filter_view(user_input, people_data)

                    elif user_input == "1":
                        user_input = capitalize_name(input("Please enter a full name to see the relevant information: "))
                        if user_input.strip() in people_data:
                            print(f"Information for {show_info(people_data, user_input.strip())}")
                    else:
                        print("Invalid input, please try again.")
                    new_input = input("Enter \"1\" to view different data sets, or any key to continue back to the main menu: \n")
                    if new_input == "1":
                        continue
                    else:
                        break
            else:
                print(f"Database is empty, add information before querying")
            continue


        elif user_input == "1":
            for item in questions:
                while True:
                    user_input = input_cleaning(input(f"Please enter {item}"))
                    if user_input == "4":
                        break

                    if "name" in item:
                        if person.set_name(user_input, people_data):
                            print(f"Valid name: {person.get_name()}")
                            break

                    elif "street" in item:
                        if person.set_address(user_input):
                            print(f"Valid address: {person.get_address()}")
                            break

                    elif "date of birth" in item:
                        if person.set_dob(user_input):
                            print(f"Valid dob: {person.get_dob()}")
                            break

                    elif "telephone" in item:
                        if person.set_phone_number(user_input):
                            print(f"Valid Phone Number: {person.get_phone_number()}")
                            break

                    elif "email" in item:
                        user_input = user_input.replace(' ', '')
                        if person.set_email(user_input):
                            print(f"Valid Email: {person.get_email()}\n")
                            break

                if user_input.strip() == "4":
                    break

            if user_input.strip() == "4":
                break
        else:
            print("Invalid input, please try again.\n")
            continue

        #person=PersonData(name,address,dob,phone_number,email)
        while True:
            result = confirm_info(person)
            if result == "add":
                people_data[person.get_name()] = person
                print("Information entry complete.")
                break
            elif result == "redo":
                change_values(person, people_data)
                if change_values(person, people_data) == "6":
                    print("Information entry was not completed. Exiting.")
                    break
            elif result == "exit":
                print("Information entry not completed. Exiting.")
                break
            else:
                print("Invalid input, please try again.")

if __name__ == "__main__":
    main()