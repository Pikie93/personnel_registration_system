from email_validator import validate_email, EmailNotValidError
import phonenumbers, re, datetime

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
            day, month, year = map(int, user_input.split('.'))
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
    return ' '.join(part for part in u_input.split()).strip()

questions = ["your first and last name: ", "your street and street number, followed by your postcode and city. e.g. Musterstraße 14 0123 Musterstadt: ", "your date of birth in the DD.MM.YYYY format: ", "your telephone number including the country code e.g. +43660123456: ", "your email address: "]
input_dict = {}
user_input = ""

while True:
    print("Please enter the following information, or type quit, to end.")
    input_info = []

    for item in questions:
        while True:
            user_input = input_cleaning(input(f"Please enter {item}"))
            if user_input.casefold() == "quit":
                break

            if "name" in item:
                corrected_name = validate_name(user_input)
                if corrected_name:
                    if corrected_name in input_dict:
                        print("This name already exists in records. Please use a different name, or type quit to end.")
                    else:
                        input_info.append(corrected_name)
                        print(f"Valid name: {corrected_name}")
                        break
                else:
                    print("Invalid name format. Please try again.")

            elif "street" in item:
                if validate_address(user_input):
                    input_info.append(user_input)
                    print(f"Valid address: {user_input}")
                    break
                else:
                    print("Invalid address format. Please try again")

            elif "date of birth" in item:
                if validate_dob(user_input):
                        input_info.append(user_input)
                        print(f"Valid date of birth: {user_input}")
                        break
                else:
                    print("Invalid date of birth. Please try again.")

            elif "telephone" in item:
                if validate_phone_numbers(user_input):
                    input_info.append(user_input)
                    print(f"Valid phone number: {user_input}")
                    break
                else:
                    print(f"Invalid phone number format. Please try again.")

            elif "email" in item:
                if validate_email_address(user_input):
                    input_info.append(user_input)
                    print(f"Valid email address: {user_input}")
                    break

        if user_input.casefold() == "quit":
            break

    if user_input.casefold() == "quit":
        break

    if len(input_info) == len(questions):
        input_dict[input_info[0]] = input_info[1:]
        print(f"Information for {input_info[0]} has been successfully added to the records.")
    else:
        print("Information entry was not completed.")