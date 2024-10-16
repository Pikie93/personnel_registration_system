from email_validator import validate_email, EmailNotValidError
import phonenumbers, re, datetime

questions = ["your first and last name: ", "your street and street number, followed by your postcode and city. e.g. Musterstraße 14 0123 Musterstadt: ", "your date of birth in the DD.MM.YYYY format: ", "your telephone number including the country code e.g. +43660123456: ", "your email address: "]
input_dict = {}
user_input = ""

while True:
    print("Please enter the following information, or type quit, to end.")
    input_info = []

    for item in questions:
        while True:
            user_input = input(f"Please enter {item}")
            if user_input.casefold() == "quit":
                break

            if "name" in item:
                name_pattern = r'^([A-Za-zÄÖÜäöüß]+(-[A-Za-zÄÖÜäöüß]+)?)\s+([A-Za-zÄÖÜäöüß]+(-[A-Za-zÄÖÜäöüß]+)?)$'
                if re.match(name_pattern, user_input, re.UNICODE):
                    corrected_name = ' '.join('-'.join(word.capitalize() for word in part.split('-'))for part in user_input.split())

                    if corrected_name in input_dict:
                        print("This name already exists in records. Please use a different name, or type quit to end.")
                    else:
                        input_info.append(corrected_name)
                        print(f"Valid name: {corrected_name}")
                        break
                else:
                    print("Invalid name format. Please try again.")


            elif "street" in item:
                address_pattern = r'^([A-Za-zäöüÄÖÜß\s-]+)\s+(\d+)(?:\s((?:Apt|Apartment|Top|Unit|Flat|/)\.?\s*\d+))?\s+(\d{4})\s+([A-Za-zäöüÄÖÜß\s.-]+)$'
                if re.match(address_pattern, user_input, re.UNICODE):
                    input_info.append(user_input)
                    print(f"Valid address: {user_input}")
                    break
                else:
                    print("Invalid address format. Please try again")


            elif "date of birth" in item:
                dob_pattern = r'^(0?[1-9]|[12][0-9]|3[01])\.(0?[1-9]|1[0-2])\.(19[2-9][0-9]|20[0-1][0-9]|202[0-4])$'
                user_input = re.sub(r'[-/,_]', ".", user_input)
                if re.match(dob_pattern, user_input):
                    try:
                        day, month, year = map(int, user_input.split('.'))
                        datetime.datetime(year, month, day)
                        input_info.append(user_input)
                        print(f"Valid date of birth: {user_input}")
                        break
                    except ValueError:
                        print("Invalid date of birth. Please try again.")

                else:
                    print("Invalid date of birth. Please try again.")


            elif "telephone" in item:
                try:
                    check_number = phonenumbers.parse(user_input)
                    if phonenumbers.is_valid_number(check_number):
                        input_info.append(user_input)
                        print(f"Valid phone number: {user_input}")
                        break
                    else:
                        print("Invalid phone number. Please try again.")

                except phonenumbers.phonenumberutil.NumberParseException:
                    print("Invalid phone number format. Please try again.")


            elif "email" in item:
                try:
                    email_address = validate_email(user_input).normalized
                    input_info.append(email_address)
                    print(f"Valid email address: {user_input}")
                    break
                except EmailNotValidError as e:
                    print(f"Invalid email address: {str(e)}. Please try again.")

        if user_input.casefold() == "quit":
            break

    if user_input.casefold() == "quit":
        break

    if len(input_info) == len(questions):
        input_dict[input_info[0]] = input_info[1:]
        print(f"Information for {input_info[0]} has been successfully added to the records.")
    else:
        print("Information entry was not completed.")






