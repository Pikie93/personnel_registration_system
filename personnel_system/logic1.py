from datetime import datetime, date
import re, calendar, json
import person_data_class

def input_cleaning(u_input):
    u_input = u_input.strip()
    u_input = re.sub(r'\s+', ' ', u_input)

    if re.search(r'\d+[\s./-]+\d+[\s./-]+\d+', u_input):
        u_input = re.sub(r'\s', '', u_input)
    return u_input


def birthdays(month, dictionary):
        try:
            month = list(calendar.month_name).index(month)
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
                return "\n\n".join(str(bday) for bday in bdays)
            else:
                  return  f"No birthdays found in {calendar.month_name[month]}."

        except Exception as e:
            raise Exception (f"An unexpected error has occurred: {e}")


def change_values(objt, attribute, new_value, people_data, filename):
    new_value = input_cleaning(new_value)

    if attribute == "Full Name":
        old_name = objt.get_name()
        success, message = objt.set_name(new_value, people_data)
        if success:
            people_data[objt.get_name()] = people_data.pop(old_name)
            write_to(filename, people_data)
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


def filter_view(i, dictionary):
    if i == "View all Data":
        return "\n\n".join(str(person) for person in dictionary.values())
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
        return {name: person_data_class.PersonData(**person_data) for name, person_data in data.items()}
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
            json.dump(existing_data, file, indent=4) #type: ignore
    except IOError:
        raise IOError(f"Error writing to file {filename}.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while writing to {filename}: {str(e)}")


def delete_data(filename, person_choice=None):
    if person_choice is None:
        try:
            with open(filename, "w") as file:
                json.dump({}, file) #type: ignore
            return f"{filename} successfully cleared."
        except IOError:
            raise IOError(f"Error clearing file {filename}.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while clearing {filename}: {str(e)}")
    else:
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            del data[person_choice]

            with open(filename, "w") as file:
                json.dump(data, file, indent=4) #type: ignore
            return f"{person_choice} removed from database."
        except Exception as e:
            raise Exception(f"An unexpected error occurred while deleting {person_choice}: {str(e)}")
