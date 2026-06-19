import csv
from datetime import datetime

from consumers import *
from loader import load_tariff
from exceptions import *

tariff = load_tariff("tariff_config.json")

report = open("bill_report.txt","w")

with open("customers.csv") as file:
    reader = csv.DictReader(file)

    for row in reader:

        cid = row['id']
        category = row['type']
        units = int(row['consumption'])

        if units < 0:
            raise NegativeConsumptionError()

        if category not in tariff:
            raise InvalidCategoryError()

        if category == "Residential":
            obj = ResidentialConsumer(cid, units)

        elif category == "Commercial":
            obj = CommercialConsumer(cid, units)

        else:
            obj = IndustrialConsumer(cid, units)

        bill = obj.compute_bill(tariff[category])

        due = datetime.strptime(row['due_date'],"%Y-%m-%d")

        late_fee = 0

        if due < datetime.today():
            late_fee = bill * 0.05

        total = bill + late_fee

        report.write(
            f"{cid} {category} {units} "
            f"{bill:.2f} {late_fee:.2f} {total:.2f}\n"
        )

report.close()