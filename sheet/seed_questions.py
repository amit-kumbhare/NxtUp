import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheet.settings')
django.setup()

from sheet.models import question

def load_questions():
    with open('sheet_problems/1300.json', 'r') as f:
        data = json.load(f)
    
    instances = [
        question(
            problem_id = f"{item["contestId"]}{item["index"]}",
            title = item["title"],
            rating  = item["rating"],
            problem_link = f"https://codeforces.com/problemset/problem/{item["contestId"]}/{item["index"]}",
            solution_link = "",
            star = False,
            notes = None,
            category = ""

        ) for item in data
    ]
    question.objects.bulk_create(instances)

if __name__ == "__main__":
    load_questions()

