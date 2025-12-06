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