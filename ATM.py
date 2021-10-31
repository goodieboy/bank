from decimal import Decimal
from random import choice


class ATM:
    db_content = None
    is_logged_in = False
    first_name = ""
    last_name = ""
    phone = ""
    account_number = ""
    pin = ""
    balance = None
    db_row_number = None
    exit_key = 'q'

    def __init__(self):
        print("###########################################################")
        print("################ Welcome To JAIZ Bank #####################")
        print("###########################################################")
        self.load_db_data()
        print(self.db_content)
        self.begin()

    def prepare_quit(self):
        return self.save_to_db()

    def save_to_db(self):
        d = [self.first_name, self.last_name, self.phone, self.account_number, self.pin, str(self.balance)]
        to_str = ",".join(d)+"\n"
        self.db_content[self.db_row_number] = to_str
        file = open("db.txt", 'w')
        file.writelines(self.db_content)
        file.close()

    def check_quit(self, val):
        if val == self.exit_key:
            print("Are you sure you want to quit? \n Press Y/n?")
            opt = str(input()).lower()
            if opt == "y":
                self.prepare_quit()
                return True
            else:
                return False
        return False

    def begin(self):
        opt = input("What will you like to do today? \n"
                    "Type L to Login to your account \n"
                    "Type R to Register a new account\n"
                    "Press Q to quit at any point")
        opt = str(opt).lower()
        if opt == 'l':
            return self.login()
        elif opt == 'r':
            return self.register()
        elif opt == 'q':
            return self.check_quit()
        else:
            print("Sorry, Invalid option selected. Pls try again")
            return self.begin()

    def load_db_data(self):
        d = open('db.txt', 'r')
        df = d.readlines()
        d.close()
        self.db_content = df

    def login(self):
        account_number = input("Please supply your account number ::  ")
        pin = input("Please supply your account pin ::  ")
        cont = "%s,%s" % (account_number,pin)
        if self.validate_login(cont):
            print("Login successful")
            self.is_logged_in = True
            print(self.db_row_number)
            print(self.first_name)
            return self.post_login_operations()
        else:
            print("Login failed")
            return self.login()

    def validate_login(self, data):
        for ind, i in enumerate(self.db_content):
            if str(i).__contains__(data):
                obj = str(i).strip("\n").split(",")
                self.first_name = obj[0]
                self.last_name = obj[1]
                self.phone = obj[2]
                self.account_number = obj[3]
                self.pin = obj[4]
                self.balance = Decimal(obj[5])
                self.db_row_number = ind
                return True
        return False

    def post_login_operations(self):
        print(" Welcome %s, What will you like to do?" % str(self.first_name).title())
        opt = input("Press D for Deposit \n Press W for Withdraw \n Press B to check your balance")
        opt = str(opt).lower()
        if opt == 'd':
            return self.make_deposit()
        elif opt == 'w':
            return self.make_withdraw()
        elif opt == 'b':
            return self.check_balance()
        else:
            print("Invalid option selected. Pls try again later")
            return self.post_login_operations()

    def check_balance(self):
        self.login_required()
        print("You balance is %s" % str(self.balance))
        print("")
        print("")
        print("")
        print("")
        return self.post_login_operations()

    def make_withdraw(self):
        self.login_required()
        amt = input("Enter the amount you want to withdraw:: ")
        try:
            amt = int(amt)
        except:
            print("You must enter an integer value. Pls try again")
            return self.make_withdraw()
        if amt <= self.balance:
            self.balance -= amt
            print("You have successfully withdraw %s from your account. Your new balance is %s" % (amt, self.balance))
            self.save_to_db()
            return self.post_login_operations()
        else:
            print("Operation Denied. Insufficient balance")
            return self.post_login_operations()

    def login_required(self):
        if not self.is_logged_in:
            print("Sorry, You have to login before making this operation")
            return self.login()

    def make_deposit(self):
        self.login_required()
        amt = input("Enter the amount you want to deposit:: ")
        try:
            amt = int(amt)
        except:
            print("You must enter an integer value. Pls try again")
            return self.make_deposit()

        self.balance += amt
        print("You have successfully deposit %s from your account. Your new balance is %s" % (amt, self.balance))
        self.save_to_db()
        return self.post_login_operations()

    def register(self):
        first_name = input("Please supply your first name ::  ")
        last_name = input("Please supply your last name ::  ")
        phone = input("Please supply your phone ::  ")

        if not first_nlame or not last_name or not phone:
            print(" sorry. All fields are required")
            return self.register()
        account_no = self.generate_digits(10)
        pin = self.generate_digits(4)
        user_details = [first_name,last_name,phone,account_no,pin,"0"]
        ud = ",".join(user_details)+"\n"
        """Save to txt file"""
        f = open("db.txt", 'a')
        f.write(ud)
        f.close()
        print("Account created successfully. Your details is as below \n"
              " First name: %s \n Last name: %s \n Phone: %s\n Account Number: %s \n Pin: %s" % (first_name, last_name, phone,account_no,pin))
        return self.begin()

    def generate_digits(self, length):
        v = []
        while length > 0:
            v.append(str(choice([0,1,2,3,4,5,6,7,8,9])))
            length -= 1
        return "".join(v)


app = ATM()