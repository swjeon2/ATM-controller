from abc import ABC, abstractmethod
from typing import List
from models import Account, Card

class BankService(ABC):
    @abstractmethod
    def verify_pin(self, card_number: str, pin: str) -> bool:
        """은행은 PIN 번호를 주지 않고 맞는지 여부만 반환함"""
        pass

    @abstractmethod
    def get_accounts(self, card_number: str) -> List[Account]:
        pass

    @abstractmethod
    def update_balance(self, account_id: str, amount: int) -> bool:
        pass

class CashBin(ABC):
    @abstractmethod
    def has_enough_cash(self, amount: int) -> bool:
        pass

    @abstractmethod
    def dispense(self, amount: int) -> bool:
        pass