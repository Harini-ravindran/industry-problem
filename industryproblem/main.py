import csv
import json
import os
import importlib

# Attempt to import load_tariffs from tariff_loader; if unavailable, provide a
# simple fallback that loads the JSON file directly.
try:
    tariff_loader = importlib.import_module("tariff_loader")
    load_tariffs = tariff_loader.load_tariffs
except (ImportError, ModuleNotFoundError):
    def load_tariffs(path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Tariff config not found: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
from consumers import *
from exceptions import *

tariffs = load_tariffs("tariff_config.json")

summary = {
    "Residential": 0,
    "Commercial": 0,
    "Industrial": 0
}

report = []

with open("customers.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        try:

            customer_id = row["customer_id"]
            category = row["type"]
            consumption = float(row["consumption"])

            if consumption < 0:
                raise NegativeConsumptionError(
                    "Negative Consumption"
                )

            if category == "Residential":
                obj = ResidentialConsumer(
                    customer_id,
                    consumption,
                    tariffs["Residential"]
                )

            elif category == "Commercial":
                obj = CommercialConsumer(
                    customer_id,
                    consumption,
                    tariffs["Commercial"]
                )

            elif category == "Industrial":
                obj = IndustrialConsumer(
                    customer_id,
                    consumption,
                    tariffs["Industrial"]
                )

            else:
                raise InvalidCategoryError(
                    "Invalid Category"
                )

            bill = obj.compute_bill()

            late_fee = 0

            if row["payment_due"] == "Yes":
                late_fee = bill * 0.05

            total = bill + late_fee

            summary[category] += total

            report.append(
                [customer_id,
                 category,
                 consumption,
                 bill,
                 late_fee,
                 total]
            )

        except Exception as e:
            print("Error:", e)

with open("bills_report.txt", "w", encoding="utf-8") as file:

    file.write("WATER BILL REPORT\n")
    file.write("=" * 60 + "\n")

    for r in report:

        file.write(
            f"ID:{r[0]} "
            f"Type:{r[1]} "
            f"Consumption:{r[2]} "
            f"Bill:{r[3]:.2f} "
            f"LateFee:{r[4]:.2f} "
            f"Total:{r[5]:.2f}\n"
        )

with open("summary_report.txt", "w", encoding="utf-8") as file:

    file.write("SUMMARY REPORT\n")
    file.write("=" * 40 + "\n")

    for cat, amount in summary.items():
        file.write(
            f"{cat}: ₹{amount:.2f}\n"
        )

print("Reports Generated Successfully")