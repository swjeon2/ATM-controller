from database import SimpleATMDatabase
from interfaces import BankService, CashBin
from controller import ATMController
from ui import ConsoleUI
from models import Account

class BankServiceWithDB(BankService):
    """
    추상 인터페이스인 BankService를 상속받아 실제 DB와 통신하는 구현체
    """
    def __init__(self, db: SimpleATMDatabase):
        self.db = db

    def verify_pin(self, card_number: str, pin: str) -> bool:
        """
        DB를 통해 PIN 해시값을 비교합니다. 컨트롤러에는 성공 여부(bool)만 반환
        """
        return self.db.verify_pin_hash(card_number, pin)

    def get_accounts(self, card_number: str):
            card_info = self.db.get_card_info(card_number)
            if not card_info: return []
            
            # [핵심] DB에서 get_account()를 통해 '원본 객체'를 리스트에 담아 반환합니다.
            return [self.db.get_account(aid) for aid in card_info["acc_ids"] if self.db.get_account(aid)]

    def update_balance(self, account_id: str, amount: int) -> bool:
        account = self.db.get_account(account_id)
        if account:
            # 원본 객체의 값을 직접 수정합니다.
            account.balance += amount
            return True
        return False

class MockCashBin(CashBin):
    """
    ATM 하드웨어 현금함을 모사하는 클래스입니다.
    """
    def __init__(self, initial_stock: int = 10000):
        self.stock = initial_stock  # $1 bills count

    def has_enough_cash(self, amount: int) -> bool:
        """출금 전 물리적 현금 재고를 확인합니다."""
        return self.stock >= amount

    def dispense(self, amount: int) -> bool:
        """현금을 실제로 배출하고 재고를 차감합니다."""
        if self.has_enough_cash(amount):
            self.stock -= amount
            return True
        return False

def main():

    # [Data Layer] 인메모리 DB 생성 (6개의 기본 데이터 포함)
    db = SimpleATMDatabase()

    # [Service Layer] DB를 주입받은 은행 서비스 생성
    bank_service = BankServiceWithDB(db)

    # [Hardware Layer] 현금함 생성
    cash_bin = MockCashBin(initial_stock=5000)

    # [Core Logic Layer] 컨트롤러에 서비스와 하드웨어 주입 (Dependency Injection)
    atm_controller = ATMController(bank_service, cash_bin)

    # [Presentation Layer] UI에 컨트롤러 주입 및 실행
    atm_ui = ConsoleUI(atm_controller)
    
    try:
        atm_ui.run()
    except KeyboardInterrupt:
        print("\n\n>> System force closed. Security session wiped.")
    except Exception as e:
        print(f"\n>> Critical System Error: {e}")

if __name__ == "__main__":
    main()