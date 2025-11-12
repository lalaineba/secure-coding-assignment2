"""
Description: A class to manage bank account objects.
"""
__author__ = "Lalaine Balmediano"
__version__ = "3.0.0"

from abc import ABC, abstractmethod
from datetime import date
from patterns.observer.observer import Observer
from patterns.observer.subject import Subject

class BankAccount(Subject, ABC):
    """
    BankAccount class: Maintains bank account data.
    """ 
    #Class constants
    LARGE_TRANSACTION_THRESHOLD = 9999.99
    LOW_BALANCE_LEVEL = 50.0

    def __init__(self, account_number: int,
                 client_number: int,
                 balance: float,
                 date_created: date):
        """
        Initializes the class attributes with argument values.
        
        Args:
            account_number (int): An integer value representing the 
            bank account number.
            client_number (int): An integer value representing the client 
            number representing the account holder.
            balance (float): A float value representing the current balance of
            the bank account.
            date_created (date): Represents a date in the calendar.

        Raises:
            ValueError: When the account number and client numbers are not 
            integers.
        """
        super().__init__()

        if isinstance(account_number, int):
            self.__account_number = account_number
        else:
            raise ValueError("Account number must be an integer.")
        
        if isinstance(client_number, int):
            self.__client_number = client_number
        else:
            raise ValueError("Client number must be an integer.")
        
        if isinstance(balance, (int, float)):
            self.__balance = float(balance)
        else: 
            self.__balance = 0

        if isinstance(date_created, date):
            self._date_created = date_created
        else:
            self._date_created = date.today()
            
    # ACCESSORS
    @property
    def account_number(self) -> int:
        """
        Accessor for the account_number attribute.
        
        Returns:
            int: The bank account number of the client.
        """
        return self.__account_number
    
    @property
    def client_number(self) -> int:
        """
        Accessor for the client_number attribute.
        
        Returns:
            int: The client number of the account holder.
        """
        return self.__client_number

    @property
    def balance(self) -> float:
        """
        Accessor for the balance attribute.

        Returns:
            float: The current balance of the bank account. 
        """
        return self.__balance
    
    def update_balance(self, amount: float):
        """
        Updates the balance of the BankAccount so that the amount received is 
        added to the current account balance.
        
        Args: 
            amount (float): The amount of transaction. 
        """
        if isinstance(amount, (int, float)):
            update_balance = float(amount + self.__balance)
            self.__balance = update_balance
        
        if self.__balance < BankAccount.LOW_BALANCE_LEVEL:
            message = (f"Low balance warning ${self.__balance:,.2f}: "
                    + f"on account {self.__account_number}.")
            
            self.notify(message)
        
        if abs(amount) > BankAccount.LARGE_TRANSACTION_THRESHOLD:
            message = (f"Large transaction ${amount:,.2f}: on account "
                       + f"{self.__account_number}.")
            
            self.notify(message)
            
    def deposit(self, amount: float):
        """
        Deposit and update the balance of the BankAccount if the amount 
        received is positive and valid. 

        Args:
            amount (float): The amount of transaction. 

        Raises:
            ValueError: When the amount received is non-numeric and negative.
        """
        if not isinstance(amount, (int, float)):
            raise ValueError(f"Deposit amount: {amount} must be numeric.")

        if amount < 0:
            raise ValueError(f"Deposit amount: "
                             + f"${amount:,.2f} must be positive.")
        
        self.update_balance(amount)

    def withdraw(self, amount: float):
        """
        Withdraw and update the balance of the BankAccount if the amount 
        received is positive and valid. 

        Args:
            amount (float): The amount of transaction. 

        Raises:
            ValueError: When the amount received is non-numeric, negative, and 
            has exceeded the current balance.
        """
        if not isinstance(amount, (int, float)):
            raise ValueError(f"Withdraw amount: {amount} must be numeric.")

        if amount < 0:
            raise ValueError(f"Withdrawal amount: "
                             + f"${amount:,.2f} must be positive.")

        if amount > self.__balance:
            raise ValueError(f"Withdrawal amount: "
                             + f"${amount:,.2f} must not exceed the "
                             + f"account balance: ${self.__balance:,.2f}")

        self.update_balance(-amount)
    
    def __str__(self) -> str:
        """
        Return a string representation of the class instance.

        Returns:
            str: A string representation of the account number and balance.
        """
        return (f"Account Number: {self.__account_number} "
                + f"Balance: ${self.__balance:,.2f}\n")

    @abstractmethod
    def get_service_charges(self) -> float:
        """
        Returns the calculated service charges that a BankAccount will incur.
        To be implemented in subclasses.
        """
        pass

    def attach(self, observer: Observer):
        """
        Attaches observers to the subject.

        Args:
            observer (Observer): The observer attached to the subject.
        """
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        """
        Detaches observers from the subject.

        Args:
            observer (Observer): The observer detached from the subject.
        """
        self._observers.remove(observer)

    def notify(self, message: str):
        """
        Notifies observers when an event takes place.

        Args:
            message (str): The string representation of the alert message. 
        """
        for observer in self._observers:
            observer.update(message)

