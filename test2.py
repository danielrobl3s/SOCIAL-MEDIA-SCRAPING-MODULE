import json

file_path = "ouput_link_36.txt"
json_objects = []

with open(file_path, "r") as file:
    for line in file:
        try:
            # Parse each line as a separate JSON object
            json_obj = json.loads(line.strip())
            json_objects.append(json_obj)
        except json.JSONDecodeError as e:
            print(f"Error parsing line: {e}")

# Process your list of JSON objects
print(json_objects)
