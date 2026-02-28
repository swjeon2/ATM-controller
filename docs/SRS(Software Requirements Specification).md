# SRS: Simple ATM Controller System

## 1. Introduction
### 1.1 Project Overview
The objective of this project is to implement a **functional ATM Controller** that manages the core logic of an Automated Teller Machine. The system will handle the interaction between the user, the bank's backend API, and the physical cash bin hardware.

### 1.2 Goals
* **Decoupling:** Ensure a clear separation between the controller logic, the bank service, and the hardware interfaces.
* **Extensibility:** Design the system using interfaces to allow easy integration with real-world Bank APIs and Cash Bin hardware in the future.
* **Testability:** Enable comprehensive unit testing of the controller logic by utilizing mock implementations of external dependencies.

---

## 2. System Actors
* **Primary Actor:** **Customer** (User) - Interacts with the ATM to manage their accounts.
* **Secondary Actors:**
    * **Bank API:** Validates credentials and processes financial transactions.
    * **Cash Bin:** Represents the physical hardware responsible for storing and dispensing cash.

---

## 3. Requirements

### 3.1 Functional Requirements (FR)
| ID | Requirement | Description |
| :--- | :--- | :--- |
| **FR-1** | **Insert Card** | The system must be able to read card information and transition to the authentication state. |
| **FR-2** | **PIN Authentication** | The system must verify the PIN via the Bank API. It should allow access only if the PIN is correct. |
| **FR-3** | **Account Selection** | Upon successful authentication, the system must retrieve a list of accounts associated with the card and allow the user to select one. |
| **FR-4** | **Balance Inquiry** | The system must provide the current balance of the selected account. |
| **FR-5** | **Deposit** | The system must allow users to deposit funds, updating the balance through the Bank API. |
| **FR-6** | **Withdrawal** | The system must allow users to withdraw funds if: <br>1. The account balance is sufficient. <br>2. The ATM's Cash Bin has enough physical currency. |

### 3.2 Non-Functional Requirements (NFR)
| ID | Requirement | Description |
| :--- | :--- | :--- |
| **NFR-1** | **Interface-Based Design** | Dependencies (Bank, CashBin) must be abstracted through interfaces to support future hardware/software swaps. |
| **NFR-2** | **Integer Precision** | All monetary values are represented as integers (1 USD = 1 unit). No decimal/cent handling is required. |
| **NFR-3** | **Security** | The controller shall only receive the PIN verification result (True/False) from the Bank API and must not store or have direct access to the actual PIN. |
| **NFR-4** | **UI Independence** | The controller must be purely logic-driven, allowing any UI (CLI, GUI, or Web) to be built on top of it. |

---

## 4. Use Case : Scenario

**Main Flow:**
1. **Insert Card:** Customer inserts their card.
2. **Enter PIN:** Customer enters their PIN.
3. **Authorize:** Controller sends the card and PIN to the **Bank API** for validation.
4. **Select Account:** Controller retrieves and displays account list; Customer selects an account.
5. **Perform Transaction:**
    * **Inquiry:** Customer views balance.
    * **Deposit:** Customer adds funds.
    * **Withdraw:** Customer requests cash -> Controller checks **Bank API** (balance) and **Cash Bin** (stock) -> Cash is dispensed -> **Bank API** is updated.

---

## 5. Constraints & Assumptions
* **Currency:** Only $1 bills are supported.
* **Implementation:** Actual network communication (REST, RPC) and hardware drivers are out of scope.
* **Security:** Physical security of the ATM and encryption of the PIN during transit are not handled in this version.