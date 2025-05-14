from faker import Faker
import random
import pandas as pd

# CONFIG
CSV_PATH = "./data/synthetic_data.csv"

fake = Faker()

def generate_invoice():
    items = "\n".join([f"- {fake.word()}: ${random.randint(10, 500)}" for _ in range(3)])
    return f"""
    Invoice #: {fake.random_int(1000, 9999)}
    Date: {fake.date_this_year()}
    Billed To: {fake.name()}
    Address: {fake.address()}
    {items}
    Total: ${random.randint(100, 1000)}
    """

def generate_bank_statement():
    transactions = "\n".join([f"{fake.date_this_year()} - {fake.company()} - ${random.randint(10, 300)}"
                              for _ in range(5)])
    return f"""
    Bank Statement
    Name: {fake.name()}
    Account #: {fake.iban()}
    {transactions}
    Closing Balance: ${random.randint(1000, 5000)}
    """

def generate_drivers_license():
    return f"""
    Driver's License
    Name: {fake.name()}
    Address: {fake.address()}
    DOB: {fake.date_of_birth(minimum_age=18, maximum_age=90)}
    License #: {fake.bothify('??######')}
    Expiry: {fake.date_between(start_date="+1y", end_date="+10y")}
    """

def generate_health_insurance_card():
    return f"""
    Health Insurance Card
    Name: {fake.name()}
    Policy Number: {fake.bothify('??#########')}
    Member ID: {fake.uuid4()}
    Group #: {fake.random_int(1000, 9999)}
    Plan Type: {fake.random_element(elements=('HMO', 'PPO', 'EPO', 'POS'))}
    Coverage Start Date: {fake.date_this_year()}
    Coverage End Date: {fake.date_between(start_date="+1y", end_date="+5y")}
    Issuer: {fake.company()}
    """

# Generate samples
samples = []
labels = []
for _ in range(500):
    samples.append(generate_invoice())
    labels.append("invoice")

    samples.append(generate_bank_statement())
    labels.append("bank_statement")

    samples.append(generate_drivers_license())
    labels.append("drivers_license")

    samples.append(generate_health_insurance_card())
    labels.append("health_insurance_card")

# Save as CSV
df = pd.DataFrame({'text': samples, 'label': labels})
df.to_csv(CSV_PATH, index=False)
