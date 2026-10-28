# Issues Found: bank_account_system.py

Line numbers refer to the original file (see the `*_before.txt` reports).
Ordered by severity, high first.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Weak MD5 hash for PINs (Bandit B324, High) | Security | 44 | `hashlib.md5` is cryptographically broken and fast to brute-force. A 4-digit PIN hashed with unsalted MD5 can be cracked instantly. | Replaced with salted `hashlib.pbkdf2_hmac("sha256", ...)` using a random salt from `os.urandom(16)`. |
| Shell command with string concatenation (Bandit B605, High) | Security | 55 | `os.system("echo ... " + filename)` starts a shell, so a crafted filename could inject arbitrary commands. | Removed `os.system` and used `print("Backup complete:", filename)`. |
| Use of `eval` on input (Bandit B307 / Pylint W0123, Medium) | Security | 39 | `eval(expr)` executes arbitrary code passed in as a string. `ast.literal_eval` cannot evaluate `bal * 0.05`, so it is not a drop-in fix. | Changed signature to `compute_bonus(acc_id, rate)` and return `balance * rate`. No string evaluation. |
| Hardcoded secret and secret printed (Bandit B105, Low) | Security | 59, 70 | `admin_token` is hardcoded in source and then printed to the console, leaking it to logs and the repo. | Read it from `os.environ.get("ADMIN_TOKEN")` and print only whether it is configured. |
| Bare `except` with `pass` (Bandit B110, Pylint W0702, Flake8 E722, Low) | Bug | 20-23 | Every error is silently swallowed, including typos and missing accounts, so a failed deposit looks successful. | Removed try/except. Check that the account exists and the amount is positive, and return `True`/`False`. |
| Non-cryptographic `random` for PIN (Bandit B311, Low) | Security | 47-48 | `random.randint` is predictable and unsuitable for generating PINs. | Replaced with `secrets.randbelow(9000) + 1000`. |
| Mutable default argument (Pylint W0102) | Bug | 11 | `transactions=[]` is created once and shared across all calls. | Removed the parameter and used a module-level `transactions` ledger. |
| Transaction log is lost (not flagged by tools) | Logic | 11-16 | The ledger list was local to `createAccount` and never returned or stored, so the log was discarded. | Module-level `transactions` list that persists across calls. |
| `service_fee` defined but never charged (Pylint W0612, Flake8 F841) | Logic | 27 | The fee is assigned but `withdraw` never applies it, so withdrawals are fee-free. | Added `SERVICE_FEE` constant and deducted `amount + SERVICE_FEE` from the balance. |
| File opened without `with` or encoding (Pylint R1732, W1514) | Bug | 52-54 | If `write` fails, the file is never closed. Encoding is platform-dependent. | Used `with open(filename, "w", encoding="utf-8") as f:`. |
| `deposit` accepts invalid amounts (not flagged by tools) | Logic | 19-23 | Negative or zero deposits are accepted silently. | Reject `amount <= 0` and unknown accounts. |
| Unused variable `bal` (Pylint W0612, Flake8 F841) | Style | 38 | `bal` was assigned but never used directly because `eval` took a string. | Removed along with `eval`. |
| Unused import `sys` (Pylint W0611, Flake8 F401) | Style | 6 | Imported but never used. | Deleted the import. |
| Comparison to `None` with `==` (Pylint C0121, Flake8 E711) | Style | 28 | Should use identity comparison for `None`. | Replaced with `acc_id not in account_data`. |
| Unnecessary `else` after `return` (Pylint R1705) | Style | 30 | The `else` branch is redundant after a `return`. | Removed `else` and de-indented. |
| Function name not snake_case (Pylint C0103) | Style | 11 | `createAccount` violates PEP 8 naming. | Renamed to `create_account` and updated the call in `main()`. |
| Old-style `%` string formatting (Pylint C0209) | Style | 15 | Should use an f-string. `%d` also truncates decimal balances. | Used an f-string. |
| Missing docstrings (Pylint C0116) | Style | 11, 19, 26, 37, 43, 47, 51, 58 | None of the functions are documented. | Added a one-line docstring to each function. |
| Line too long, 89 > 79 (Flake8 E501) | Style | 15 | Exceeds the PEP 8 line limit. | Wrapped the `append(...)` call across lines. |
| Missing final newline (Pylint C0304, Flake8 W292) | Style | 70 | File does not end with a newline. | Added a trailing newline. |
| `main()` runs on import (not flagged by tools) | Bug | 70 | Importing the module executes the demo and writes `backup.txt`. | Wrapped in `if __name__ == "__main__":`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.62/10 | 10/10 |
| Bandit | 6 issues (2 High, 1 Medium, 3 Low) | 0 issues |
| Flake8 | 7 issues | 5 issues (related to blanks lines after each code block)  |