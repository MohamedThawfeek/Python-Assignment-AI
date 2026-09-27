
import pandas as pd


def preprocees_dataset(dataset, remove_row=[], remove_col=[], column_name=["Date", "Time", "Name", "Chat"]):
    row_remove = dataset.drop(index=remove_row).reset_index(drop=True)
    final_data = row_remove.drop(remove_col, axis=1)
    Time = final_data[1].str.split("-", n=1, expand=True) 
    Name = Time[1].str.split(":", n=1, expand=True) 
    final_data.columns=[column_name[0], column_name[3]]
    final_data[column_name[1]] = Time[0]
    final_data[column_name[3]] = Time[1]
    final_data[column_name[2]] = Name[0]
    final_data[column_name[3]] = Name[1]

    final_data=final_data[column_name]

    return final_data
