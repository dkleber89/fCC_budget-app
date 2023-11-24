"""Budget handler"""
from __future__ import annotations
import math
from typing import TypedDict

class LedgerElement(TypedDict):
    """LedgerElement Dict"""
    amount: float
    description: str

class Category:
    """Small Budget Category handler"""
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.ledger: list[LedgerElement] = []

    def get_balance(self) -> float:
        """Get Balance of category

        Returns:
            float: Balance of category
        """
        balance: float = 0.0

        for element in self.ledger:
            balance += element.get("amount")

        return balance

    def check_funds(self, amount: float) -> bool:
        """Check is amount of money available

        Args:
            amount (float): Amount of money to check if available

        Returns:
            bool: Given amount of money is available
        """
        return self.get_balance() >= amount

    def deposit(self, amount: float, description: str = "") -> None:
        """Deposit money

        Args:
            amount (float): Deposit amount
            description (str, optional): Deposit description text. Defaults to "".
        """
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount: float, description: str = "") -> bool:
        """Withdraw money

        Args:
            amount (float): Withdraw amount
            description (str, optional): Withdraw description text. Defaults to "".

        Returns:
            bool: Operation successful
        """
        if self.check_funds(amount):
            self.ledger.append({"amount": amount * -1.0, "description": description})
            return True

        return False

    def transfer(self, amount: float, destination: Category) -> bool:
        """Transfer a amount of money from this category to a destination category

        Args:
            amount (float): Transfer amount
            destination (Category): Destination category

        Returns:
            bool: Operation successful
        """
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + destination.name)
            destination.deposit(amount, "Transfer from " + self.name)

            return True

        return False

    def __str__(self) -> str:
        result = self.name.center(30, "*") + "\n"

        for element in self.ledger:
            amount = f"{element.get('amount'):0.2f}"
            amount_len = len(amount)

            description = element.get("description")[:23]
            description_len = len(description)

            line = description + "".rjust(30 - amount_len - description_len, " ") + amount + "\n"
            result += line

        total = "Total: " + f"{self.get_balance():0.2f}"

        result += total

        return result


class Withdraw(TypedDict):
    """Withdraw Dict"""
    name: str
    amount: float

class XAxis(TypedDict):
    """XAxis Dict"""
    name: str
    value: int

def create_spend_chart(categories: list[Category]) -> str:
    """Show Categories in a Bar Chart

    Args:
        categories (list[Category]): List of Categories to show in Chart

    Returns:
        str: Chart
    """
    withdraws: list[Withdraw] = []

    for category in categories:
        withdraw_sum = 0.0

        for ledger_element in category.ledger:
            amount = ledger_element.get("amount")

            if amount < 0:
                withdraw_sum += amount * -1.0

        withdraws.append({"name": category.name, "amount": withdraw_sum})

    overall_withdraw = 0

    for withdraw in withdraws:
        overall_withdraw += withdraw.get("amount")

    y_axis = ["100", "90", "80", "70", "60", "50", "40", "30", "20", "10", "0"]
    x_axis: list[XAxis] = []
    max_name_length = 0

    for withdraw in withdraws:
        withdraw_percent = math.floor(100.0 / overall_withdraw * withdraw.get("amount") / 10.0) * 10
        x_axis.append({"name": withdraw.get("name"), "value": withdraw_percent })
        max_name_length = max(max_name_length, len(withdraw.get("name")))


    result = "Percentage spent by category" + "\n"

    for y_element in y_axis:
        result += (y_element + "|").rjust(4, " ")

        y_value = int(y_element)
        empty = "   "
        full = " o "

        for x_element in x_axis:
            if x_element.get("value") >= y_value:
                result += full
            else:
                result += empty

        result += " \n"

    result += "    " + "".rjust(len(x_axis) * 3, "-") + "-\n"

    i = 0
    while i < max_name_length:
        line = "    "

        for x_element in x_axis:
            element = ""

            try:
                element = " " + x_element.get("name")[i] + " "
            except IndexError:
                element = "   "

            line += element

        result += line + " "

        if i < max_name_length - 1:
            result += "\n"

        i += 1

    print(result)

    return result
