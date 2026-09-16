# Adam Heier - ICT703 Task 2 - Python Program

Bank Transaction Fraud Detection System. These six files are the complete submission (`Adam Heier - Task 2.zip`).

Run with `python main.py`, test with `python test.py` from the program folder. The `output/` folder with the CSV results is created by the program itself.

## Contents

- [`main.py`](#mainpy) - Main program
- [`fraud_detection.py`](#fraud_detectionpy) - Program logic (all classes)
- [`test.py`](#testpy) - Test program
- [`transactions.txt`](#transactionstxt) - Transaction data
- [`accounts.csv`](#accountscsv) - Customer account data
- [`rules_config.json`](#rules_configjson) - Rule configuration

## `main.py`

*Main program*

```python
"""
Program: main.py
Author: Adam Heier
Last date modified: 16/09/2026

The purpose of this program is to find suspicious activity in a file of
fictional bank transaction records (ICT703 Assessment Task 2). It reads
the records from transactions.txt, validates them, stores the valid
records, applies the fraud-detection rules and displays the suspicious
transactions and accounts.

Run the program with "python main.py" and the tests with "python
test.py". All files are opened with relative paths.
"""

from fraud_detection import (AccountAnalyser, AccountLoader, AlertStore,
                             DataFileError, FraudDetector, RuleConfig,
                             SummaryReport, TransactionLoader,
                             TransactionStore, TransactionValidator,
                             use_program_folder)

TRANSACTION_FILE = "transactions.txt"   # The records that are analysed
ACCOUNT_FILE = "accounts.csv"          # Customer accounts, a CSV file
CONFIG_FILE = "rules_config.json"      # Thresholds, rule names, severity
INVALID_RECORD_FILE = "output/invalid_records.csv"
VALID_RECORD_FILE = "output/valid_transactions.csv"
ALERT_FILE = "output/alerts.csv"
SUMMARY_FILE = "output/summary_report.csv"
LINE_WIDTH = 74                        # Character width of a heading


def print_heading(title):
    """Print a section heading in a consistent style."""
    print()
    print("=" * LINE_WIDTH)
    print(title)
    print("=" * LINE_WIDTH)


def print_invalid_records(invalid_records):
    """Print every rejected record with its line number and reason."""
    print_heading("REJECTED RECORDS")
    if not invalid_records:
        print("All records passed the validation checks.")
        return
    print(f"{len(invalid_records)} records were not used in the analysis:")
    print()
    for record in invalid_records:
        print(f"  Line {record.line_number:>3} | field: {record.field_name}")
        print(f"           Reason: {record.reason}")
        print(f"           Record: {record.raw_line}")
        print()


def print_alerts(alert_store):
    """Print every fraud alert, most serious alerts first."""
    print_heading("SUSPICIOUS ACTIVITY")
    if alert_store.count() == 0:
        print("No suspicious activity was found.")
        return
    print(f"{alert_store.count()} alerts were created for "
          f"{len(alert_store.suspicious_account_ids())} accounts:")
    print()
    for alert in alert_store.sorted_by_severity():
        print(f"  [{alert.severity}] {alert.rule_name}")
        print(f"    Account      : {alert.account_id}")
        print(f"    Transactions : {alert.transaction_id_text()}")
        if alert.details != "":
            print(f"    Details      : {alert.details}")
        print(f"    Reason       : {alert.reason}")
        print()


def print_account_overview(store, alert_store):
    """Print one line for every account with its alert count."""
    print_heading("ACCOUNT OVERVIEW")
    print(f"  {'Account':<10}{'Transactions':>14}{'Alerts':>10}   Result")
    for account_id in store.account_ids():
        alert_count = len(alert_store.filter_by_account(account_id))
        result = "SUSPICIOUS" if alert_count > 0 else "normal"
        print(f"  {account_id:<10}"
              f"{len(store.transactions_for(account_id)):>14}"
              f"{alert_count:>10}   {result}")


def print_summary(summary):
    """Print the summary statistics of advanced feature 7."""
    print_heading("SUMMARY REPORT")
    statistics = summary.build()
    for label in statistics:
        print(f"  {label:<40}{statistics[label]:>12}")


class FraudDetectionApp:
    """Runs the complete fraud-detection process step by step."""

    def __init__(self):
        """Create the empty data stores that the analysis fills."""
        self.config = None
        self.loader = None
        self.store = TransactionStore()
        self.alert_store = AlertStore()
        self.accounts = {}

    def run(self):
        """Run the six steps of the analysis one after the other."""
        print_heading("BANK TRANSACTION FRAUD DETECTION SYSTEM")
        self.load_configuration()
        if not self.load_transactions():
            return
        self.load_accounts()
        self.run_detection()
        summary = self.show_results()
        self.export_results(summary)
        print()
        print("Analysis finished.")

    def load_configuration(self):
        """Load the fraud-detection settings (advanced feature 4)."""
        self.config = RuleConfig(CONFIG_FILE)
        print(f"Configuration source: {self.config.source}")
        for message in self.config.messages:
            print(f"  Warning: {message}")
        mode = "enhanced" if self.config.enhanced_validation() else "core"
        print(f"Validation mode     : {mode}")

    def load_transactions(self):
        """Read and validate the transaction file."""
        validator = TransactionValidator(self.config.enhanced_validation())
        self.loader = TransactionLoader(validator)
        try:
            self.loader.load(TRANSACTION_FILE, self.store)
        except DataFileError as error:
            print()
            print(f"Error: {error}")
            print("The program cannot continue without transaction data.")
            return False
        print(f"Transaction file    : {TRANSACTION_FILE}")
        print(f"Records read        : {self.loader.total_records}")
        print(f"Valid records       : {self.store.count()}")
        print(f"Rejected records    : {self.loader.invalid_count()}")
        return True

    def load_accounts(self):
        """Read the customer account file (advanced feature 5)."""
        account_loader = AccountLoader()
        try:
            self.accounts = account_loader.load(ACCOUNT_FILE)
        except DataFileError as error:
            print(f"  Warning: {error}")
            print("  The account checks (rules 6 to 9) are skipped.")
            return
        for message in account_loader.messages:
            print(f"  Warning: {message}")
        print(f"Customer accounts   : {len(self.accounts)}")

    def run_detection(self):
        """Apply all fraud-detection rules to the stored transactions."""
        detector = FraudDetector(self.store, self.config)
        self.alert_store.add_all(detector.run_all_rules())
        if self.accounts:
            analyser = AccountAnalyser(self.store, self.accounts,
                                       self.config)
            self.alert_store.add_all(analyser.run_all_checks())

    def show_results(self):
        """Print all results and return the summary report object."""
        print_invalid_records(self.loader.invalid_records)
        print_alerts(self.alert_store)
        print_account_overview(self.store, self.alert_store)
        summary = SummaryReport(self.loader, self.store, self.alert_store)
        print_summary(summary)
        return summary

    def export_results(self, summary):
        """Save the results to CSV files in the output folder."""
        print_heading("EXPORTED FILES")
        if self.loader.export_invalid_records(INVALID_RECORD_FILE):
            print(f"  Saved: {INVALID_RECORD_FILE}")
        if self.store.export_to_csv(VALID_RECORD_FILE):
            print(f"  Saved: {VALID_RECORD_FILE}")
        if self.alert_store.export_to_csv(ALERT_FILE):
            print(f"  Saved: {ALERT_FILE}")
        if summary.export_to_csv(SUMMARY_FILE):
            print(f"  Saved: {SUMMARY_FILE}")


def main():
    """Change to the program folder and start the analysis."""
    use_program_folder()
    FraudDetectionApp().run()


if __name__ == "__main__":
    main()
```

## `fraud_detection.py`

*Program logic (all classes)*

```python
"""
Program: fraud_detection.py
Author: Adam Heier
Last date modified: 16/09/2026

The purpose of this module is to hold all the program logic of the bank
transaction fraud detection system (ICT703 Assessment Task 2): reading
the data files, checking every record, storing the valid records and
applying the fraud-detection rules. It writes nothing to the screen, so
the same classes are used by main.py and by test.py.

Contents:
    1. Helper functions for writing CSV files
    2. Data model classes    - Transaction, Account, InvalidRecord, Alert
    3. Rule configuration    - RuleConfig
    4. Validation            - TransactionValidator, ValidationError
    5. File loading          - TransactionLoader, AccountLoader
    6. Storage               - TransactionStore, AlertStore
    7. Detection rules       - FraudDetector, AccountAnalyser
    8. Summary statistics    - SummaryReport
"""

import csv
import json
import os
from datetime import datetime, timedelta

# --------------------------------------------------------------------
# 1. HELPER FUNCTIONS
# --------------------------------------------------------------------


def use_program_folder():
    """Change to the folder that contains the program files.

    The program opens its data files with relative paths such as
    "transactions.txt". Without this function those files would only be
    found when the program is started from its own folder. Calling it
    first means the program also works when it is started from
    somewhere else, for example from an editor.
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


def write_csv(file_path, header, rows):
    """Write a header row and data rows to a CSV file.

    The folder is created if it does not exist yet. Returns True when
    the file was written successfully.
    """
    folder = os.path.dirname(file_path)
    try:
        if folder != "" and not os.path.isdir(folder):
            os.makedirs(folder)
        with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(rows)
    except OSError as error:
        print(f"  Warning: '{file_path}' could not be written ({error}).")
        return False
    return True

# --------------------------------------------------------------------
# 2. DATA MODEL CLASSES
# --------------------------------------------------------------------


TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"   # Format of section 3.2
DATE_FORMAT = "%Y-%m-%d"                 # Used to group by day


class Transaction:
    """A single bank transaction record."""

    def __init__(self, timestamp, transaction_id, account_id,
                 transaction_type, amount, location, status):
        """Store the seven fields of one transaction record."""
        self.timestamp = timestamp
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.location = location
        self.status = status

    def is_approved(self):
        """Return True if the transaction was approved."""
        return self.status == "APPROVED"

    def is_declined(self):
        """Return True if the transaction was declined."""
        return self.status == "DECLINED"

    def date_text(self):
        """Return the calendar date of the transaction as text."""
        return self.timestamp.strftime(DATE_FORMAT)

    def timestamp_text(self):
        """Return the timestamp of the transaction as text."""
        return self.timestamp.strftime(TIMESTAMP_FORMAT)

    def summary(self):
        """Return a short description used in the alert output."""
        return (f"{self.transaction_type} of ${self.amount:,.2f} "
                f"in {self.location} on {self.timestamp_text()}")


class Account:
    """A customer account record from the account data file."""

    def __init__(self, account_id, account_type, home_location,
                 daily_limit, account_status):
        """Store the five fields of one customer account record."""
        self.account_id = account_id
        self.account_type = account_type
        self.home_location = home_location
        self.daily_limit = daily_limit
        self.account_status = account_status

    def is_active(self):
        """Return True if the account is allowed to be used."""
        return self.account_status == "ACTIVE"

    def __str__(self):
        """Return a readable description of the account."""
        return (f"{self.account_id} ({self.account_type}, "
                f"{self.home_location}, limit ${self.daily_limit:,.2f}, "
                f"{self.account_status})")


class InvalidRecord:
    """A record that failed validation and was not used in the analysis."""

    def __init__(self, line_number, raw_line, field_name, reason):
        """Store where the record came from and why it was rejected."""
        self.line_number = line_number
        self.raw_line = raw_line
        self.field_name = field_name
        self.reason = reason


class Alert:
    """A suspicious transaction or account found by a detection rule."""

    def __init__(self, rule_key, rule_name, severity, account_id,
                 transaction_ids, reason, details=""):
        """Store the result of one triggered fraud-detection rule."""
        self.rule_key = rule_key
        self.rule_name = rule_name
        self.severity = severity
        self.account_id = account_id
        self.transaction_ids = transaction_ids
        self.reason = reason
        self.details = details

    def transaction_id_text(self):
        """Return the related transaction IDs as a single string."""
        if not self.transaction_ids:
            return "-"
        return ", ".join(self.transaction_ids)

# --------------------------------------------------------------------
# 3. RULE CONFIGURATION (ADVANCED FEATURE 4)
# --------------------------------------------------------------------


def default_settings():
    """Return a new dictionary with the built-in default settings.

    These values are used when rules_config.json is missing or damaged,
    so the program always has a complete set of settings to work with.
    """
    return {
        "thresholds": {
            "high_value_amount": 5000.00,
            "declined_count": 4,
            "location_count": 3,
            "rapid_decline_count": 4,
            "rapid_decline_window_minutes": 30,
            "structuring_min_amount": 4500.00,
            "structuring_count": 3,
            "structuring_window_hours": 24,
        },
        "rule_names": {
            "RULE_1": "Rule 1 - High-Value Transaction",
            "RULE_2": "Rule 2 - Repeated Declined Transactions",
            "RULE_3": "Rule 3 - Multiple Locations",
            "RULE_4": "Rule 4 - Rapid Declined Transactions",
            "RULE_5": "Rule 5 - Amounts Just Below Threshold",
            "RULE_6": "Rule 6 - Daily Limit Exceeded",
            "RULE_7": "Rule 7 - Transaction Outside Home Location",
            "RULE_8": "Rule 8 - Activity On Inactive Account",
            "RULE_9": "Rule 9 - Unknown Account",
        },
        "severities": {
            "RULE_1": "HIGH", "RULE_2": "MEDIUM", "RULE_3": "MEDIUM",
            "RULE_4": "HIGH", "RULE_5": "HIGH", "RULE_6": "HIGH",
            "RULE_7": "MEDIUM", "RULE_8": "HIGH", "RULE_9": "LOW",
        },
        "options": {
            "enhanced_validation": True,
        },
    }


class RuleConfig:
    """Fraud-detection settings loaded from a JSON configuration file."""

    def __init__(self, file_path=None):
        """Start with the default settings and load the file if given."""
        self.settings = default_settings()
        self.source = "built-in default settings"
        self.messages = []
        if file_path is not None:
            self.load(file_path)

    def load(self, file_path):
        """Read the configuration file and overwrite the defaults.

        Any problem is stored in self.messages, so that the main
        program can show it and still continue with the defaults.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as config_file:
                file_settings = json.load(config_file)
        except FileNotFoundError:
            self.messages.append(
                f"Configuration file '{file_path}' was not found. "
                f"The default settings are used.")
            return
        except (OSError, ValueError) as error:
            self.messages.append(
                f"Configuration file '{file_path}' could not be read "
                f"({error}). The default settings are used.")
            return

        for section in self.settings:
            if section in file_settings:
                self.settings[section].update(file_settings[section])
        self.source = file_path

    def threshold(self, name):
        """Return the value of one threshold setting."""
        return self.settings["thresholds"][name]

    def rule_name(self, rule_key):
        """Return the display name of a detection rule."""
        return self.settings["rule_names"][rule_key]

    def severity(self, rule_key):
        """Return the severity level of a detection rule."""
        return self.settings["severities"][rule_key]

    def enhanced_validation(self):
        """Return True if the enhanced validation checks are switched on."""
        return self.settings["options"]["enhanced_validation"]

# --------------------------------------------------------------------
# 4. VALIDATION OF TRANSACTION RECORDS
# --------------------------------------------------------------------


FIELD_COUNT = 7                # Fields in one transaction record
VALID_TYPES = ["TRANSFER", "CARD_PAYMENT", "CASH_WITHDRAWAL",
               "ONLINE_PURCHASE", "DIRECT_DEBIT"]
VALID_STATUSES = ["APPROVED", "DECLINED", "PENDING"]


class ValidationError(Exception):
    """Raised when a transaction record does not pass validation."""

    def __init__(self, field_name, reason):
        """Store the field that caused the problem and the reason."""
        super().__init__(reason)
        self.field_name = field_name
        self.reason = reason


class TransactionValidator:
    """Checks records and turns them into Transaction objects."""

    def __init__(self, enhanced=False):
        """Create a validator in core mode or in enhanced mode."""
        self.enhanced = enhanced
        self.seen_transaction_ids = {}
        self.seen_records = {}

    def validate(self, line, line_number=0):
        """Check one record and return a Transaction object.

        Raises a ValidationError if the record must be rejected.
        """
        raw_fields = line.split("|")
        if self.enhanced:
            self._check_duplicate_record(line)
            self._check_spacing(raw_fields)

        fields = [field.strip() for field in raw_fields]
        self._check_field_count(fields)

        timestamp = self._check_timestamp(fields[0])
        transaction_id = self._check_id(fields[1], "Transaction ID",
                                        "transaction_id", "T", 4)
        if self.enhanced and transaction_id in self.seen_transaction_ids:
            raise ValidationError(
                "transaction_id",
                f"Duplicate transaction ID '{transaction_id}', already "
                f"used on line {self.seen_transaction_ids[transaction_id]}")
        account_id = self._check_id(fields[2], "Account ID", "account_id",
                                    "A", 5)
        transaction_type = self._check_from_list(
            fields[3], VALID_TYPES, "transaction_type")
        amount = self._check_amount(fields[4])
        location = self._check_location(fields[5])
        status = self._check_from_list(fields[6], VALID_STATUSES, "status")

        self._remember(transaction_id, line, line_number)
        return Transaction(timestamp, transaction_id, account_id,
                           transaction_type, amount, location, status)

    def _remember(self, transaction_id, line, line_number):
        """Store an accepted record so duplicates can be found later."""
        self.seen_transaction_ids[transaction_id] = line_number
        self.seen_records[line.strip()] = line_number

    def _check_field_count(self, fields):
        """Check that the record contains exactly seven fields."""
        if len(fields) < FIELD_COUNT:
            raise ValidationError(
                "record",
                f"Missing fields: expected {FIELD_COUNT} fields but "
                f"found {len(fields)}")
        if len(fields) > FIELD_COUNT:
            raise ValidationError(
                "record",
                f"Additional fields: expected {FIELD_COUNT} fields but "
                f"found {len(fields)}")

    def _check_timestamp(self, value):
        """Check the timestamp format and return it as a datetime."""
        if value == "":
            raise ValidationError("timestamp", "Timestamp is empty")
        try:
            return datetime.strptime(value, TIMESTAMP_FORMAT)
        except ValueError:
            raise ValidationError(
                "timestamp",
                f"Invalid timestamp '{value}', expected YYYY-MM-DD HH:MM:SS")

    def _check_id(self, value, name, field_name, letter, digits):
        """Check an ID such as T1001 or A10025 and return it.

        Both ID fields follow the same pattern, so one method can check
        them. In core mode only an empty value is rejected. In enhanced
        mode the ID must be the given letter followed by the given
        number of digits.
        """
        if value == "":
            raise ValidationError(field_name, f"{name} is empty")
        if self.enhanced and (len(value) != digits + 1
                              or value[0] != letter
                              or not value[1:].isdigit()):
            raise ValidationError(
                field_name,
                f"Invalid {name} '{value}', expected the letter "
                f"{letter} followed by {digits} digits")
        return value

    def _check_from_list(self, value, allowed_values, field_name):
        """Check that a field contains one of the allowed values."""
        if value in allowed_values:
            return value
        if self.enhanced and value.upper() in allowed_values:
            raise ValidationError(
                field_name,
                f"Inconsistent capitalisation in {field_name} '{value}', "
                f"expected '{value.upper()}'")
        raise ValidationError(
            field_name,
            f"Invalid {field_name} '{value}', allowed values are "
            f"{', '.join(allowed_values)}")

    def _check_amount(self, value):
        """Check the amount and return it as a number."""
        try:
            amount = float(value)
        except ValueError:
            raise ValidationError("amount",
                                  f"Amount '{value}' is not numeric")
        if amount <= 0:
            raise ValidationError(
                "amount",
                f"Amount {amount:.2f} must be greater than zero")
        if self.enhanced and "." in value and len(value.split(".")[1]) > 2:
            raise ValidationError(
                "amount",
                f"Amount '{value}' has more than two decimal places")
        return amount

    def _check_location(self, value):
        """Check that the location is not empty and return it."""
        if self.enhanced and value == "":
            raise ValidationError("location", "Location is empty")
        return value

    def _check_spacing(self, raw_fields):
        """Check that the record does not contain untidy whitespace.

        The file separates the fields with " | ", so a field may have at
        most one space around its value. Empty fields are skipped here,
        because the check of the field itself reports them.
        """
        for raw_field in raw_fields:
            value = raw_field.strip()
            if value == "":
                continue
            allowed = (value, f" {value}", f"{value} ", f" {value} ")
            if raw_field not in allowed:
                raise ValidationError(
                    "record",
                    f"Additional whitespace around the value '{value}'")

    def _check_duplicate_record(self, line):
        """Check that the complete record was not already read."""
        text = line.strip()
        if text in self.seen_records:
            first_line = self.seen_records[text]
            raise ValidationError(
                "record",
                f"Duplicate record, identical to line {first_line}")

# --------------------------------------------------------------------
# 5. READING THE DATA FILES
# --------------------------------------------------------------------


ACCOUNT_COLUMNS = ["account_id", "account_type", "home_location",
                   "daily_limit", "account_status"]


class DataFileError(Exception):
    """Raised when a data file is missing, empty or unreadable."""


def read_record_lines(file_path, header_start):
    """Return the usable lines of a data file as (number, text) pairs.

    Empty lines, comment lines and the header line are skipped, but the
    original line numbers of the file are kept.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as data_file:
            all_lines = data_file.readlines()
    except FileNotFoundError:
        raise DataFileError(f"The file '{file_path}' was not found.")
    except (OSError, UnicodeDecodeError) as error:
        raise DataFileError(
            f"The file '{file_path}' could not be read ({error}).")

    # Each record is returned as a (line number, text) tuple, so the
    # caller can report the line number of a rejected record.
    records = []
    for line_number, line in enumerate(all_lines, start=1):
        text = line.rstrip("\n")
        stripped = text.strip()
        if (stripped == "" or stripped.startswith("#")
                or stripped.lower().startswith(header_start)):
            continue
        records.append((line_number, text))

    if not records:
        raise DataFileError(f"The file '{file_path}' contains no records.")
    return records


class TransactionLoader:
    """Reads a transaction file and separates valid and invalid records."""

    def __init__(self, validator):
        """Store the validator that is used to check every record."""
        self.validator = validator
        self.total_records = 0
        self.invalid_records = []

    def load(self, file_path, store):
        """Read the file, validate the records and fill the store.

        Returns the number of valid transactions that were stored.
        """
        records = read_record_lines(file_path, "timestamp")
        for line_number, line in records:
            self.total_records += 1
            try:
                transaction = self.validator.validate(line, line_number)
            except ValidationError as error:
                self.invalid_records.append(
                    InvalidRecord(line_number, line.strip(),
                                  error.field_name, error.reason))
                continue
            store.add(transaction)
        return store.count()

    def invalid_count(self):
        """Return the number of rejected records."""
        return len(self.invalid_records)

    def export_invalid_records(self, file_path):
        """Write the rejected records to a CSV file."""
        header = ["line_number", "field", "reason", "record"]
        rows = []
        for record in self.invalid_records:
            rows.append([record.line_number, record.field_name,
                         record.reason, record.raw_line])
        return write_csv(file_path, header, rows)


class AccountLoader:
    """Reads the customer account file (advanced feature 5).

    The account file is a real CSV file, so it is read with
    csv.DictReader (module 8). Every row then arrives as a dictionary
    and each field can be read by its column name, for example
    row["home_location"], instead of by a column number.
    """

    def __init__(self):
        """Create a loader with an empty list of problem messages."""
        self.messages = []

    def load(self, file_path):
        """Return a dictionary of Account objects keyed by account ID."""
        try:
            with open(file_path, "r", newline="",
                      encoding="utf-8") as account_file:
                rows = list(csv.DictReader(account_file))
        except FileNotFoundError:
            raise DataFileError(f"The file '{file_path}' was not found.")
        except (OSError, UnicodeDecodeError) as error:
            raise DataFileError(
                f"The file '{file_path}' could not be read ({error}).")

        accounts = {}
        # The header is line 1, so the first data row is line 2.
        for line_number, row in enumerate(rows, start=2):
            account = self._build_account(line_number, row)
            if account is not None:
                accounts[account.account_id] = account
        if not accounts:
            raise DataFileError(f"The file '{file_path}' has no accounts.")
        return accounts

    def _build_account(self, line_number, row):
        """Turn one CSV row into an Account, or return None if unusable."""
        for column in ACCOUNT_COLUMNS:
            if not row.get(column):
                self._ignore(line_number, f"the column '{column}' is empty")
                return None
        try:
            daily_limit = float(row["daily_limit"])
        except ValueError:
            self._ignore(line_number, f"'{row['daily_limit']}' is not a "
                                      f"numeric daily limit")
            return None
        return Account(row["account_id"], row["account_type"],
                       row["home_location"], daily_limit,
                       row["account_status"])

    def _ignore(self, line_number, problem):
        """Note that one account record could not be used."""
        self.messages.append(f"Line {line_number}: account record "
                             f"ignored, {problem}.")


# --------------------------------------------------------------------
# 6. STORING TRANSACTIONS AND ALERTS
# --------------------------------------------------------------------


SEVERITY_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
RULE_LABELS = {
    "RULE_1": "Rule 1 high-value",
    "RULE_2": "Rule 2 repeated-decline",
    "RULE_3": "Rule 3 multiple-location",
    "RULE_4": "Rule 4 rapid-decline",
    "RULE_5": "Rule 5 below-threshold",
    "RULE_6": "Rule 6 daily-limit",
    "RULE_7": "Rule 7 outside-home-location",
    "RULE_8": "Rule 8 inactive-account",
    "RULE_9": "Rule 9 unknown-account",
}


class TransactionStore:
    """Stores valid transactions in a list and grouped by account ID."""

    def __init__(self):
        """Create an empty store.

        The records are kept twice: a list keeps the order of the file,
        and a dictionary groups them by account ID so that the account
        rules do not have to search the whole list again.
        """
        self.transactions = []
        self.accounts = {}

    def add(self, transaction):
        """Add one transaction to the list and to its account group."""
        self.transactions.append(transaction)
        account_id = transaction.account_id
        if account_id not in self.accounts:
            self.accounts[account_id] = []
        self.accounts[account_id].append(transaction)

    def account_ids(self):
        """Return the account IDs in alphabetical order."""
        return sorted(self.accounts.keys())

    def transactions_for(self, account_id):
        """Return the transactions of one account."""
        return self.accounts.get(account_id, [])

    def count(self):
        """Return the number of stored transactions."""
        return len(self.transactions)

    def find_by_id(self, transaction_id):
        """Return the transaction with this ID, or None if not found."""
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                return transaction
        return None

    def filter_by_status(self, status):
        """Return all transactions with one status value."""
        return [transaction for transaction in self.transactions
                if transaction.status == status]

    def sorted_by_amount(self, highest_first=True):
        """Return all transactions sorted by their amount."""
        return sorted(self.transactions,
                      key=lambda transaction: transaction.amount,
                      reverse=highest_first)

    def export_to_csv(self, file_path):
        """Write all stored transactions to a CSV file."""
        header = ["timestamp", "transaction_id", "account_id",
                  "transaction_type", "amount", "location", "status"]
        rows = [[transaction.timestamp_text(), transaction.transaction_id,
                 transaction.account_id, transaction.transaction_type,
                 f"{transaction.amount:.2f}", transaction.location,
                 transaction.status]
                for transaction in self.transactions]
        return write_csv(file_path, header, rows)


class AlertStore:
    """Stores the alerts created by the fraud-detection rules."""

    def __init__(self):
        """Create an empty alert store."""
        self.alerts = []

    def add(self, alert):
        """Add one alert to the store."""
        self.alerts.append(alert)

    def add_all(self, alerts):
        """Add a list of alerts to the store."""
        for alert in alerts:
            self.add(alert)

    def count(self):
        """Return the total number of alerts."""
        return len(self.alerts)

    def filter_by_rule(self, rule_key):
        """Return all alerts created by one detection rule."""
        return [alert for alert in self.alerts if alert.rule_key == rule_key]

    def filter_by_account(self, account_id):
        """Return all alerts that belong to one account."""
        return [alert for alert in self.alerts
                if alert.account_id == account_id]

    def suspicious_account_ids(self):
        """Return every flagged account ID once, in alphabetical order.

        A set is used so that an account which triggers several rules
        is still only counted once.
        """
        # A set removes the duplicates by itself, which is exactly
        # what sets are good for.
        return sorted({alert.account_id for alert in self.alerts})

    def suspicious_transaction_ids(self):
        """Return every flagged transaction ID once, in order."""
        found = set()
        for alert in self.alerts:
            found.update(alert.transaction_ids)
        return sorted(found)

    def sorted_by_severity(self):
        """Return the alerts with the most serious ones first."""
        return sorted(self.alerts,
                      key=lambda alert: (SEVERITY_ORDER[alert.severity],
                                         alert.account_id))

    def export_to_csv(self, file_path):
        """Write all alerts to a CSV file."""
        header = ["severity", "rule", "account_id", "transaction_ids",
                  "reason"]
        rows = [[alert.severity, alert.rule_name, alert.account_id,
                 alert.transaction_id_text(), alert.reason]
                for alert in self.sorted_by_severity()]
        return write_csv(file_path, header, rows)

# --------------------------------------------------------------------
# 7. THE FRAUD-DETECTION RULES
# --------------------------------------------------------------------


def sorted_by_time(transactions):
    """Return the transactions sorted from oldest to newest."""
    return sorted(transactions, key=lambda item: item.timestamp)


def transaction_ids(transactions):
    """Return the transaction IDs of a list of transactions."""
    return [transaction.transaction_id for transaction in transactions]


def make_alert(config, rule_key, account_id, related_ids, reason,
               details=""):
    """Create an Alert using the name and severity from the config."""
    return Alert(rule_key, config.rule_name(rule_key),
                 config.severity(rule_key), account_id, related_ids,
                 reason, details)


def amount_list(transactions):
    """Return the amounts of the transactions as readable text."""
    return ", ".join([f"${item.amount:,.2f}" for item in transactions])


def count_text(count, word):
    """Return a count together with its word in the correct form."""
    if count == 1:
        return f"{count} {word}"
    return f"{count} {word}s"


class FraudDetector:
    """Applies the fraud-detection rules to the stored transactions."""

    def __init__(self, store, config):
        """Store the transaction store and the rule configuration."""
        self.store = store
        self.config = config

    def run_all_rules(self):
        """Run every detection rule and return all alerts together."""
        alerts = []
        alerts.extend(self.detect_high_value())
        alerts.extend(self.detect_repeated_declines())
        alerts.extend(self.detect_multiple_locations())
        alerts.extend(self.detect_rapid_declines())
        alerts.extend(self.detect_structuring())
        return alerts

    def detect_high_value(self):
        """Rule 1: flag approved transactions above the amount limit."""
        limit = self.config.threshold("high_value_amount")
        alerts = []
        for transaction in self.store.transactions:
            if transaction.is_approved() and transaction.amount > limit:
                reason = (f"The approved amount of ${transaction.amount:,.2f} "
                          f"exceeded the ${limit:,.2f} threshold.")
                alerts.append(make_alert(
                    self.config, "RULE_1", transaction.account_id,
                    [transaction.transaction_id], reason,
                    transaction.summary()))
        return alerts

    def detect_repeated_declines(self):
        """Rule 2: flag accounts with too many declined transactions."""
        limit = self.config.threshold("declined_count")
        alerts = []
        for account_id in self.store.account_ids():
            declined = self._declined_transactions(account_id)
            if len(declined) >= limit:
                counted = count_text(len(declined),
                                     "declined transaction")
                reason = (f"The account had {counted}, which is at or "
                          f"above the limit of {limit}.")
                details = (f"First decline "
                           f"{declined[0].timestamp_text()}, last decline "
                           f"{declined[-1].timestamp_text()}")
                alerts.append(make_alert(
                    self.config, "RULE_2", account_id,
                    transaction_ids(declined),
                    reason, details))
        return alerts

    def detect_multiple_locations(self):
        """Rule 3: flag accounts that were used in many locations."""
        limit = self.config.threshold("location_count")
        alerts = []
        for account_id in self.store.account_ids():
            transactions = self.store.transactions_for(account_id)
            # A set would also remove the duplicates, but a set has no
            # order. The list keeps the order in which the locations
            # were used, which is more useful in the alert text.
            locations = []
            for transaction in transactions:
                if transaction.location not in locations:
                    locations.append(transaction.location)
            if len(locations) >= limit:
                counted = count_text(len(locations),
                                     "different location")
                reason = (f"The account was used in {counted}, which is "
                          f"at or above the limit of {limit}.")
                details = f"Locations: {', '.join(locations)}"
                alerts.append(make_alert(
                    self.config, "RULE_3", account_id,
                    transaction_ids(transactions),
                    reason, details))
        return alerts

    def detect_rapid_declines(self):
        """Rule 4: flag several declined transactions in a short time.

        Advanced feature 2. A single declined payment is normal, but
        several declined payments within a few minutes can mean that
        somebody is testing stolen card details.
        """
        limit = self.config.threshold("rapid_decline_count")
        minutes = self.config.threshold("rapid_decline_window_minutes")
        window = timedelta(minutes=minutes)
        alerts = []
        for account_id in self.store.account_ids():
            declined = self._declined_transactions(account_id)
            group = self._first_group_in_window(declined, window, limit)
            if group:
                counted = count_text(len(group),
                                     "declined transaction")
                reason = (f"{counted} within {minutes} minutes, between "
                          f"{group[0].timestamp_text()} and "
                          f"{group[-1].timestamp_text()}.")
                details = f"Declined amounts: {amount_list(group)}"
                alerts.append(make_alert(
                    self.config, "RULE_4", account_id, transaction_ids(group),
                    reason, details))
        return alerts

    def detect_structuring(self):
        """Rule 5: flag repeated amounts just below the high-value limit.

        Advanced feature 2. Splitting one large payment into several
        smaller ones is a common way to stay under a reporting limit.
        """
        high_value = self.config.threshold("high_value_amount")
        minimum = self.config.threshold("structuring_min_amount")
        limit = self.config.threshold("structuring_count")
        hours = self.config.threshold("structuring_window_hours")
        window = timedelta(hours=hours)
        alerts = []
        for account_id in self.store.account_ids():
            near_limit = [
                transaction
                for transaction in self.store.transactions_for(account_id)
                if transaction.is_approved()
                and minimum <= transaction.amount < high_value]
            group = self._first_group_in_window(near_limit, window, limit)
            if group:
                total = sum(item.amount for item in group)
                counted = count_text(len(group), "approved transaction")
                reason = (f"{counted} between ${minimum:,.2f} and "
                          f"${high_value:,.2f} within {hours} hours, "
                          f"${total:,.2f} in total.")
                details = f"Amounts: {amount_list(group)}"
                alerts.append(make_alert(
                    self.config, "RULE_5", account_id, transaction_ids(group),
                    reason, details))
        return alerts

    def _declined_transactions(self, account_id):
        """Return the declined transactions of an account, oldest first."""
        return sorted_by_time(
            [transaction
             for transaction in self.store.transactions_for(account_id)
             if transaction.is_declined()])

    def _first_group_in_window(self, transactions, window, limit):
        """Return the first group of transactions inside a time window.

        The transactions are sorted by time. Starting from every
        transaction, the method counts how many later transactions
        happened within the time window. The first group that reaches
        the limit is returned, otherwise an empty list.
        """
        ordered = sorted_by_time(transactions)
        for start in range(len(ordered)):
            group = [ordered[start]]
            for later in ordered[start + 1:]:
                if later.timestamp - ordered[start].timestamp <= window:
                    group.append(later)
            if len(group) >= limit:
                return group
        return []


class AccountAnalyser:
    """Compares transactions with the customer account information.

    Advanced feature 5. The account file adds information that is not
    part of a transaction record, such as the daily limit, the home
    location and whether the account is still active.
    """

    def __init__(self, store, accounts, config):
        """Store the transactions, the account data and the config."""
        self.store = store
        self.accounts = accounts
        self.config = config

    def run_all_checks(self):
        """Run every account check and return all alerts together."""
        alerts = []
        alerts.extend(self.detect_daily_limit_breach())
        alerts.extend(self.detect_outside_home_location())
        alerts.extend(self.detect_inactive_accounts())
        alerts.extend(self.detect_unknown_accounts())
        return alerts

    def detect_daily_limit_breach(self):
        """Rule 6: flag days on which an account spent above its limit."""
        alerts = []
        for account_id, account in self._known_accounts():
            daily_totals = self._approved_totals_per_day(account_id)
            for date in sorted(daily_totals.keys()):
                day = daily_totals[date]
                if day["amount"] > account.daily_limit:
                    reason = (f"Approved transactions on {date} totalled "
                              f"${day['amount']:,.2f}, which is above the "
                              f"daily limit of ${account.daily_limit:,.2f}.")
                    counted = count_text(len(day["ids"]),
                                         "approved transaction")
                    details = f"{counted} on {date}"
                    alerts.append(make_alert(
                        self.config, "RULE_6", account_id, day["ids"], reason,
                        details))
        return alerts

    def detect_outside_home_location(self):
        """Rule 7: flag transactions away from the home location."""
        alerts = []
        for account_id, account in self._known_accounts():
            away = [item
                    for item in self.store.transactions_for(account_id)
                    if item.location != account.home_location]
            if away:
                locations = sorted({item.location for item in away})
                reason = (f"The account was used "
                          f"{count_text(len(away), 'time')} outside its "
                          f"home location {account.home_location} "
                          f"({', '.join(locations)}).")
                details = f"Account type: {account.account_type}"
                alerts.append(make_alert(
                    self.config, "RULE_7", account_id,
                    transaction_ids(away), reason, details))
        return alerts

    def detect_inactive_accounts(self):
        """Rule 8: flag transactions on suspended or dormant accounts."""
        alerts = []
        for account_id, account in self._known_accounts():
            transactions = self.store.transactions_for(account_id)
            if transactions and not account.is_active():
                counted = count_text(len(transactions),
                                     "transaction")
                reason = (f"The account has the status "
                          f"{account.account_status} but was used for "
                          f"{counted}.")
                details = str(account)
                alerts.append(make_alert(
                    self.config, "RULE_8", account_id,
                    transaction_ids(transactions),
                    reason, details))
        return alerts

    def detect_unknown_accounts(self):
        """Rule 9: flag transactions of accounts that are not on file."""
        alerts = []
        for account_id in self.store.account_ids():
            if account_id in self.accounts:
                continue
            transactions = self.store.transactions_for(account_id)
            counted = count_text(len(transactions), "transaction")
            reason = (f"The account ID was not found in the customer "
                      f"account file ({counted}).")
            alerts.append(make_alert(
                self.config, "RULE_9", account_id,
                transaction_ids(transactions), reason))
        return alerts

    def _known_accounts(self):
        """Return (account_id, account) pairs that have transactions."""
        return [(account_id, self.accounts[account_id])
                for account_id in self.store.account_ids()
                if account_id in self.accounts]

    def _approved_totals_per_day(self, account_id):
        """Return the approved amount and IDs for each calendar day."""
        daily_totals = {}
        for transaction in self.store.transactions_for(account_id):
            if not transaction.is_approved():
                continue
            date = transaction.date_text()
            if date not in daily_totals:
                daily_totals[date] = {"amount": 0.0, "ids": []}
            daily_totals[date]["amount"] += transaction.amount
            daily_totals[date]["ids"].append(transaction.transaction_id)
        return daily_totals


# --------------------------------------------------------------------
# 8. SUMMARY STATISTICS (ADVANCED FEATURE 7)
# --------------------------------------------------------------------


class SummaryReport:
    """Builds the summary statistics of advanced feature 7."""

    def __init__(self, loader, store, alert_store):
        """Store the loader, the transactions and the alerts."""
        self.loader = loader
        self.store = store
        self.alert_store = alert_store

    def build(self):
        """Calculate the statistics and return them as a dictionary."""
        approved = self.store.filter_by_status("APPROVED")
        declined = self.store.filter_by_status("DECLINED")
        approved_value = sum(transaction.amount for transaction in approved)
        statistics = {
            "Total records processed": self.loader.total_records,
            "Valid records": self.store.count(),
            "Invalid records": self.loader.invalid_count(),
            "Approved transactions": len(approved),
            "Declined transactions": len(declined),
            "Total value of approved transactions":
                f"${approved_value:,.2f}",
            "Suspicious transactions":
                len(self.alert_store.suspicious_transaction_ids()),
            "Suspicious accounts":
                len(self.alert_store.suspicious_account_ids()),
        }
        for rule_key in RULE_LABELS:
            label = f"{RULE_LABELS[rule_key]} alerts"
            statistics[label] = len(
                self.alert_store.filter_by_rule(rule_key))
        return statistics

    def export_to_csv(self, file_path):
        """Write the summary statistics to a CSV file."""
        statistics = self.build()
        rows = [[label, statistics[label]] for label in statistics]
        return write_csv(file_path, ["statistic", "value"], rows)
```

## `test.py`

*Test program*

```python
"""
Program: test.py
Author: Adam Heier
Last date modified: 16/09/2026

The purpose of this program is to test the bank transaction fraud
detection system automatically (ICT703 Assessment Task 2). It asks for
no user input:
    python test.py

Every test prints the feature that is tested, the test input, the
expected result, the actual result and whether the test passed.

The tests are black-box tests (module 8): they only use the input and
the output of a function, not its internal steps. Each group uses
positive and negative cases, and the rule tests add boundary value
analysis on the exact threshold of every rule.

All test records are built with the helper function record(). It has a
valid default value for every field, so a test only has to name the one
field it wants to change. This keeps each test case to a single line.
"""

import os

from fraud_detection import (AccountAnalyser, AccountLoader, AlertStore,
                             DataFileError, FraudDetector, RuleConfig,
                             SummaryReport, TransactionLoader,
                             TransactionStore, TransactionValidator,
                             ValidationError, use_program_folder)

TRANSACTION_FILE = "transactions.txt"
ACCOUNT_FILE = "accounts.csv"
CONFIG_FILE = "rules_config.json"
MISSING_FILE = "this_file_does_not_exist.txt"
TEMP_EMPTY_FILE = "output/temp_empty.txt"
TEMP_BROKEN_FILE = "output/temp_broken.txt"
TEMP_CONFIG_FILE = "output/temp_config.json"
TEMP_EXPORT_FILE = "output/temp_invalid_records.csv"
TEMP_SUMMARY_FILE = "output/temp_summary.csv"


def record(tid="T3001", account="A10025", kind="TRANSFER", amount="850.00",
           place="Brisbane", status="APPROVED",
           time="2026-07-11 09:15:23"):
    """Build one transaction record line.

    Every field has a valid default value, so a test only has to name
    the field it wants to change, for example record(amount="abc").
    """
    return (f"{time} | {tid} | {account} | {kind} | {amount} | "
            f"{place} | {status}")


NORMAL_RECORD = record()
SAMPLE_RECORDS = [
    record(tid="T2001"),
    record(tid="T2002", amount="6500.00"),
    record(tid="T2003", kind="ONLINE_PURCHASE", amount="120.00",
           status="DECLINED"),
    record(tid="T2004", account="A20318", kind="CASH_WITHDRAWAL",
           amount="500.00", place="Gold Coast"),
    record(tid="T2005", account="A20318", kind="CARD_PAYMENT",
           amount="45.50", place="Gold Coast"),
]


class TestRunner:
    """Runs test cases and prints the result of every test."""

    def __init__(self):
        """Create a runner with empty counters."""
        self.number = 0
        self.passed = 0
        self.failed = 0

    def check(self, feature, test_input, expected, actual):
        """Compare the expected and the actual result and print it."""
        self.number += 1
        if expected == actual:
            outcome = "PASS"
            self.passed += 1
        else:
            outcome = "FAIL"
            self.failed += 1
        print(f"Test {self.number:>2}: {outcome}")
        print(f"  Feature  : {feature}")
        print(f"  Input    : {test_input}")
        print(f"  Expected : {expected}")
        print(f"  Actual   : {actual}")
        print()

    def print_summary(self):
        """Print how many tests passed and how many failed."""
        print("=" * 74)
        print(f"TEST SUMMARY: {self.number} tests, {self.passed} passed, "
              f"{self.failed} failed")
        print("=" * 74)


def print_section(title):
    """Print the heading of a group of tests."""
    print()
    print("=" * 74)
    print(title)
    print("=" * 74)
    print()


def write_temp_file(file_path, text):
    """Create a small file that is only needed during the tests."""
    folder = os.path.dirname(file_path)
    if folder != "" and not os.path.isdir(folder):
        os.makedirs(folder)
    with open(file_path, "w", encoding="utf-8") as temp_file:
        temp_file.write(text)


def write_temp_bytes(file_path, data):
    """Create a file that does not contain valid UTF-8 text."""
    folder = os.path.dirname(file_path)
    if folder != "" and not os.path.isdir(folder):
        os.makedirs(folder)
    with open(file_path, "wb") as temp_file:
        temp_file.write(data)


def delete_temp_files():
    """Delete the files that were created by the tests."""
    for file_path in [TEMP_EMPTY_FILE, TEMP_BROKEN_FILE, TEMP_CONFIG_FILE,
                      TEMP_EXPORT_FILE, TEMP_SUMMARY_FILE]:
        if os.path.exists(file_path):
            os.remove(file_path)


def build_store(lines, enhanced=False):
    """Create a transaction store from a list of record lines."""
    validator = TransactionValidator(enhanced)
    store = TransactionStore()
    for line_number, line in enumerate(lines, start=1):
        store.add(validator.validate(line, line_number))
    return store


def validate_record(line, enhanced=False):
    """Return 'accepted' or 'rejected (field)' for one record."""
    validator = TransactionValidator(enhanced)
    try:
        validator.validate(line, 1)
    except ValidationError as error:
        return f"rejected ({error.field_name})"
    return "accepted"


def load_config():
    """Return the configuration used by most of the rule tests."""
    return RuleConfig(CONFIG_FILE)


def load_main_file():
    """Read the main transaction file and return two objects.

    The loader and the store are returned together as a tuple, so the
    caller can unpack them in one line:
        loader, store = load_main_file()
    """
    store = TransactionStore()
    loader = TransactionLoader(TransactionValidator(True))
    loader.load(TRANSACTION_FILE, store)
    return loader, store


def expect_data_file_error(file_path):
    """Return the name of the error that reading this file raises."""
    try:
        TransactionLoader(TransactionValidator()).load(
            file_path, TransactionStore())
    except DataFileError:
        return "DataFileError"
    return "no error"


def first_error_reason(validator, line):
    """Return the reason why the validator rejected this record."""
    try:
        validator.validate(line, 2)
    except ValidationError as error:
        return error.reason
    return "accepted"


def test_file_handling(runner):
    """Test reading valid, missing and empty transaction files."""
    print_section("1. FILE HANDLING - error handling")

    # Unit testing of the error handling: the three ways a data file
    # can fail are a missing file, an empty file and a file that is not
    # valid text.
    loader, store = load_main_file()
    runner.check("TransactionLoader.load - valid file", TRANSACTION_FILE,
                 "46 read, 28 valid",
                 f"{loader.total_records} read, {store.count()} valid")
    runner.check("TransactionLoader.load - missing file", MISSING_FILE,
                 "DataFileError", expect_data_file_error(MISSING_FILE))

    write_temp_file(TEMP_EMPTY_FILE, "")
    runner.check("TransactionLoader.load - empty file", TEMP_EMPTY_FILE,
                 "DataFileError", expect_data_file_error(TEMP_EMPTY_FILE))

    # A file with bytes that are not valid UTF-8 cannot be read as text.
    write_temp_bytes(TEMP_BROKEN_FILE, b"\xff\xfe not readable text")
    runner.check("TransactionLoader.load - unreadable file",
                 TEMP_BROKEN_FILE, "DataFileError",
                 expect_data_file_error(TEMP_BROKEN_FILE))


def test_core_validation(runner):
    """Test the basic validation checks of section 4.2."""
    print_section("2. CORE DATA VALIDATION - equivalence partitioning")

    # Equivalence partitioning: every rejection reason is one class of
    # invalid input, so one record per class is enough. Each record
    # differs from a valid record in exactly one field.
    # Removing the last field leaves a record with only six fields.
    short_record = record().rsplit(" | ", 1)[0]
    cases = [
        ("valid record", record(), "accepted"),
        ("incorrect number of fields", short_record, "rejected (record)"),
        ("invalid transaction type", record(kind="BITCOIN_SWAP"),
         "rejected (transaction_type)"),
        ("invalid status value", record(status="REJECTED"),
         "rejected (status)"),
        ("non-numeric amount", record(amount="abc"), "rejected (amount)"),
        ("zero amount", record(amount="0.00"), "rejected (amount)"),
        ("negative amount", record(amount="-50.00"), "rejected (amount)"),
        ("empty transaction ID", record(tid=""),
         "rejected (transaction_id)"),
        ("empty account ID", record(account=""), "rejected (account_id)"),
    ]
    for description, line, expected in cases:
        runner.check(f"TransactionValidator.validate - {description}",
                     line, expected, validate_record(line))


def test_core_rules(runner):
    """Test the three core fraud-detection rules."""
    print_section("3. CORE FRAUD-DETECTION RULES - boundary values")
    config = load_config()

    high_value = [record(tid="T4001"), record(tid="T4002", amount="6500.00")]
    alerts = FraudDetector(build_store(high_value),
                           config).detect_high_value()
    runner.check("Rule 1 - approved transaction above $5,000",
                 "T4002 approved, $6,500.00", "1 alert for T4002",
                 f"{len(alerts)} alert for {alerts[0].transaction_id_text()}")

    # Boundary value analysis: the rule uses ">", so an amount of
    # exactly $5,000.00 must still be allowed.
    boundary = [record(tid="T4003", amount="5000.00")]
    runner.check("Rule 1 - boundary value of exactly $5,000",
                 "T4003 approved, $5,000.00", 0,
                 len(FraudDetector(build_store(boundary),
                                   config).detect_high_value()))

    declines = [record(tid=f"T41{number}0", account="A20318",
                       kind="ONLINE_PURCHASE", amount="100.00",
                       place="Gold Coast", status="DECLINED",
                       time=f"2026-07-11 1{number}:00:00")
                for number in range(4)]
    runner.check("Rule 2 - four declined transactions on one account",
                 "4 declined transactions for A20318", 1,
                 len(FraudDetector(build_store(declines),
                                   config).detect_repeated_declines()))
    # Boundary value analysis on the other side of the limit: three
    # declined transactions are one below the threshold of four.
    runner.check("Rule 2 - boundary value of three declined transactions",
                 "3 declined transactions for A20318", 0,
                 len(FraudDetector(build_store(declines[:3]),
                                   config).detect_repeated_declines()))

    locations = [record(tid="T4201", account="A30712", place="Sydney"),
                 record(tid="T4202", account="A30712", place="Melbourne"),
                 record(tid="T4203", account="A30712", place="Perth")]
    runner.check("Rule 3 - transactions in three different locations",
                 "Sydney, Melbourne, Perth", 1,
                 len(FraudDetector(build_store(locations),
                                   config).detect_multiple_locations()))
    runner.check("Rule 3 - boundary value of two different locations",
                 "Sydney, Melbourne", 0,
                 len(FraudDetector(build_store(locations[:2]),
                                   config).detect_multiple_locations()))

    # Negative test case: an ordinary account must produce no alert at
    # all, otherwise the bank would investigate innocent customers.
    normal = [record(tid="T4301", account="A40199", kind="DIRECT_DEBIT",
                     amount="120.00", place="Hobart"),
              record(tid="T4302", account="A40199", kind="CARD_PAYMENT",
                     amount="62.30", place="Hobart"),
              record(tid="T4303", account="A40199", kind="CARD_PAYMENT",
                     amount="25.00", place="Hobart", status="DECLINED")]
    runner.check("All rules - normal account must not be flagged",
                 "A40199 with 3 small transactions in one location", 0,
                 len(FraudDetector(build_store(normal),
                                   config).run_all_rules()))


def test_enhanced_validation(runner):
    """Test advanced feature 1 - enhanced data validation."""
    print_section("4. ADVANCED FEATURE 1 - ENHANCED DATA VALIDATION")

    wrong_id = record(tid="TX999")
    runner.check("Enhanced validation - transaction ID format (core mode)",
                 wrong_id, "accepted", validate_record(wrong_id, False))
    runner.check("Enhanced validation - transaction ID format",
                 wrong_id, "rejected (transaction_id)",
                 validate_record(wrong_id, True))

    cases = [
        ("account ID format", record(tid="T5001", account="A8051"),
         "rejected (account_id)"),
        ("timestamp format",
         record(tid="T5002", time="11/07/2026 09:15:23"),
         "rejected (timestamp)"),
        ("inconsistent capitalisation",
         record(tid="T5003", kind="transfer"),
         "rejected (transaction_type)"),
        ("additional whitespace",
         record(tid="T5004", account="A10025 "), "rejected (record)"),
    ]
    for description, line, expected in cases:
        runner.check(f"Enhanced validation - {description}", line, expected,
                     validate_record(line, True))

    validator = TransactionValidator(enhanced=True)
    validator.validate(NORMAL_RECORD, 1)
    runner.check("Enhanced validation - duplicate transaction ID",
                 "T3001 used twice",
                 "Duplicate transaction ID 'T3001', already used on line 1",
                 first_error_reason(validator,
                                    record(amount="99.00",
                                           time="2026-07-11 10:00:00")))

    # The data file contains one record for each rejection reason, so
    # this test covers every format check and every extra check at once.
    loader = load_main_file()[0]
    loader.export_invalid_records(TEMP_EXPORT_FILE)
    with open(TEMP_EXPORT_FILE, "r", encoding="utf-8") as export_file:
        exported_rows = len(export_file.readlines()) - 1
    runner.check("Enhanced validation - all checks on the data file",
                 TRANSACTION_FILE, "18 rejected, 18 exported",
                 f"{loader.invalid_count()} rejected, "
                 f"{exported_rows} exported")


def test_time_based_rules(runner):
    """Test advanced feature 2 - time-based fraud detection."""
    print_section("5. ADVANCED FEATURE 2 - TIME-BASED DETECTION")
    config = load_config()

    def decline(tid, time):
        """Build one declined online purchase for account A20318."""
        return record(tid=tid, account="A20318", kind="ONLINE_PURCHASE",
                      amount="199.99", place="Gold Coast",
                      status="DECLINED", time=f"2026-07-11 {time}")

    # The same four declined transactions are used twice: once inside
    # the time window (positive case) and once spread over six hours
    # (negative case). Only the timestamps differ.
    fast = [decline("T6001", "11:02:11"), decline("T6002", "11:09:47"),
            decline("T6003", "11:15:30"), decline("T6004", "11:24:58")]
    runner.check("Rule 4 - four declined transactions within 30 minutes",
                 "4 declined transactions between 11:02 and 11:24", 1,
                 len(FraudDetector(build_store(fast),
                                   config).detect_rapid_declines()))

    slow = [decline("T6001", "09:00:00"), decline("T6002", "11:00:00"),
            decline("T6003", "13:00:00"), decline("T6004", "15:00:00")]
    runner.check("Rule 4 - four declined transactions over six hours",
                 "4 declined transactions between 09:00 and 15:00", 0,
                 len(FraudDetector(build_store(slow),
                                   config).detect_rapid_declines()))

    structuring = [
        record(tid="T6101", account="A50876", amount="4900.00",
               place="Adelaide", time="2026-07-12 10:12:33"),
        record(tid="T6102", account="A50876", amount="4850.00",
               place="Adelaide", time="2026-07-12 10:48:07"),
        record(tid="T6103", account="A50876", amount="4750.00",
               place="Adelaide", time="2026-07-12 11:26:51"),
    ]
    runner.check("Rule 5 - three approved amounts just below $5,000",
                 "$4,900.00, $4,850.00, $4,750.00 within one hour", 1,
                 len(FraudDetector(build_store(structuring),
                                   config).detect_structuring()))
    runner.check("Rule 5 - only two amounts just below $5,000",
                 "$4,900.00, $4,850.00", 0,
                 len(FraudDetector(build_store(structuring[:2]),
                                   config).detect_structuring()))


def test_storage(runner):
    """Test advanced feature 3 - storage, search, filter and sort."""
    print_section("6. ADVANCED FEATURE 3 - STORAGE AND MANAGEMENT")
    config = load_config()
    store = build_store(SAMPLE_RECORDS, enhanced=True)

    runner.check("TransactionStore.find_by_id", "T2002", 6500.00,
                 store.find_by_id("T2002").amount)
    runner.check("TransactionStore.sorted_by_amount", "highest first",
                 "T2002", store.sorted_by_amount()[0].transaction_id)

    alert_store = AlertStore()
    alert_store.add_all(FraudDetector(store, config).run_all_rules())
    runner.check("AlertStore.suspicious_account_ids - counted once",
                 "5 sample records", ["A10025"],
                 alert_store.suspicious_account_ids())


def test_configuration(runner):
    """Test advanced feature 4 - configurable fraud rules."""
    print_section("7. ADVANCED FEATURE 4 - CONFIGURABLE FRAUD RULES")

    config = RuleConfig(CONFIG_FILE)
    runner.check("RuleConfig - missing file uses the default settings",
                 "no_such_config.json", "built-in default settings",
                 RuleConfig("no_such_config.json").source)

    # This file only contains one threshold. If the program still works
    # with it, the other settings were correctly taken from the defaults.
    write_temp_file(TEMP_CONFIG_FILE,
                    '{"thresholds": {"high_value_amount": 1000.00}}')
    changed = RuleConfig(TEMP_CONFIG_FILE)

    store = build_store([record(tid="T7001", amount="2500.00")])
    runner.check("Rule 1 - $2,500.00 with the standard threshold",
                 "threshold $5,000.00", 0,
                 len(FraudDetector(store, config).detect_high_value()))
    runner.check("Rule 1 - $2,500.00 with the lowered threshold",
                 "threshold $1,000.00", 1,
                 len(FraudDetector(store, changed).detect_high_value()))


def test_account_analysis(runner):
    """Test advanced feature 5 - customer account analysis."""
    print_section("8. ADVANCED FEATURE 5 - CUSTOMER ACCOUNT ANALYSIS")
    config = load_config()
    accounts = AccountLoader().load(ACCOUNT_FILE)

    over_limit = [record(tid="T8001", account="A40199", amount="1500.00",
                         place="Hobart", time="2026-07-12 10:00:00"),
                  record(tid="T8002", account="A40199", amount="900.00",
                         place="Hobart", time="2026-07-12 11:00:00")]
    analyser = AccountAnalyser(build_store(over_limit), accounts, config)
    runner.check("Rule 6 - approved total above the daily limit",
                 "A40199 spent $2,400.00, limit $2,000.00", 1,
                 len(analyser.detect_daily_limit_breach()))

    away = [record(tid="T8003", account="A40199", amount="100.00",
                   place="Perth")]
    analyser = AccountAnalyser(build_store(away), accounts, config)
    runner.check("Rule 7 - transaction outside the home location",
                 "A40199 used in Perth, home location Hobart", 1,
                 len(analyser.detect_outside_home_location()))

    suspended = [record(tid="T8004", account="A60234",
                        kind="CASH_WITHDRAWAL", amount="1200.00",
                        place="Cairns")]
    analyser = AccountAnalyser(build_store(suspended), accounts, config)
    runner.check("Rule 8 - transaction on a suspended account",
                 "A60234 has the status SUSPENDED", 1,
                 len(analyser.detect_inactive_accounts()))

    unknown = [record(tid="T8005", account="A99999", amount="100.00")]
    analyser = AccountAnalyser(build_store(unknown), accounts, config)
    runner.check("Rule 9 - account is not in the customer account file",
                 "A99999", 1, len(analyser.detect_unknown_accounts()))


def test_summary_report(runner):
    """Test advanced feature 7 - summary statistics and reporting."""
    print_section("9. ADVANCED FEATURE 7 - SUMMARY STATISTICS")
    config = load_config()

    loader, store = load_main_file()
    accounts = AccountLoader().load(ACCOUNT_FILE)
    alert_store = AlertStore()
    alert_store.add_all(FraudDetector(store, config).run_all_rules())
    alert_store.add_all(
        AccountAnalyser(store, accounts, config).run_all_checks())
    summary = SummaryReport(loader, store, alert_store)
    statistics = summary.build()

    expected_values = [
        ("total value of approved transactions",
         "Total value of approved transactions", "$34,322.65"),
        ("suspicious accounts counted once", "Suspicious accounts", 7),
    ]
    for description, key, expected in expected_values:
        runner.check(f"SummaryReport - {description}", TRANSACTION_FILE,
                     expected, statistics[key])

    summary.export_to_csv(TEMP_SUMMARY_FILE)
    runner.check("SummaryReport.export_to_csv", TEMP_SUMMARY_FILE, True,
                 os.path.exists(TEMP_SUMMARY_FILE))


def main():
    """Run all groups of tests and print the overall result."""
    use_program_folder()
    print("=" * 74)
    print("TEST PROGRAM - BANK TRANSACTION FRAUD DETECTION SYSTEM")
    print("=" * 74)
    runner = TestRunner()
    test_file_handling(runner)
    test_core_validation(runner)
    test_core_rules(runner)
    test_enhanced_validation(runner)
    test_time_based_rules(runner)
    test_storage(runner)
    test_configuration(runner)
    test_account_analysis(runner)
    test_summary_report(runner)
    delete_temp_files()
    runner.print_summary()


if __name__ == "__main__":
    main()
```

## `transactions.txt`

*Transaction data*

```text
# Fictional transaction data for ICT703 Task 2 (Adam Heier)
# Format: timestamp | transaction_id | account_id | transaction_type | amount | location | status
# Valid and invalid records are mixed, as they would be in a real export.
timestamp | transaction_id | account_id | transaction_type | amount | location | status
2026-07-11 07:30:00 | T1015 | A40199 | DIRECT_DEBIT | 120.00 | Hobart | APPROVED
2026-07-11 07:52:14 | T1028 | A80512 | BITCOIN_SWAP | 300.00 | Brisbane | APPROVED
2026-07-11 08:45:00 | T1011 | A30712 | CARD_PAYMENT | 89.90 | Sydney | APPROVED
2026-07-11 09:15:23 | T1001 | A10025 | TRANSFER | 850.00 | Brisbane | APPROVED
2026-07-11 09:18:40 | T1002 | A10025 | TRANSFER | 6500.00 | Brisbane | APPROVED
2026-07-11 09:20:12 | T1003 | A10025 | ONLINE_PURCHASE | 120.00 | Sydney | DECLINED
2026-07-11 09:22:05 | T1004 | A20318 | CASH_WITHDRAWAL | 500.00 | Gold Coast | APPROVED
2026-07-11 09:41:36 | T1029 | A80512 | TRANSFER | abc | Brisbane | APPROVED
2026-07-11 10:05:00 | T1005 | A10025 | CARD_PAYMENT | 45.50 | Brisbane | APPROVED
2026-07-11 10:33:07 | T1030 | A80512 | TRANSFER | -50.00 | Brisbane | APPROVED
2026-07-11 11:02:11 | T1006 | A20318 | ONLINE_PURCHASE | 199.99 | Gold Coast | DECLINED
2026-07-11 11:09:47 | T1007 | A20318 | ONLINE_PURCHASE | 249.99 | Gold Coast | DECLINED
2026-07-11 11:15:30 | T1008 | A20318 | ONLINE_PURCHASE | 310.00 | Gold Coast | DECLINED
2026-07-11 11:24:58 | T1009 | A20318 | ONLINE_PURCHASE | 275.50 | Gold Coast | DECLINED
2026-07-11 11:31:12 | T1010 | A20318 | ONLINE_PURCHASE | 180.00 | Gold Coast | APPROVED
2026-07-11 11:58:22 | T1031 | A80512 | CARD_PAYMENT | 0.00 | Brisbane | APPROVED
2026-07-11 12:30:15 | T1012 | A30712 | CARD_PAYMENT | 145.00 | Melbourne | APPROVED
2026-07-11 13:45:20 | T1016 | A40199 | CARD_PAYMENT | 62.30 | Hobart | APPROVED
2026-07-11 14:19:05 | T1032 | A80512 | TRANSFER | 100.00 | Brisbane | REJECTED
2026-07-11 16:10:42 | T1013 | A30712 | CASH_WITHDRAWAL | 400.00 | Perth | APPROVED
2026-07-11 17:02:48 | T1033 | A80512 | TRANSFER | 100.00 | Brisbane
2026-07-11 18:55:03 | T1014 | A30712 | ONLINE_PURCHASE | 59.95 | Sydney | APPROVED
2026-07-11 19:26:31 |  | A80512 | TRANSFER | 100.00 | Brisbane | APPROVED
2026-07-12 08:14:52 | T1035 |  | TRANSFER | 100.00 | Brisbane | APPROVED
2026-07-12 09:05:10 | T1017 | A40199 | TRANSFER | 300.00 | Hobart | APPROVED
2026-07-12 10:12:33 | T1019 | A50876 | TRANSFER | 4900.00 | Adelaide | APPROVED
12/07/2026 10:31:19 | T1036 | A80512 | TRANSFER | 100.00 | Brisbane | APPROVED
2026-07-12 10:48:07 | T1020 | A50876 | TRANSFER | 4850.00 | Adelaide | APPROVED
2026-07-12 11:26:51 | T1021 | A50876 | TRANSFER | 4750.00 | Adelaide | APPROVED
2026-07-12 12:03:44 | TX999 | A80512 | TRANSFER | 100.00 | Brisbane | APPROVED
2026-07-12 13:17:20 | T1038 | A8051 | TRANSFER | 100.00 | Brisbane | APPROVED
2026-07-12 14:03:19 | T1022 | A60234 | CASH_WITHDRAWAL | 1200.00 | Cairns | APPROVED
2026-07-12 14:35:44 | T1023 | A60234 | CASH_WITHDRAWAL | 900.00 | Cairns | APPROVED
2026-07-12 15:48:09 | T1039 | A80512 | TRANSFER | 100.123 | Brisbane | APPROVED
2026-07-12 16:21:55 | T1040 | A80512 | TRANSFER | 100.00 |  | APPROVED
2026-07-12 17:22:48 | T1018 | A40199 | CARD_PAYMENT | 25.00 | Hobart | DECLINED
2026-07-12 18:40:12 | T1001 | A10025 | TRANSFER | 75.00 | Brisbane | APPROVED
2026-07-13 07:35:26 | T1042 | A10025 | transfer | 60.00 | Brisbane | approved
2026-07-13 08:10:05 | T1024 | A70455 | TRANSFER | 7500.00 | Darwin | APPROVED
2026-07-13 09:45:30 | T1025 | A70455 | CARD_PAYMENT | 220.00 | Alice Springs | APPROVED
2026-07-13 10:00:00 | T1045 | A90123 | CARD_PAYMENT | 150.00 | Brisbane | APPROVED
2026-07-13 11:12:38 | T1043 | A10025 | TRANSFER | 60.00 | Brisbane | APPROVED | EXTRA
2026-07-13 13:05:15 | T1026 | A70455 | ONLINE_PURCHASE | 85.00 | Darwin | DECLINED
2026-07-13 14:27:03 | T1044 | A10025  | TRANSFER | 60.00 | Brisbane | APPROVED
2026-07-13 15:40:00 | T1027 | A70455 | CASH_WITHDRAWAL | 600.00 | Katherine | APPROVED
2026-07-11 07:30:00 | T1015 | A40199 | DIRECT_DEBIT | 120.00 | Hobart | APPROVED
```

## `accounts.csv`

*Customer account data*

```text
account_id,account_type,home_location,daily_limit,account_status
A10025,EVERYDAY,Brisbane,10000.00,ACTIVE
A20318,SAVINGS,Gold Coast,5000.00,ACTIVE
A30712,EVERYDAY,Sydney,5000.00,ACTIVE
A40199,SAVINGS,Hobart,2000.00,ACTIVE
A50876,BUSINESS,Adelaide,10000.00,ACTIVE
A60234,EVERYDAY,Cairns,3000.00,SUSPENDED
A70455,BUSINESS,Darwin,15000.00,ACTIVE
A80512,EVERYDAY,Brisbane,4000.00,ACTIVE
A11500,SAVINGS,Newcastle,2000.00,DORMANT
```

## `rules_config.json`

*Rule configuration*

```json
{
    "thresholds": {
        "high_value_amount": 5000.0,
        "declined_count": 4,
        "location_count": 3,
        "rapid_decline_count": 4,
        "rapid_decline_window_minutes": 30,
        "structuring_min_amount": 4500.0,
        "structuring_count": 3,
        "structuring_window_hours": 24
    },
    "rule_names": {
        "RULE_1": "Rule 1 - High-Value Transaction",
        "RULE_2": "Rule 2 - Repeated Declined Transactions",
        "RULE_3": "Rule 3 - Multiple Locations",
        "RULE_4": "Rule 4 - Rapid Declined Transactions",
        "RULE_5": "Rule 5 - Amounts Just Below Threshold",
        "RULE_6": "Rule 6 - Daily Limit Exceeded",
        "RULE_7": "Rule 7 - Transaction Outside Home Location",
        "RULE_8": "Rule 8 - Activity On Inactive Account",
        "RULE_9": "Rule 9 - Unknown Account"
    },
    "severities": {
        "RULE_1": "HIGH",
        "RULE_2": "MEDIUM",
        "RULE_3": "MEDIUM",
        "RULE_4": "HIGH",
        "RULE_5": "HIGH",
        "RULE_6": "HIGH",
        "RULE_7": "MEDIUM",
        "RULE_8": "HIGH",
        "RULE_9": "LOW"
    },
    "options": {
        "enhanced_validation": true
    }
}
```
