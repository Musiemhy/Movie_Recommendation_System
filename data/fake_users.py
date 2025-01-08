import csv
from faker import Faker
import random

fake = Faker()

num_users = 671

users = []
for user_id in range(1, num_users + 1):
    user = {
        "userId": user_id,
        "name": fake.name(),
        "age": random.randint(18, 65),
        "location": f"{fake.city()}, {fake.country()}"
    }
    users.append(user)

csv_file = "fake_users.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["userId", "name", "age", "location"])
    writer.writeheader()
    writer.writerows(users)

print(f"Fake user data generated and saved to {csv_file}")
