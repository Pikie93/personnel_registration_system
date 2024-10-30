from email_validator import validate_email, EmailNotValidError
from datetime import datetime, date
import phonenumbers, re, calendar, json

class PersonData:
    def __init__(self, name, first_name, last_name, status, address, dob, phone_number, email):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.status = status
        self.address = address
        self.dob = dob
        self.phone_number = phone_number
        self.email = email

    def get_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_name(self, name, people_data):
        try:
            if capitalize_name(name) in people_data:
                return False, "This name already exists in the records. Please try again."
            if not validate_name(name):
                return False, "Invalid name format. Please try again."
            self.name = capitalize_name(name)
            names = name.split(" ")
            self.first_name = capitalize_name(names[0])
            self.last_name = capitalize_name(names[-1])
            return True, f"Name successfully updated to {self.get_name()}."
        except ValueError as e:
            return False, f"Error setting name: {str(e)}"

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_status(self):
        return self.status

    # noinspection SpellCheckingInspection
    def set_status(self, status):
        if status.lower() in ["employee", "visitor"]:
            self.status = status.capitalize()
            return True, ""
        else:
            return False, "Invalid input, please select either Employee or Visitor."

    def get_address(self):
        return self.address

    def set_address(self, address):
        if validate_address(address):
            self.address = address
            return True, ""
        else:
            return False, "Invalid address format. Please try again"

    def get_dob(self):
        return self.dob

    def set_dob(self, dob):
        try:
            validated_dob = validate_dob(dob)
            self.dob = validated_dob
            return True, ""
        except ValueError as e:
            return False, f"Error setting date of birth: {e}"

    def get_phone_number(self):
        return self.phone_number

    def set_phone_number(self, phone_number):
            if validate_phone_numbers(phone_number):
                self.phone_number = phone_number
                return True, ""
            else:
                return False, "Invalid phone number. Please try again."

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
            return False, f"Error setting email: {e}"

    def __str__(self):
        return f"Summary for {self.name}:\nStatus: {self.status}\nAddress: {self.address}\nDate of Birth: {self.dob}\nPhone Number: {self.phone_number}\nEmail: {self.email}\n"


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
            validated_dob = datetime(year, month, day)
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

    person_data = dictionary[key_name]
    return str(person_data)

def birthdays(dictionary):
    while True:
        month_choice = input("Enter a month to see all birthdays within it or (E)xit: ")

        if month_choice.lower() == "e":
            break

        try:
            month = int(month_choice) if month_choice.isdigit() else list(calendar.month_name).index(month_choice.capitalize())
            if month < 1 or month > 12:
                raise ValueError("Month must be between 1 and 12. Please try again.")

            today = date.today()
            current_year = today.year
            bdays = []

            for person in dictionary.values():
                dob = datetime.strptime(person.get_dob(), "%d.%m.%Y").date()
                if dob.month == month:
                    this_year = date(current_year, dob.month, dob.day) #the birthday this year
                    last_year = date(current_year -1, dob.month, dob.day) # the birthday last year
                    next_year = date(current_year +1, dob.month, dob.day) # birthday next year
                    name = person.get_name()

                    if this_year > today:#brithday not happened yet
                        days_until = (this_year - today).days
                        days_since = (today - last_year).days
                        next_bday = this_year
                    elif this_year == today:
                        days_until = 0
                        days_since = 0
                        next_bday = next_year
                    else:#has happened
                        days_until = (next_year - today).days
                        days_since = (today - this_year).days
                        next_bday = next_year

                    bdays.append(f"{name}.\n{dob}.\nDays since the last birthday: {days_since}.\nDays until the next birthday: {days_until}.\nNext birthday: {next_bday}.")

            if bdays:
                for people in bdays:
                    print(people)
            else:
                print(f"No birthdays found in {calendar.month_name[month]}.")

        except ValueError as e:
            print(f"Error: {e}")
            continue
        except IndexError:
            print("Error: Invalid month input.")
            continue
        except Exception as e:
            print(f"An unexpected error has occured: {e}")
            continue


def change_values(objt, attribute, new_value, people_data, filename):
    new_value = input_cleaning(new_value)

    if attribute == "Full Name":
        old_name = objt.get_name()
        success, message = objt.set_name(new_value, people_data)
        if success:
            people_data[objt.get_name()] = people_data.pop(old_name)
            write_to("personnel_data.json", people_data)
            return f"New name is {objt.get_name()}"
        return message

    elif attribute == "First Name":
        old_name = objt.get_name()
        full_name = f"{new_value} {objt.get_last_name()}"
        success, message = objt.set_name(full_name, people_data)
        if success:
            people_data[objt.get_name()] = people_data.pop(old_name)
            write_to("personnel_data.json", people_data)
            return f"New first name is {objt.get_first_name()}."
        return message

    elif attribute == "Last Name":
        old_name = objt.get_name()
        full_name = f"{objt.get_first_name()} {new_value}"
        success, message = objt.set_name(full_name, people_data)
        if success:
            people_data[objt.get_name()] = people_data.pop(old_name)
            write_to("personnel_data.json", people_data)
            return f"New last name is {objt.get_last_name()}"
        return message

    elif attribute == "Status":
        success, message = objt.set_status(new_value)
        if success:
            write_to("personnel_data.json", people_data)
            return f"New status is {objt.get_status()}"
        return message

    elif attribute == "Address":
        success, message = objt.set_address(new_value)
        if success:
            write_to("personnel_data.json", people_data)
            return f"New address is {objt.get_address()}"
        return message

    elif attribute == "Date of Birth":
        success, message = objt.set_dob(new_value)
        if success:
            write_to("personnel_data.json", people_data)
            return f"New date of birth is {objt.get_dob()}"
        return

    elif attribute == "Phone Number":
        success, message = objt.set_phone_number(new_value)
        if success:
            write_to("personnel_data.json", people_data)
            return f"New phone number is {objt.get_phone_number()}"
        return message

    elif attribute == "Email Address":
        success, message = objt.set_email(new_value)
        if success:
            write_to("personnel_data.json", people_data)
            return f"New email address is {objt.get_email()}"
        return message

'''
def confirm_info(input_object):
    while True:
        print(input_object)
        print("Press 1 to confirm and add to records.\nPress 2 to redo the entry.\nPress 3 to cancel and exit.\n ")
        confirm = input("Please enter your choice: ")
        if confirm == "1":
            return "add", f"{input_object.get_name()} has been added to the records."
        elif confirm == "2":
            return "redo", "Please redo the entry."
        elif confirm == "3":
            return "exit"
        else:
            print("Invalid choice. Please try again.")
'''
# noinspection SpellCheckingInspection
def filter_view(i, dictionary):
    if i == "View all Data":
        return "\n\n".join(str(person) for person in dictionary.values())#*(person for person in dictionary.values()), "\n"
    elif i == "View Full Names":
        return "\n".join(person.get_name() for person in dictionary.values())
    elif i == "View First Names":
        return "\n".join(person.get_first_name() for person in dictionary.values())
    elif i == "View Last Names":
        return "\n".join(person.get_last_name() for person in dictionary.values())
    elif i == "View Employees":
        return "\n".join(
            f"{person.get_name()}: {person.get_status()}" for person in dictionary.values() if person.get_status() == "Employee")
    elif i == "View Visitors":
        return "\n".join(
            f"{person.get_name()}: {person.get_status()}" for person in dictionary.values() if person.get_status() == "Visitor")
    elif i == "View Addresses":
        return "\n".join(f"{person.get_name()}: {person.get_address()}" for person in dictionary.values())
    elif i == "View Dates of Birth":
        return "\n".join(f"{person.get_name()}: {person.get_dob()}" for person in dictionary.values())
    elif i == "View Phone Numbers":
        return "\n".join(f"{person.get_name()}: {person.get_phone_number()}" for person in dictionary.values())
    elif i == "View Email Addresses":
        return "\n".join(f"{person.get_name()}: {person.get_email()}" for person in dictionary.values())
    else:
        return "Please select an option"

def read_from(filename):
    try:
        with open(filename, "r") as file:
            content = file.read()
            if not content:
                return {}
            data = json.loads(content)
        return {name: PersonData(**person_data) for name, person_data in data.items()}
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON from {filename}. File might be corrupted.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while reading {filename}: {str(e)}")

def write_to(filename, people_data):
    try:
        existing_data = {name: person.__dict__ for name, person in people_data.items()}

        with open(filename, "w") as file:
            json.dump(existing_data, file, indent=4)
    except IOError:
        raise IOError(f"Error writing to file {filename}.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while writing to {filename}: {str(e)}")


def delete_data(filename):
    try:
        with open(filename, "w") as file:
            json.dump({}, file)
    except IOError:
        raise IOError(f"Error clearing file {filename}.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while clearing {filename}: {str(e)}")

# noinspection SpellCheckingInspection
def main():
    filename = "personnel_data.json"
    people_data = read_from(filename)


    questions = [
        "your first and last name: ",
        "your status, please enter \"Employee\" or  \"Visitor?\"",
        "your street and street number, followed by your postcode and city. e.g. Musterstraße 14 0123 Musterstadt: ",
        "your date of birth in the DD.MM.YYYY format: ",
        "your telephone number including the country code e.g. +43660123456: ",
        "your email address: "
    ]


    while True:
        person = PersonData("", "", "", "", "", "", "", "")
        print(
            "Please enter one of the following:\nEnter \"1\" to input new information\n"
            "Enter \"2\" to view stored data\n"
            "Enter \"3\" to edit stored data\n"
            "Enter \"4\" to view Birthdays.\n"
            "Enter \"5\" to clear databank.\n"
            "Enter \"6\" to exit.")
        user_input = input("Enter your choice: ").strip()

        if user_input == "6":
            write_to(filename, people_data)
            break

        elif user_input == "5":
            confirm = input("Enter \"y\" to clear stored data, or any key to exit: ")
            if confirm.lower() == "y":
                extra_confirm = input("Are you sure? Enter \"y\" again to confirm, or any key to exit: ")
                if extra_confirm.lower() == "y":
                    delete_data(filename)
                    continue
                else:
                    continue
            else:
                continue

        elif user_input == "4":
            if len(people_data) > 0:
                birthdays(people_data)
            else:
                print(f"Database is empty, add information before querying")
            continue

        elif user_input == "3":
            if len(people_data) > 0:
                while True:
                    user_input = capitalize_name(input(
                        "Please enter a full name to edit the relevant information or enter \"4\" to return to the main menu\nEnter your input now: "))
                    if user_input == "4":
                        break
                    elif user_input.strip() in people_data:
                        person = people_data[user_input.strip()]
                        old_name = person.get_name()
                        change_values(person, people_data)
                        if person.get_name() != old_name:
                            people_data[person.get_name()] = people_data.pop(old_name)
                            write_to(filename, people_data)
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
                    user_input = input(
                        "Enter \"1\" to select a person to view.\nEnter \"2\" to view everyone based on a catagory.\nEnter \"3\" to view all data\nEnter \"4\"to quit\nEnter your input now: ")
                    if user_input == "4":
                        break
                    elif user_input == "3":
                        for items in people_data.values():
                            print(items)
                    elif user_input == "2":
                        while True:
                            user_input = input(
                                "Please choose a catagory to view from the following:\n1 for name.\n2 for status.\n3 for address.\n4 for date of birth.\n5 for phone number.\n6 for email address.\n7 to exit.\nEnter you input now: ")
                            if user_input == "7":
                                break
                            filter_view(user_input, people_data)

                    elif user_input == "1":
                        user_input = capitalize_name(
                            input("Please enter a full name to see the relevant information: "))
                        if user_input.strip() in people_data:
                            print(f"Information for {show_info(people_data, user_input.strip())}")
                    else:
                        print("Invalid input, please try again.")
                    new_input = input(
                        "Enter \"1\" to view different data sets, or any key to continue back to the main menu: \n")
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

                    elif "status" in item:
                        if person.set_status(user_input):
                            print(f"Valid status: {person.get_status()}")
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

        while True:
            result = confirm_info(person)
            if result == "add":
                people_data[person.get_name()] = person
                write_to(filename, people_data)
                print("Information entry complete.")
                print(f"Added {person.get_name()} to dict. current size: {len(people_data)}")
                break
            elif result == "redo":
                if change_values(person, people_data) == "7":
                    print("Information changed.")
                    continue
            elif result == "exit":
                print("Information entry not completed. Exiting.")
                break
            else:
                print("Invalid input, please try again.")


if __name__ == "__main__":
    main()