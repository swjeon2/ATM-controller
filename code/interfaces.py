from abc import ABC, abstractmethod
from typing import List
from models import Account

class BankService(ABC):
    @abstractmethod
    def verify_pin(self, card_number: str, pin: str) -> bool:
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