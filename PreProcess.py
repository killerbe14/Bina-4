import pandas as pd
import numpy as np

class PreProcess:

    def __init__(self, pathToDataframe):
        self.df = pd.read_excel(pathToDataframe)
        self.df.fillna(self.df.mean(), inplace=True)  # Fill every missing value with mean
        for column in self.df:
            if self.df[column].dtype != 'object' and self.df[column].name != 'year':
                self.df[column] = (self.df[column] - self.df[column].mean()) / self.df[column].std()  # for every column we do Standardization
        countriesDataList = []
        for country in self.df.country.unique():
            countryData = [];
            linesForCountry = self.df.loc[self.df['country'] == country]
            for column in linesForCountry:
                if linesForCountry[column].dtype != 'object':
                    countryData.append(linesForCountry[column].mean())
                else:
                    countryData.append(country)
            countriesDataList.append(countryData)
        self.countriesDataFrame = pd.DataFrame(countriesDataList, columns=self.df.columns)
        self.countriesDataFrame = self.countriesDataFrame.drop(['year'], axis=1)