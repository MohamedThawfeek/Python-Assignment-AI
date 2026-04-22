import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from scipy.stats import ttest_ind
import seaborn as sns

class Univariate():
     def std_graph(dataset):
        mean=dataset.mean()
        std=dataset.std()
    
        values = [i for i in dataset]
        z_score = [((j-mean)/std) for j in values]
    
        sns.displot(z_score, kde=True)
    
        sum(z_score)/len(z_score)

    
     def t_test_cal(dataset, filter_col, filter_col2, val1, val2, target_col, target_col2):        
         group1 = dataset[dataset[filter_col] == val1][target_col].dropna()
         group2 = dataset[dataset[filter_col2] == val2][target_col2].dropna()
    
         t_stat, p_value = ttest_ind(group1, group2)
    
         return {
                "column":filter_col,
                "column2":filter_col2,
                "filter": val1,
                "filter2": val2,
                "target_col": target_col,
                "target_col2": target_col2,
                "t_stat": t_stat,
                "p_value": p_value
         }
     def categorical_nan_values(dataset, categorical_values):
        # Categorical Values convert
        cat = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        cat.fit(dataset[qual])
        categoricalValues=cat.transform(dataset[qual])
        return categoricalValues
        
     def numaric_nan_values(dataset, numerical_values):
        # Numarical Values convert
        num = SimpleImputer(missing_values=np.nan, strategy='mean')
        num.fit(dataset[numerical_values])
        numericalValues=num.transform(dataset[numerical_values])
        return numericalValues    
   
         
     def quanQual(dataset):
        qual = []
        quan = []
        for colName in dataset.columns:
            if dataset[colName].dtype == "O":
                qual.append(colName)
            else:
                quan.append(colName)
             
    
        return quan, qual

    
         

     

    

   
        
        
         
        