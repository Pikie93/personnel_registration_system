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
    pattern = r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19[2-9][0-9]|20[0-1][0-9]|202[0-4])$'
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
input_info = []
input_dict = {}
'''
name = "Jam Dw"#input("Please enter your last name: ")
address = "Moserhofgasse 31 8010 Graz "#input("Please enter your address: ")
date_of_birth = "12-12-2020"#input("Please enter your date of birth: ")
telephone = "+436609523819"#input("Please enter your telephone number with the country code, for example +43 for Austria: ")
email = "adwada@grgdrg.com"#input("Please enter your email address: ")
'''
while user_input.casefold() != "quit":
    print("Please enter the following information, or type quit, to end.")
    for items in questions:
        user_input = input(f"Please enter {items}")
        if user_input.casefold() == "quit":
            break

        input_info.append(user_input)
    input_dict[input_info[0]].append(input_info[1:])



#print(input_info)
#print(user_input)
print(input_dict)


