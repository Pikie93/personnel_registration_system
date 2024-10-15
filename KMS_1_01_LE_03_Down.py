from email_validator import validate_email, EmailNotValidError
import phonenumbers, re, datetime

# full name ({1}[A-Z])+[a-z]+(\s+{1}[A-Z])+[a-z]
# address ^[A-Za-z\s.-]+\s+[0-9A-Za-z]+(\s+(?:Apt|Top|Unit|Zimmer)\s+[A-Za-z0-9-],\s*([A-Za-z\s]+)\s+(\d{4})$
# D.O.B done
# telephone done
# email done
# other rel data?
#
# error checking, correct input form etc.
#
# feedback on valid input or error
'''
def validate_email_address(email_address):
    try:
        v = validate_email(email_address)
        email_address = v["email"]
        return True, email_address
    except EmailNotValidError as e:
        return False, str(e)

def validate_phone_numbers(check_number):
    try:
        check_number = phonenumbers.parse(check_number)
        return phonenumbers.is_valid_number(check_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False, "Invalid phone number."

def validate_dob(dob):
    dob_pattern = r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19[2-9][0-9]|20[0-1][0-9]|202[0-4])$'
    dob = re.sub("-", ".", dob)
    if re.match(pattern, dob):
        try:
            day, month, year = map(int, dob.split('.'))
            datetime.datetime(year, month, day)
            return True
        except ValueError:
            return False
    return False

def validate_address(check_address):
    address_pattern = r'^([A-Za-zäöüÄÖÜß\s.-]+)\s+(\d+)\s*(\d{4})\s+([A-Za-zäöüÄÖÜß\s.-]+)$'
    if re.match(address_pattern, check_address, re.UNICODE):
        return True
    else:
         return False

def validate_name(check_name):
    name_pattern = r'([A-ZÄÖÜ]{1})+[a-zäöüß]+\s+([A-ZÄÖÜ]{1})+[a-zäöüß]'
    if re.match(name_pattern, check_name, re.UNICODE):
        return True
    else:
        return False
'''

questions = ["your first and last name: ", "your address: ", "your date of birth: ", "your telephone number with the country code: ", "your email address: "]
user_input = ""
input_dict = {}
#make in for max attetmps, make dict for manual reviews and dict for failed input. on fail add name to failed input
#and failed attempts + 1, if name already in faield attempts also +1, if failed attempts >=3 break and add info to manual review dict.

while user_input.casefold() != "quit":
    print("Please enter the following information, or type quit, to end.")
    input_info = []

    for item in questions:
        user_input = input(f"Please enter {item}")
        if user_input.casefold() == "quit":
            break

        if "name" in item:
            name_pattern = r'([A-ZÄÖÜ]{1})+[a-zäöüß]+\s+([A-ZÄÖÜ]{1})+[a-zäöüß]'
            if re.match(name_pattern, user_input, re.UNICODE):
                if user_input in input_dict:
                    print("This name already exists in records. Please use a different name, or type quit to end.")
                    break
                input_info.append(user_input)
                print("Valid name.")
            else:
                print("Invalid name format. Please try again.")
                continue

        elif "address" in item:
            address_pattern = r'^([A-Za-zäöüÄÖÜß\s.-]+)\s+(\d+)\s*(\d{4})\s+([A-Za-zäöüÄÖÜß\s.-]+)$'
            if re.match(address_pattern, user_input, re.UNICODE):
                input_info.append(user_input)
                print("Valid address")
            else:
                print("Invalid address format. Please try again")
                continue

        elif "date of birth" in item:
            dob_pattern = r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19[2-9][0-9]|20[0-1][0-9]|202[0-4])$'
            user_input = re.sub("-", ".", user_input)
            if re.match(dob_pattern, user_input):
                try:
                    day, month, year = map(int, user_input.split('.'))
                    datetime.datetime(year, month, day)
                    input_info.append(user_input)
                    print("Valid date of birth")
                except ValueError:
                    print("Invalid date of birth. Please try again.")
                    continue
            else:
                print("Invalid date of birth. Please try again.")
                continue

        elif "telephone" in item:
            try:
                check_number = phonenumbers.parse(user_input)
                if phonenumbers.is_valid_number(check_number):
                    input_info.append(user_input)
                    print("Valid phone number.")
                else:
                    print("Invalid phone number. Please try again.")
                    continue
            except phonenumbers.phonenumberutil.NumberParseException:
                print("Invalid phone number format. Please try again.")
                continue

        elif "email" in item:
            try:
                v = validate_email(user_input)
                email_address = v["email"]
                input_info.append(email_address)
                print("Valid email address.")
            except EmailNotValidError as e:
                print(f"Invalid email address: {str(e)}. Please try again.")
                continue


        if user_input.casefold() != "quit" and len(input_info) == len(questions):
            input_dict[input_info[0]] = input_info[1:]
            print(f"Information for {input_info[0]} has been successfully added to the records.")

        if user_input.casefold() == "quit:":
            break



