import json
import pandas as pd

file_names = [
    "porfolio_chat.json"
]

all_conversations = []

for file_name in file_names:
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)
        all_conversations.extend(data["conversation"])

dataset = pd.DataFrame(all_conversations)

dataset = dataset.drop_duplicates(
    subset=["question"]
).reset_index(drop=True)

questions = dataset["question"].tolist()
answers = dataset["answer"].tolist()

dataset.to_csv(
    "my_portfolio_data.csv",
    index=False,
    encoding="utf-8"
)

print("CSV created successfully")
print("Total conversations:", len(dataset))