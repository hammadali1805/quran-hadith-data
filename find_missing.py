import json

# Load the JSON file
def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Save the JSON file
def save_data(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Find missing IDs and IDs with incomplete data
def find_missing_and_incomplete_ids(data, start_id, end_id):
    existing_ids = {entry['id'] for entry in data}
    complete_data_ids = {entry['id'] for entry in data if all(entry.values())}

    missing_ids = set(range(start_id, end_id + 1)) - existing_ids
    incomplete_ids = existing_ids - complete_data_ids

    return missing_ids, incomplete_ids

if __name__ == "__main__":
    file_path = "hadiths.json"  # Path to the JSON file
    start_id = 1  # Adjust according to your dataset
    end_id = 3033  # Adjust according to your dataset

    data = load_data(file_path)
    missing_ids, incomplete_ids = find_missing_and_incomplete_ids(data, start_id, end_id)

    print(f"Missing IDs: {len(missing_ids)}")
    print(f"Incomplete IDs: {incomplete_ids}")