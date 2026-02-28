from dataclasses import dataclass

@dataclass
class Card:
    card_number: str

@dataclass
class Account:
    account_id: str
    balance: int = 0  # $1 bills only