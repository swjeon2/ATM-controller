from enum import Enum, auto
from interfaces import BankService, CashBin
from models import Card, Account

class ATMState(Enum):
    IDLE = auto()
    AUTHENTICATING = auto()
    ACCOUNT_SELECTION = auto()
    TRANSACTION_MENU = auto()

class ATMController:
    def __init__(self, bank_service: BankService, cash_bin: CashBin):
        self.bank = bank_service
        self.cash_bin = cash_bin
        self._reset_session()

    def _reset_session(self):
        self.state = ATMState.IDLE
        self.current_card = None
        self.accounts = []
        self.selected_account = None

    def insert_card(self, card_number: str):
        """UI에서 받은 문자열을 Card 객체로 변환하여 저장합니다"""
        if self.state == ATMState.IDLE:
            # 문자열을 Card 객체로 생성
            self.current_card = Card(card_number=card_number) 
            self.state = ATMState.AUTHENTICATING
            return True
        return False

    def enter_pin(self, pin: str) -> bool:
        if self.state != ATMState.AUTHENTICATING:
            return False
        
        # PIN을 저장하지 않고 결과만 받음
        if self.bank.verify_pin(self.current_card.card_number, pin):
            self.accounts = self.bank.get_accounts(self.current_card.card_number)
            self.state = ATMState.ACCOUNT_SELECTION
            return True
        return False

    def select_account(self, account_id: str) -> bool:
        if self.state != ATMState.ACCOUNT_SELECTION:
            return False
        
        for acc in self.accounts:
            if acc.account_id == account_id:
                self.selected_account = acc
                self.state = ATMState.TRANSACTION_MENU
                return True
        return False

    def check_balance(self) -> int:
        if self.state == ATMState.TRANSACTION_MENU:
            return self.selected_account.balance
        raise PermissionError("Access Denied")

    def deposit(self, amount: int) -> bool:
        if self.state != ATMState.TRANSACTION_MENU or amount <= 0:
            return False
        
        if self.bank.update_balance(self.selected_account.account_id, amount):
            self.selected_account.balance += amount
            self.eject_card() # 보안상 자동 로그아웃
            return True
        return False

    def withdraw(self, amount: int) -> bool:
        if self.state != ATMState.TRANSACTION_MENU or amount <= 0:
            return False

        # 잔액 확인 및 현금함 재고 확인
        if self.selected_account.balance >= amount and self.cash_bin.has_enough_cash(amount):
            if self.bank.update_balance(self.selected_account.account_id, -amount):
                self.cash_bin.dispense(amount)
                self.selected_account.balance -= amount
                self.eject_card() # 보안상 자동 로그아웃
                return True
        return False

    def eject_card(self):
        self._reset_session()