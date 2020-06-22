import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import chart_studio
import plotly.express as px
import plotly.graph_objs as go
import chart_studio.plotly as py

from PreProcess import PreProcess


class Kmeans:

    def __init__(self, dataframe, numOfClusters, numOfInit):
        self.dataframe = dataframe
        self.countries = self.dataframe['country']
        le = LabelEncoder()
        self.dataframe['country'] = le.fit_transform(dataframe['country'])
        self.groups = KMeans(n_clusters=numOfClusters,n_init=numOfInit,).fit_predict(dataframe)
        self.dataframe['group'] = self.groups
        a=1+1

    def draw(self):
        chart_studio.tools.set_credentials_file(username='yuvalkh', api_key='RIFhZ501TiULtcboxut5')
        groups_to_data = {}
        for group,(_,row) in zip(self.groups,self.dataframe.iterrows()):
            if group not in groups_to_data:
                groups_to_data[group] = []
            support, generosity = row['Social support'], row['Generosity']
            groups_to_data[group].append((support,generosity))

        self.scatter = plt.Figure(figsize=(5, 5), dpi=100)
        ax = self.scatter.add_subplot(111)
        for group,value in groups_to_data.items():
            x = [support for support,generosity in value]
            y = [generosity for support,generosity in value]
            ax.scatter(x, y, color=np.random.rand(3, ))
        ax.set_xlabel('Social Support')
        ax.set_ylabel('Generosity')
        ax.set_title('Impact of Social Support on Generosity')

        df_to_draw = self.dataframe.copy()
        df_to_draw['country'] = self.countries
        df_to_draw['group'] = [str (val) for val in self.groups]
        data = go.Choropleth(z=df_to_draw['group'], locations=df_to_draw['country'], locationmode='country names', colorscale='Viridis')
        self.map = go.Figure(data=[data])
        self.map.update_layout(title_text='Choropleth map')
        py.image.save_as(self.map, filename='choropleth-map.png')