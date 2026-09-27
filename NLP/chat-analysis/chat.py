import matplotlib.pyplot as plt
import pandas as pd



def bar_chart_view(dataset, column_name, figsize=(10, 10), chart_type="bar", title="Message Count by Name", xlabel="Name", ylabel="Message Count"):
    plt.figure(figsize=figsize)
    dataset[column_name].value_counts().plot(kind=chart_type, color="skyblue")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



def flirt_chat(dataset, group_column, column_name, label, title, xlabel, ylabel, figsize=(4,4)):
    # Count total messages
    total = dataset.groupby(group_column).size()

    # Count flirting messages
    flirting = dataset[dataset[column_name] == label].groupby(group_column).size()

    # Calculate percentage
    percentage = (flirting / total * 100).fillna(0)

    plt.figure(figsize=figsize)
    plt.bar(percentage.index, percentage.values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    for i, value in enumerate(percentage.values):
        plt.text(i, value, f"{value:.1f}%")
    plt.show()


def pie_chart_view(dataset, column_name, figsize=(10, 10), chart_type="bar", title="Message Count by Name", xlabel="Name", ylabel="Message Count"):
    plt.figure(figsize=figsize)
    dataset[column_name].value_counts().plot(kind=chart_type, color="skyblue")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def group_chart(dataset, date_column_name="Date", group_column_name="Name", title="Date Wise Message Count", xlabel="Date", ylabel="Message Count"):
    dataset[date_column_name] = pd.to_datetime(dataset[date_column_name], dayfirst=True)
    date_count = dataset.groupby([date_column_name, group_column_name]).size().unstack(fill_value=0)
    date_count.plot(kind="bar", figsize=(15, 8))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()