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

def capitalize_name(name):
    def capitalize_hyphen(part):
        return '-'.join(word.capitalize() for word in part.split'-'))
    return ' '.join(part.capitalize() for part in name.split())
'''