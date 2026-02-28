# Simple ATM Controller System

이 프로젝트는 객체지향 설계 원칙을 준수하여 개발된 **모듈형 ATM 컨트롤러 시스템**입니다. 단순한 기능 구현을 넘어, 실제 은행 시스템의 확장성과 보안성을 고려한 아키텍처를 지향합니다.

---

## 🚀 설계 문서 (Design Artifacts)
시스템의 상세 요구사항과 설계 구조는 아래 문서에서 확인하실 수 있습니다.
* **[SRS (Software Requirements Specification)](https://github.com/swjeon2/ATM-controller/blob/main/docs/SRS(Software%20Requirements%20Specification).md)**
* **[SDD (Software Design Description)](https://github.com/swjeon2/ATM-controller/blob/main/docs/SDD(Software%20Design%20Description).md)**

---

## ✨ 주요 기능 (Key Features)

### 1. 기본 금융 거래
* **잔액 조회 (Balance Inquiry)**: 선택된 계좌의 현재 잔고를 실시간으로 확인합니다.
* **입금 (Deposit)**: $1 단위로 현금을 입금하며, 성공 시 즉시 데이터베이스에 반영됩니다.
* **출금 (Withdrawal)**: 계좌 잔액과 ATM 기기의 물리적 현금 재고를 동시에 확인한 후 출금을 수행합니다.

### 2. 유연한 계좌 매핑 (N:M Mapping)
* **다중 계좌 매핑**: 하나의 카드에 여러 개의 계좌를 연결하여 선택할 수 있습니다.
* **공유 계좌 지원**: 서로 다른 카드들이 하나의 특정 계좌를 공유하여 사용할 수 있는 실무적인 구조를 제공합니다.

### 3. 강력한 보안 기능
* **PIN 암호화**: SHA-256 단방향 해시 알고리즘을 사용하여 사용자의 PIN 번호를 안전하게 보호합니다.
* **자동 로그아웃 (Auto-Logout)**: 입금 및 출금과 같은 물리적 거래 완료 후 보안을 위해 즉시 세션을 종료하고 카드를 배출합니다.
* **카드 유효성 검사**: DB에 등록되지 않은 카드가 삽입될 경우 즉시 차단하여 불필요한 인증 과정을 방지합니다.

---

## 🏗️ 시스템 아키텍처 (Architecture)

본 시스템은 **Modular Layered Architecture**를 채택하여 각 계층 간의 의존성을 최소화했습니다.


* **Core Controller**: 상태 머신(FSM)을 기반으로 전체 거래 흐름을 제어합니다.
* **Abstraction Layer**: 인터페이스(ABC)를 통해 은행 서비스와 하드웨어를 추상화하여, 실제 하드웨어가 없어도 Mock 객체로 테스트가 가능합니다.
* **Persistence Layer**: 인메모리 DB를 통해 데이터의 일관성을 유지합니다.

---

## 🛠️ 설치 및 실행 (Setup & Run)

### Clone Repository
```bash
git clone [https://github.com/swjeon2/ATM-controller.git](https://github.com/swjeon2/ATM-controller.git)
cd ATM-controller
python3 code/main.py
```
## 📊 초기 테스트 데이터 (Initial Data)
시스템 실행 시 아래와 같은 초기 데이터가 로드됩니다. (시스템 재시작 시 초기값으로 리셋됩니다.)

| 카드 번호 | PIN | 연결된 계좌 ID | 비고 |
| :--- | :--- | :--- | :--- |
| `0000-0000-0000-0000` | `0000` | `00000-00000`, `99999-99999` | 다중 계좌 보유 |
| `1111-1111-1111-1111` | `1111` | `11111-11111`, `99999-99999` | **99999-99999 계좌 공유** |
| `2222-2222-2222-2222` | `2222` | `22222-22222` | |
| `3333-3333-3333-3333` | `3333` | `33333-33333` | |
| `4444-4444-4444-4444` | `4444` | `44444-44444` | |
| `5555-5555-5555-5555` | `5555` | `55555-55555` | |

> **💡 Tip**: `0000...` 카드와 `1111...` 카드로 각각 접속하여 **99999-99999** 계좌의 잔액이 공유되는지 테스트해 보세요!

---

* **`main.py`**: 시스템의 모든 객체를 조립하고 실행하는 **엔트리 포인트** (의존성 주입 수행).
* **`code/controller.py`**: ATM의 상태 머신(FSM)과 핵심 **비즈니스 로직** 담당.
* **`code/ui.py`**: 사용자 입력을 처리하고 상태별 화면을 출력하는 **텍스트 UI**.
* **`code/database.py`**: SHA-256 기반 **PIN 해싱** 및 인메모리 데이터 저장소 관리.
* **`code/interfaces.py`**: 시스템 간 결합도를 낮추기 위한 **추상 인터페이스**(Abstract Base Classes).
* **`code/models.py`**: `Card`, `Account` 등 시스템에서 사용하는 **데이터 모델**.

---

## ✅ 테스트 실행 (Unit Testing)

시스템의 신뢰성을 보장하기 위해 `unittest` 프레임워크를 활용한 자동화 테스트를 포함하고 있습니다.

### 테스트 명령어
프로젝트 루트 폴더(`atm/`)에서 아래 명령어를 실행합니다.

```bash
python3 -m tests.unit_test
```