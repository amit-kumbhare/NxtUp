import chromadb
import csv
import sys
import ast
import json
import os
import time
from dotenv import load_dotenv
load_dotenv()
import regex as re

client = chromadb.PersistentClient(path="./chroma_db") # PersistentDB -> Stays on HD without erasing anything
collection = client.get_or_create_collection(name="db_questions_v7")
collection_to_get = client.get_collection(name="db_questions_final_with_titles_fixed_tags")

sys.set_int_max_str_digits(1000000) 
csv.field_size_limit(sys.maxsize) 

groq_api_key = os.getenv("GROQ_API_KEY")
from groq import Groq

groq_client = Groq(api_key=groq_api_key)
def get_cml(desc):
    max_retries = 5
    base_delay = 4

    for at in range(max_retries):
        try:
            time.sleep(2.0)
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": 'You must respond with a JSON object containing a single key "logic" containing a 5-10-word math description. Example: {"logic": "Binary search on answer"}'
                    },
                    {
                        "role" : "user",
                        "content": str(desc)
                    }
                ],
                model="llama-3.1-8b-instant",
                temperature=0,
                response_format={"type": "json_object"}
            )

            raw_string = chat_completion.choices[0].message.content
            proc = json.loads(raw_string)
            return proc["logic"]
        
        except Exception as e:
            # Check if error is rate limit 429
            if "429" in str(e) or "rate_limit" in str(e).lower():
                wait_time = base_delay * (2 ** at)
                print(f"\n[429 Rate Limit Hit], Waiting {wait_time} seconds before retrying.")
                time.sleep(wait_time)
                continue 
            else:
                print(f"\nUncaught Error: {e}")
                return 'Invalid'

def delete_db():
    try:
        client.delete_collection(name="db_questions_fixed")
        print("Existing vector database cleared successfully.")
    except Exception:
        pass

# # Calc total Ques to be processed
with open("codeforces_train.csv", mode="r", encoding="utf-8") as f:
    total_rows = sum(1 for row in csv.reader(f)) - 1 
print(f"Total : {total_rows}")

with open ("codeforces_train.csv", mode="r") as f:
    data = csv.reader(f)
    header = next(data)

    tracker = 0

    for row in data:
        tracker += 1
        rating = int(float(row[18])) if row[18] else 0
        # Converting str of tags to actual list of tags
        # tags = row[19].replace('[', '').replace(']', '').replace('"', '').strip()
        # tags = json.dumps(ast.literal_eval(row[19])) 
        tags = json.dumps(re.findall(r"'([^']+)'", row[19]))
        # CML = get_cml(row[11])
        CML = collection_to_get.get(ids=[row[0]])
        core_math_logic = ""
        # Check if the list contains any matching results
        if CML["ids"] and CML["metadatas"]:
            # Safely look up the 'author' key using .get() to avoid KeyError if it's missing
            core_math_logic = CML["metadatas"][0].get("core_math_logic")
        else:
            print(f"ERROR on {row[0]}")

        collection.add(
            ids=[f"{row[0]}"],
            documents = [row[11]],
            metadatas = [{
                "contestId": row[2],
                "index": row[7],
                "title": row[10],
                "tags" : tags,
                "rating": rating,
                "core_math_logic" : core_math_logic
            }]
        )

        progress_percentage = (tracker / total_rows) * 100
        print(f"Current Prog : {tracker}/{total_rows} ({progress_percentage:.1f}%)", end="\r")

        if tracker % max(1, total_rows // 10) == 0:
            print(f"\n>>>{int(progress_percentage)+1}% Done!")

































