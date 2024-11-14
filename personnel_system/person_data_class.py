from personnelRegistrationSystem.personnel_system.validation_logic import *

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