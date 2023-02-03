"""Create n random samples to generate sql insert queries."""

from random import randint, random, choice, choices
from datetime import date, timedelta
import json
import string


def random_date(start_date, end_date, threshold=1):
    """Generate random date between start_date and end_date, with threshold probability."""
    if random() < threshold:
        dt = start_date + (end_date - start_date) * random()
    else:
        dt = date(4000, 1, 1)
    return dt


def random_model(groups):
    """Generate random model, make and group."""
    group_name = choice(list(groups.keys()))
    group = groups.get(group_name)
    group_id = group.get("groupId")
    makes = group.get("makes")
    make_name = choice(list(makes.keys()))
    make = makes.get(make_name)
    make_id = make.get("makeId")
    models = make.get("models")
    model_name = choice(list(models.keys())) #.title()
    model_id = models.get(model_name)

    return (group_name, group_id, make_name, make_id, model_name, model_id)


def main():
    with open(r".\data\groups_makes_models.json", "r") as f:
        groups_makes_models = json.load(f)

    with open(r".\data\insurance_companies.json", "r") as f:
        insurance_companies = json.load(f)

    with open(r".\data\colors.json", "r") as f:
        colors = json.load(f)

    n = 200
    insert_vehicles = []
    insert_models = set()
    insert_makes = set()
    insert_groups = set()
    insert_insurance_companies = set()

    # Generate n random vehicles registries
    for i in range(n):
        group_name, group_id, make_name, make_id, model_name, model_id = random_model(groups_makes_models)
        today = date.today()
        purchase_date = random_date(date(2010, 1, 1), today)
        deregistration_date = random_date(purchase_date, today, threshold=0.15)
        color = colors.get(f"{randint(1, len(colors)):03}")
        number_plate = f"{randint(1, 9999):04}" + "".join(choices(string.ascii_uppercase, k=3))
        kilometers = randint(0, 10000) + 80000 * (min(deregistration_date, today) - purchase_date) / (today - date(2010, 1, 1))
        insurance_company_id = str(randint(1, len(insurance_companies))).zfill(3)
        insurance_company_name = insurance_companies[insurance_company_id]
        insurance_policy_number = insurance_company_name[0] + f"{randint(1, 999):03}-{randint(1, 9999):04}"

        insert_vehicles.append(f"('{i+1:05}', {purchase_date:'%Y-%m-%d'}, {deregistration_date:'%Y-%m-%d'}, \
'{model_id}', '{color}', '{number_plate}', '{kilometers}', '{insurance_policy_number}', '{insurance_company_id}')")
        insert_models.add(f"('{model_id}', '{model_name if len(model_name) <= 3 else model_name.title()}', '{make_id}')")
        insert_makes.add(f"('{make_id}', '{make_name}', '{group_id}')")
        insert_groups.add(f"('{group_id}', '{group_name}')")
        insert_insurance_companies.add(f"('{insurance_company_id}', '{insurance_company_name}')")

    # Create INSERT queries
    vehicles_query = "INSERT INTO keepcoding.vehicles \
(vehicle_id, purchase_date, deregistration_date, model_id, color, number_plate, kilometers, insurance_policy_number, insurance_company_id) \
VALUES " + ", ".join(insert_vehicles) + ";"
    models_query = "INSERT INTO keepcoding.models (model_id, model_name, make_id) VALUES " + ", ".join(insert_models) + ";"
    makes_query = "INSERT INTO keepcoding.makes (make_id, make_name, group_id) VALUES " + ", ".join(insert_makes) + ";"
    groups_query = "INSERT INTO keepcoding.groups (group_id, group_name) VALUES " + ", ".join(insert_groups) + ";"
    insurance_companies_query = "INSERT INTO keepcoding.insurance_companies \
(insurance_company_id, insurance_company_name) VALUES " + ", ".join(insert_insurance_companies) + ";"

    # Update sql file with new generated data
    with open(r".\vehicles.sql", "r+") as f:
        sql = f.readlines()
        n = sql.index("-- Insert data\n")
        f.seek(0)
        f.truncate()
        f.writelines(sql[:n+1])
        f.writelines([groups_query, "\n" * 2, makes_query, "\n" * 2, models_query, "\n" * 2, insurance_companies_query, "\n" * 2, vehicles_query])


if __name__ == "__main__":
    main()
