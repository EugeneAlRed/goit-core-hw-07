from collections import UserDict
import re
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def get_name(self):
        return str(self.value)


class Phone(Field):
    def __init__(self, value):
        pattern = r'^\d{10}$'
        if not re.match(pattern, value):
            return "Invalid phone number format. The phone number must contain 10 digits"
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d-%m-%Y')
            return self.value
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        self.phones = [num for num in self.phones if num.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for num in self.phones:
            if num.value == old_phone:
                num.value = new_phone

    def find_phone(self, phone):
        return [str(num) for num in self.phones if num.value == phone]

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(num.value for num in self.phones)}, birthday: {self.birthday.value if self.birthday else 'Not indicated'}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        date_now = datetime.today().date()
        birthday = []
        for user in self.data.values():
            birthday_date = user['birthday']
            birthday_date = str(date_now.year) + birthday_date[4:]
            birthday_date = datetime.strptime(birthday_date, '%Y.%m.%d').date()
            day_difference = (birthday_date - date_now).days
            day_week = birthday_date.isoweekday()
            if day_difference >= 0 and day_difference < 7:
                if day_week < 6:
                    birthday.append(
                        {'name': user['name'], 'birthday': birthday_date.strftime('%Y.%m.%d')})
                else:
                    if (birthday_date + timedelta(day=2)).weekday() == 0:
                        birthday.append({'name': user['name'], 'birthday': (
                            birthday_date + timedelta(day=2)).strftime('%Y.%m.%d')})
                    elif (birthday_date + timedelta(day=1)).weekday() == 0:
                        birthday.append({'name': user['name'], 'birthday': (
                            birthday_date + timedelta(day=1)).strftime('%Y.%m.%d')})
        return birthday


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "No such name found"
        except IndexError:
            return "Not found"
        except Exception as e:
            return f'Error: {e}'

    return inner


@input_error
def add_birthday(args, book):
    name, birthday = args
    try:
        record = book.find(name)
        if record:
            record.add_birthday(birthday)
            print(f"Birthday for {name} added.")
        else:
            print(f"{name} not found in address book")
    except ValueError as e:
        print(e)


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        print(f"{name} birthday : {record.birthday.value}")
    elif record and not record.birthday:
        print(f"{name} no birthday information")
    else:
        print(f"{name} not found")


@input_error
def birthday(args, book):
    upcoming_birthday = book.get_upcoming_birthday()
    if upcoming_birthday:
        print("Upcoming birthday:")
        for record in upcoming_birthday:
            print(
                f" Don't forget to congratulate {record['name']} is {record['congratulation_date']}")
    else:
        print("No upcoming birthdays")


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            if len(args) < 2:
                print("Invalid command. Please provide both name and phone number")
                continue
            name, new_phone = args
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            print(f"{name:12}: {phone:12} ")


        # elif command == 'change':
        #     print(change_contacts(args, contacts))
        # elif command == "phone":
        #     print(show_phone(args, contacts))
        # elif command == 'all':
        #     print("All contacts:")
        #     for record in book.data.values():
        #         print(record)
        # else:
        #     print("Invalid command.")
