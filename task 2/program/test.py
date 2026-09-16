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
