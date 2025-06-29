import pathway as pw
import os
import json

# Define a schema for recipes
class Recipe(pw.Schema):
    title: str
    step_number: int
    step_text: str

def load_recipes():
    files = os.listdir("../data/recipes/")
    data = []
    for f in files:
        with open(f"../data/recipes/" + f) as json_file:
            recipe = json.load(json_file)
            for i, step in enumerate(recipe["steps"], start=1):
                data.append({
                    "title": recipe["title"],
                    "step_number": i,
                    "step_text": step
                })
    return data

if __name__ == "__main__":
    data = load_recipes()
    table = pw.Table.from_records(data, schema=Recipe)
    print("Ingested recipes into Pathway!")
