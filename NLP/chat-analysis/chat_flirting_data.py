from transformers import pipeline
import pandas as pd

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)


labels = ["Flirting", "Friendly", "Neutral"]

def classify_message(message):
    result = classifier(message, labels)
    label = result["labels"][0]
    score = round(result["scores"][0], 4)
    return label, score


def get_flirt_label(dataset, column_name):
    result = dataset[column_name].apply(classify_message)
    return result


def filer_encounter(dataset, group_name, column_name, label):
    # Total messages by each person
    total = dataset.groupby(group_name).size()

    # Flirting messages by each person
    flirting = dataset[
        dataset[column_name] == label
    ].groupby(group_name).size()

    # Flirting percentage
    percentage = (flirting / total * 100).fillna(0)

    # Flirting percentage
    each_flirt_person = []

    for name in total.index:
        each_flirt_person.append(f"{name}: {round(percentage[name], 2)}%")

    return total.idxmax(), total.idxmin(), each_flirt_person


def time_encounter(dataset, column_name, column_name1):
    # Combine Date and Time
    date_time = pd.to_datetime(
    dataset[column_name].astype(str) + " " + dataset[column_name1].astype(str),
    dayfirst=True,
    errors="coerce"
    )
    # Count messages by date
    date_count = date_time.dt.date.value_counts()

    # Count messages by day name
    day_count = date_time.dt.day_name().value_counts()

    # Count messages by hour
    hour_count = date_time.dt.hour.value_counts()

    return date_count.idxmax(), day_count.idxmax(), hour_count.idxmax(), round(date_count.mean(), 1)

