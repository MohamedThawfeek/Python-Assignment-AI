import pandas as pd
import numpy as np

class Univariate():
     def quanQual(dataset):
        qual = []
        quan = []
        for colName in dataset.columns:
            if dataset[colName].dtype == "O":
                qual.append(colName)
            else:
                quan.append(colName)
             
    
        return quan, qual
         

     def descriptiveDataset(quan, dataset):
        descriptive = pd.DataFrame(index=["Mean", "Median", "Mode", 
                                  "Q1:25%", "Q2:50%", "Q3:75%", "99%", "Q4:100%", 
                                 ], columns=quan)
        for columnName in quan:
            descriptive.loc["Mean", columnName] = dataset[columnName].mean()
            descriptive.loc["Median", columnName] = dataset[columnName].median()
            descriptive.loc["Mode", columnName] = dataset[columnName].mode()[0]
            descriptive.loc["Q1:25%", columnName] = dataset.describe()[columnName]["25%"]
            descriptive.loc["Q2:50%", columnName] = dataset.describe()[columnName]["50%"]
            descriptive.loc["Q3:75%", columnName] = dataset.describe()[columnName]["75%"]
            descriptive.loc["99%", columnName] = np.percentile(dataset[columnName], 99)
            descriptive.loc["Q4:100%", columnName] = dataset.describe()[columnName]["max"]
        return descriptive

   
        
        
         
        