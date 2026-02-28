import hashlib
from .models import Account

class SimpleATMDatabase:
    def __init__(self):
        # 1. 실제 계좌 데이터 (공유 저장소)
        self._accounts = {
            "00000-00000": Account("00000-00000", 0),
            "11111-11111": Account("11111-11111", 1000),
            "22222-22222": Account("22222-22222", 2000),
            "33333-33333": Account("33333-33333", 3000),
            "44444-44444": Account("44444-44444", 4000),
            "55555-55555": Account("55555-55555", 5000),
            "99999-99999": Account("99999-99999", 99999) # 공유 테스트용 고액 계좌
        }

        # 2. 카드 데이터: PIN과 연결된 계좌 ID 리스트를 가짐
        self._cards = {
            "0000-0000-0000-0000": {"pin": self._hash_pin("0000"), "acc_ids": ["00000-00000", "99999-99999"]}, # 다중 계좌
            "1111-1111-1111-1111": {"pin": self._hash_pin("1111"), "acc_ids": ["11111-11111", "99999-99999"]}, # 99999 계좌 공유
            "2222-2222-2222-2222": {"pin": self._hash_pin("2222"), "acc_ids": ["22222-22222"]},
            "3333-3333-3333-3333": {"pin": self._hash_pin("3333"), "acc_ids": ["33333-33333"]},
            "4444-4444-4444-4444": {"pin": self._hash_pin("4444"), "acc_ids": ["44444-44444"]},
            "5555-5555-5555-5555": {"pin": self._hash_pin("5555"), "acc_ids": ["55555-55555"]},
        }

    def _hash_pin(self, pin: str) -> str:
        return hashlib.sha256(pin.encode()).hexdigest()

    def get_card_info(self, card_number: str):
        return self._cards.get(card_number)

    def verify_pin_hash(self, card_number: str, input_pin: str) -> bool:
        card = self.get_card_info(card_number)
        return card is not None and card["pin"] == self._hash_pin(input_pin)

    def get_account(self, acc_id: str):
        """계좌 풀에서 실제 계좌 객체를 가져옴 (공유 참조)"""
        return self._accounts.get(acc_id)