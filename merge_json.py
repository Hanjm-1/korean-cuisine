import json
import os
import random
import string
from datetime import datetime, timedelta


def generate_random_string_id(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(length))


# Function to sort JSON by 'created_at' field
def sort_by_created_at(json_list):
    return sorted(json_list, key=lambda x: x["created_at"])


# Check if 'db.json' exists, and if so, load its data
merged_json = []
if os.path.exists("db.json"):
    with open("db.json", "r") as f:
        merged_json = json.load(f)

# Create a set to store unique representations of the existing JSON objects
existing_json_set = set(
    json.dumps({k: v for k, v in item.items() if k not in ["id", "created_at"]})
    for item in merged_json
)

# Load new JSON files and append them to the existing data
json_files = [
    os.path.join("./data", f)
    for f in os.listdir("./data")
    if os.path.isfile(os.path.join("./data", f))
]

for json_file in json_files:
    with open(json_file, "r") as f:
        json_data = json.load(f)
        # Create a unique representation of the current JSON object
        json_rep = json.dumps(
            {k: v for k, v in json_data.items() if k not in ["id", "created_at"]}
        )

        if json_rep not in existing_json_set:
            json_data["id"] = generate_random_string_id()
            json_data["created_at"] = (
                datetime.utcnow() + timedelta(hours=9)
            ).isoformat()
            merged_json.append(json_data)
            existing_json_set.add(json_rep)

# Sort the merged JSON by the 'created_at' field
merged_json = sort_by_created_at(merged_json)

# Save the sorted, merged JSON back to 'db.json'
with open("db.json", "w") as f:
    json.dump(
        merged_json,
        f,
        ensure_ascii=False,
        indent=4,
    )
