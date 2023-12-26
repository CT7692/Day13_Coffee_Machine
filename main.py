import menu as m


# Function Definitions:


def intro():
    print("\nWelcome to the Cyber Cafe! \nBrewing coffee from 1s and 0s!\nMenu: ")
    for i in m.MENU:
        print(i + ": " + "${:,.2f}".format(m.MENU[i]["cost"]))


def validator(option_list, prompt):
    user_input = input(prompt)
    correct = False
    for i in option_list:
        if user_input == i:
            correct = True
    if not correct:
        while not correct:
            print("\nPlease enter a valid option.")
            user_input = input(prompt)
            for i in option_list:
                if user_input == i:
                    correct = True
    return user_input


def coin_validator(prompt):
    correct = True
    num_coins = input(prompt)
    if not num_coins.isnumeric():
        correct = False
        while not correct:
            print("Please enter the number of coins you're paying with.")
            num_coins = input(prompt)
            if num_coins.isnumeric():
                correct = True
    num_coins = int(num_coins)
    return num_coins


def report(earnings):
    print("\nResources: ")
    print(f"Water: {m.resources['water']}ml")
    print(f"Milk: {m.resources['milk']}ml")
    print(f"Coffee: {m.resources['coffee']}g")
    print("Money: " + f"${earnings:,.2f}\n")


def check_resources(selection):
    sufficient = True
    for i in m.resources:
        if i in m.MENU[selection]["ingredients"]:
            if m.resources[i] < m.MENU[selection]["ingredients"][i]:
                sufficient = False
                print(f"We're sorry. There is not enough {i}.")
    return sufficient


def deduct_resources(selection):
    for i in m.resources:
        if i in m.MENU[selection]["ingredients"]:
            m.resources[i] -= m.MENU[selection]["ingredients"][i]


def insert_coins(my_coins):
    coin_prompt = ""
    payment = 0
    for i in my_coins:
        coin_prompt = f"How many {i} are you inserting? "
        num_coins = coin_validator(coin_prompt)
        if num_coins >= 1:
            change_amount = my_coins[i] * num_coins
            payment += change_amount
    return payment


def check_transaction(selection, payment, coffee_earnings):
    payment_success = False
    price = m.MENU[selection]["cost"]
    if payment == price:
        payment_success = True
        print(f"\nHere is your {selection}. Enjoy!")
    elif payment > price:
        payment_success = True
        change = payment - price
        print(f"\nHere is your {selection}. Enjoy!")
        print(f"\nYou entered ${payment:,.2f}.")
        print("Your Change: " + f"${change:,.2f}")
    elif payment < price:
        payment_success = False
        print(f"\nYou entered ${payment:,.2f}.")
        if payment > 0:
            print("Insufficient funds.\nChange refunded.")
    return payment_success


# Functions Defined.


coins = {"pennies": 0.01, "nickels": 0.05, "dimes": 0.10, "quarters": 0.25}
select_list = ["espresso", "latte", "cappuccino", "report", "off"]
earnings = 0
on = True
select_prompt = "What would you like? "
while on:
    intro()
    if (choice := validator(select_list, select_prompt)) == "report":
        report(earnings)
    elif choice == "off":
        on = False
        print("Good-bye.")
    else:
        can_order = check_resources(choice)
        if can_order:
            print("\nYour total is " + f"${m.MENU[choice]['cost']:,.2f}.")
            payment = insert_coins(coins)
            transaction_success = check_transaction(choice, payment, earnings)
            if transaction_success:
                deduct_resources(choice)
                earnings += m.MENU[choice]["cost"]
