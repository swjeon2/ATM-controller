import sys
from controller import ATMController, ATMState

class ConsoleUI:
    def __init__(self, controller: ATMController):
        """
        컨트롤러를 주입받아 사용자와 상호작용하는 텍스트 UI 클래스
        """
        self.atm = controller

    def _print_header(self, title: str):
        print(f"\n{'='*40}")
        print(f" {title.center(38)}")
        print(f"{'='*40}")

    def run(self):
        """
        메인 실행 루프입니다. 컨트롤러의 상태에 따라 다른 화면을 출력합니다.
        """
        self._print_header("WELCOME TO SIMPLE ATM")
        
        while True:
            try:
                # 1. 카드 삽입 대기 상태
                if self.atm.state == ATMState.IDLE:
                    print("\n[SYSTEM] Please insert your card.")
                    card_num = input(">> Card Number (or 'q' to shutdown): ").strip()
                    
                    if card_num.lower() == 'q':
                        print(">> System shutting down. Goodbye.")
                        sys.exit()
                    
                    if self.atm.insert_card(card_num):
                        print(">> Card recognized.")
                    else:
                        print(">> Error: Invalid Card.")

                # 2. PIN 번호 인증 상태
                elif self.atm.state == ATMState.AUTHENTICATING:
                    pin = input("\n[AUTH] Enter your 4-digit PIN (or 'c' to cancel): ").strip()
                    
                    if pin.lower() == 'c':
                        self.atm.eject_card()
                        print(">> Transaction cancelled.")
                        continue

                    if self.atm.enter_pin(pin):
                        print(">> Authentication successful.")
                    else:
                        print(">> Error: Invalid PIN. Please try again.")

                # 3. 계좌 선택 상태 (N:M 매핑 지원)
                elif self.atm.state == ATMState.ACCOUNT_SELECTION:
                    print(f"\n[SELECT] Found {len(self.atm.accounts)} account(s) linked to this card:")
                    for idx, acc in enumerate(self.atm.accounts, 1):
                        # 보안상 잔액은 여기서 보여주지 않거나, 필요시 출력 가능
                        print(f" {idx}. Account ID: {acc.account_id}")
                    
                    print(" c. Cancel and Eject Card")
                    
                    choice = input(">> Select Account ID or Number: ").strip()
                    
                    if choice.lower() == 'c':
                        self.atm.eject_card()
                        continue

                    # 인덱스(숫자)로도 선택 가능하게 편의성 제공
                    selected_id = choice
                    if choice.isdigit() and 1 <= int(choice) <= len(self.atm.accounts):
                        selected_id = self.atm.accounts[int(choice)-1].account_id

                    if self.atm.select_account(selected_id):
                        print(f">> Account [{selected_id}] selected.")
                    else:
                        print(">> Error: Invalid selection.")

                # 4. 거래 메뉴 상태
                elif self.atm.state == ATMState.TRANSACTION_MENU:
                    self._print_header(f"Account: {self.atm.selected_account.account_id}")
                    print(" 1. View Balance")
                    print(" 2. Deposit Cash")
                    print(" 3. Withdraw Cash")
                    print(" 4. Cancel / Logout")
                    
                    menu = input(">> Choose an option: ").strip()

                    if menu == '1':
                        # 잔액 조회 후에는 메뉴 상태 유지
                        balance = self.atm.check_balance()
                        print(f"\n[RESULT] Current Balance: ${balance}")
                        input("Press Enter to return to menu...")

                    elif menu == '2':
                        try:
                            amount = int(input("\n[DEPOSIT] Enter amount ($1 units): "))
                            if self.atm.deposit(amount):
                                print(f">> ${amount} deposited successfully.")
                                print(">> SECURITY: Auto-logging out and ejecting card.") #
                            else:
                                print(">> Error: Invalid amount.")
                        except ValueError:
                            print(">> Error: Please enter a numeric value.")

                    elif menu == '3':
                        try:
                            amount = int(input("\n[WITHDRAW] Enter amount ($1 units): "))
                            if self.atm.withdraw(amount):
                                print(f">> ${amount} dispensed. Please take your cash.")
                                print(">> SECURITY: Auto-logging out and ejecting card.") #
                            else:
                                # 잔액 부족 혹은 현금함 부족
                                print(">> Error: Insufficient funds or ATM cash stock.")
                        except ValueError:
                            print(">> Error: Please enter a numeric value.")

                    elif menu == '4':
                        self.atm.eject_card()
                        print(">> Card ejected. Thank you.")

            except Exception as e:
                print(f"\n[SYSTEM ERROR] {e}")
                self.atm.eject_card()