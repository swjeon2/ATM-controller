import unittest
from code.controller import ATMController, ATMState
from code.database import SimpleATMDatabase
from code.models import Account, Card
from code.main import BankServiceWithDB, MockCashBin

class TestATMController(unittest.TestCase):
    def setUp(self):
        """테스트 시작 전 매번 독립적인 시스템 환경을 구축합니다."""
        self.db = SimpleATMDatabase()
        self.bank = BankServiceWithDB(self.db)
        self.cash_bin = MockCashBin(initial_stock=5000)
        self.atm = ATMController(self.bank, self.cash_bin)

    def test_invalid_card_insertion(self):
        """DB에 없는 카드 번호 삽입 시 IDLE 상태를 유지하는지 테스트합니다."""
        result = self.atm.insert_card("9999-9999-9999-9999")
        self.assertFalse(result)
        self.assertEqual(self.atm.state, ATMState.IDLE)

    def test_valid_card_and_pin_auth(self):
        """정상 카드와 PIN 입력 시 계좌 선택 단계로 전이되는지 테스트합니다."""
        self.atm.insert_card("0000-0000-0000-0000")
        auth_result = self.atm.enter_pin("0000")
        self.assertTrue(auth_result)
        self.assertEqual(self.atm.state, ATMState.ACCOUNT_SELECTION)
        self.assertGreater(len(self.atm.accounts), 0)

    def test_shared_account_consistency(self):
        """서로 다른 카드가 하나의 계좌(99999)를 공유할 때 잔액이 동기화되는지 테스트합니다."""
        # 1. 0000 카드로 $100 입금
        self.atm.insert_card("0000-0000-0000-0000")
        self.atm.enter_pin("0000")
        self.atm.select_account("99999-99999")
        initial_balance = self.atm.check_balance()
        self.atm.deposit(100) # 입금 후 자동 로그아웃됨

        # 2. 1111 카드로 접속하여 잔액 확인
        self.atm.insert_card("1111-1111-1111-1111")
        self.atm.enter_pin("1111")
        self.atm.select_account("99999-99999")
        new_balance = self.atm.check_balance()
        
        self.assertEqual(new_balance, initial_balance + 100)

    def test_auto_logout_after_transaction(self):
        """입금 또는 출금 성공 시 즉시 IDLE 상태로 복귀하는지 테스트합니다."""
        self.atm.insert_card("2222-2222-2222-2222")
        self.atm.enter_pin("2222")
        self.atm.select_account("22222-22222")
        
        # 출금 수행
        self.atm.withdraw(500)
        
        # 보안상 즉시 초기 상태로 돌아갔는지 확인
        self.assertEqual(self.atm.state, ATMState.IDLE)
        self.assertIsNone(self.atm.current_card)

    def test_insufficient_atm_cash(self):
        """ATM 현금함 재고보다 많은 금액 출금 시도시 실패하는지 테스트합니다."""
        self.atm.insert_card("5555-5555-5555-5555") # 잔액 $5000
        self.atm.enter_pin("5555")
        self.atm.select_account("55555-55555")
        
        # 현금함 재고(5000)보다 많은 금액 출금 시도
        result = self.atm.withdraw(6000)
        self.assertFalse(result)
        self.assertEqual(self.atm.state, ATMState.TRANSACTION_MENU)

if __name__ == "__main__":
    unittest.main()