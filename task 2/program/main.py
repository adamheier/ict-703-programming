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
