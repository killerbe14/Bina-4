import pandas as pd
import numpy as np

class PreProcess:

    def __init__(self, pathToDataframe):
        self.df = pd.read_excel(pathToDataframe)
        self.df.fillna(self.df.mean(), inplace=True)  # Fill every missing value with mean
        for column in self.df:
            if self.df[column].dtype != 'object' and self.df[column].name != 'year':
                self.df[column] = (self.df[column] - self.df[column].mean()) / self.df[column].std()  # for every column we do Standardization
        countriesDataList = []  #  will hold list of information for evey country
        for country in self.df.country.unique():
            countryData = []  # will hold information for the current country
            linesForCountry = self.df.loc[self.df['country'] == country]
            for column in linesForCountry:  # we run on each country's rows and we take the mean if it's numeric and if not we take the name of the country
                if linesForCountry[column].dtype != 'object':
                    countryData.append(linesForCountry[column].mean())
                else:
                    countryData.append(country)
            countriesDataList.append(countryData)  # at the end we add country's information to the list
        self.countriesDataFrame = pd.DataFrame(countriesDataList, columns=self.df.columns)  # we create a new dataframe from the information we got from countries
        self.countriesDataFrame = self.countriesDataFrame.drop(['year'], axis=1)  # we remove the 'year' column