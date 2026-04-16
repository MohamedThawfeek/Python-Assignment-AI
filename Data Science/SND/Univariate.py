import pandas as pd
import numpy as np
from matplotlib import pyplot
from scipy.stats import norm
import seaborn as sns

class Univariate():
     def replaceOutlierGreater(loopvalues, dataset, descriptive, heading):
        for columnName in loopvalues:
            limit = descriptive.loc[heading, columnName]
            mask = dataset[columnName] > limit
            dataset.loc[mask, columnName] = limit
        return dataset

         
     def replaceOutlierLesser(loopvalues, dataset, descriptive, heading):
        for columnName in loopvalues:
            limit = descriptive.loc[heading, columnName]
            mask = dataset[columnName] < limit
            dataset.loc[mask, columnName] = limit
        return dataset
      

         
     def getOutlayer(quan, heading1, heading2, descriptive):
         values = []
        
         for columnName in quan:
            if(heading1 == "Min" and descriptive.loc[heading1, columnName] < descriptive.loc[heading2, columnName]):
                values.append(columnName)
            if(heading1 == "Max" and descriptive.loc[heading1, columnName] > descriptive.loc[heading2, columnName]):
                values.append(columnName)
         return values


        
     def freqTable(columnName, dataset):
        freeqTable = pd.DataFrame(columns=["Unique_values", "Frequency", "Relative_Frequency", "Cumsum"])
        freeqTable["Unique_values"]=dataset[columnName].value_counts().index
        freeqTable["Frequency"]=dataset[columnName].value_counts().values
        freeqTable["Relative_Frequency"]=(freeqTable["Frequency"]/len(dataset[columnName].value_counts().index))
        freeqTable["Cumsum"]=dataset["ssc_p"].value_counts().values
        return freeqTable
         
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
                                  "IQR", "1.5rule", "Lesser", "Greater", "Min", "Max" ], columns=quan)
        for columnName in quan:
            descriptive.loc["Mean", columnName] = dataset[columnName].mean()
            descriptive.loc["Median", columnName] = dataset[columnName].median()
            descriptive.loc["Mode", columnName] = dataset[columnName].mode()[0]
            descriptive.loc["Q1:25%", columnName] = dataset.describe()[columnName]["25%"]
            descriptive.loc["Q2:50%", columnName] = dataset.describe()[columnName]["50%"]
            descriptive.loc["Q3:75%", columnName] = dataset.describe()[columnName]["75%"]
            descriptive.loc["99%", columnName] = np.percentile(dataset[columnName], 99)
            descriptive.loc["Q4:100%", columnName] = dataset.describe()[columnName]["max"]
            descriptive.loc["IQR", columnName] = descriptive.loc["Q3:75%", columnName] - descriptive.loc["Q1:25%", columnName]
            descriptive.loc["1.5rule", columnName] = 1.5 * descriptive.loc["IQR", columnName]
            descriptive.loc["Lesser", columnName] = descriptive.loc["Q1:25%", columnName] - descriptive.loc["1.5rule", columnName]
            descriptive.loc["Greater", columnName] = descriptive.loc["Q3:75%", columnName] + descriptive.loc["1.5rule", columnName]
            descriptive.loc["Min", columnName] = dataset[columnName].min()
            descriptive.loc["Max", columnName] = dataset[columnName].max()
            
             
        return descriptive

     def get_pdf_density (dataset, start, end):        
         ax = sns.displot(dataset, kde=True, color='Green')
         pyplot.axvline(start, color='red')
         pyplot.axvline(end, color='red')
         sample = dataset
         simple_mean= sample.mean()
         simple_std= sample.std()
         print('Mean=%.3f, standard Deviation=%.3f' % (simple_mean, simple_std))
         dist = norm(simple_mean, simple_std)
         values = [value for value in range(start, end)]
         probility = [dist.pdf(value) for value in values]
         prob =sum(probility)
         print("The area between range({},{}):{}".format(start, end, sum(probility)))
         return prob

     def stdNBGraph (dataset):
         import seaborn as sns
         mean = dataset.mean()
         std = dataset.std()    
         values = [i for i in dataset]
         z_score = [((j-mean)/std) for j in values]
         sns.distplot(z_score, kde=True)
         sum(z_score)/len(z_score)

   
        
        
         
        