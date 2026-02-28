import hashlib

class SimpleATMDatabase:
    def __init__(self):
        # 초기 데이터를 생성할 때 PIN을 해시화하여 저장함
        self._data = {
            "0000-0000-0000-0000": {"pin": self._hash_pin("0000"), "account": "00000-00000", "balance": 0},
            "1111-1111-1111-1111": {"pin": self._hash_pin("1111"), "account": "11111-11111", "balance": 1000},
            "2222-2222-2222-2222": {"pin": self._hash_pin("2222"), "account": "22222-22222", "balance": 2000},
            "3333-3333-3333-3333": {"pin": self._hash_pin("3333"), "account": "33333-33333", "balance": 3000},
            "4444-4444-4444-4444": {"pin": self._hash_pin("4444"), "account": "44444-44444", "balance": 4000},
            "5555-5555-5555-5555": {"pin": self._hash_pin("5555"), "account": "55555-55555", "balance": 5000},
        }

    def _hash_pin(self, pin: str) -> str:
        """SHA-256을 이용한 간단한 PIN 암호화"""
        return hashlib.sha256(pin.encode()).hexdigest()

    def find_user(self, card_number: str):
        return self._data.get(card_number)

    def verify_pin_hash(self, card_number: str, input_pin: str) -> bool:
        """입력받은 PIN을 해시화하여 저장된 값과 비교함"""
        user = self.find_user(card_number)
        if user:
            return user["pin"] == self._hash_pin(input_pin)
        return False

    def update_balance(self, card_number: str, new_balance: int):
        if card_number in self._data:
            self._data[card_number]["balance"] = new_balance
            return True
        return False