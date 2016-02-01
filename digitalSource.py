# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:29:03 2016

@author: adebayo
"""
import re
import os
import conn
from spyre import server
from collections import Counter
from pandas import DataFrame
from extract import createDataframe
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set(color_codes=True)
rs = np.random.RandomState(7)

class DigitalSourceApp(server.App):
    title = "<font color='#fffaf1'><b>The Digital Source of the Tweets</b></font>"
    
    inputs = [{	'type' : 'slider',
				"label": 'Top', 
				"min" : 0,"max" : 20,"value": 0, 
				"key": 'top' }]
    
    controls = [{"type" : "button",
					"label" : "Plot the Graph",
					"id" : "submit_plot"},
				{"type" : "button",
					"label" : "Load Raw Data",
					"id" : "load_table"}]
     
    outputs = [{"type" : "plot",
					"id" : "plot1",
					"control_id" : "submit_plot",
					"tab" : "Device"},
				{"type" : "table",
					"id" : "table_id",
					"control_id" : "load_table",
					"tab" : "Data"},
				{"type" : "html",
					"id" : "custom_html",
					"tab" : "Description"}]
    tabs = ["Device", "Data", "Description"]
     
     
    def getData(self, params):
         top = int(params['top'])
         regex = re.compile('^<.*>(\w+.*)</.>')
         df = createDataframe()
         source = [str(regex.findall(line)).strip('[]') for line in df['source'] if line != None]
         source = dict(Counter(source))
         appSource = source.keys()
         count = source.values()
         tweetSource = DataFrame({'AppSource': appSource, 'Count':count})
         tweetSource = tweetSource[['AppSource', 'Count']]
         tweetSource.sort_values(by='Count', ascending=False, inplace=True)
         return tweetSource[:top]
         
    def getPlot(self, params):
         output_id = params['output_id']
         df = self.getData(params)
         f, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6), sharex=True)
         # Generate some sequential data
         x = df['AppSource'].tolist()
         y1 =df['Count']
         sns.barplot(x, y1, palette="BuGn_d", ax=ax1)
         ax1.set_ylabel("Sequential")
         
         # Center the data to make it diverging
         y2 = y1 - 1430
         sns.barplot(x, y2, palette="RdBu_r", ax=ax2)
         ax2.set_ylabel("Diverging")
      
         # Randomly reorder the data to make it qualitative
         y3 = rs.choice(y1, len(df), replace=False)
         sns.barplot(x, y3, palette="Set3", ax=ax3)
         ax3.set_ylabel("Qualitative")

         # Finalize the plot
         sns.despine(bottom=True)
         plt.setp(f.axes, yticks=[])
         plt.tight_layout()
         plt.subplots_adjust(top=0.9)
         #f.suptitle('The Digital Source of the Tweets', fontsize=20, fontweight='bold', color='#680000')
         f.autofmt_xdate(rotation=45)
         return f
         
    def getHTML(self, params):
		return "<b>App Description: </b> <i>This application includes Bar charts, Aggregated data and description. \
                   In addition, the application has a filter scale, which could be used to select the number of digital source of the tweets to be presented. \
                   The Filter can scale from 0 to 20, meaning that maximum of top 20 countries of the tweets and minimum of 1. The filter scale cannot generate \
                   charts and aggregated data by itself without pushing of the bottons. Two buttons are included into the application to trigger chart and aggregated data after the filter scale has selected into the appropriate number.. \
                   The first button is to plot the chart while the second is to present the data behind the graph. Furthermore, the chart has three graphs that classify into Sequential, Diverging, and Qualitaive. The sequential bar chart indicate \
                   from top digital source to least digital source while diverging bar chart shows the bar can be twisted by substracting median of the dataset from the dataset. And lastly, the qualitative bar chart provides clarity which digital source has \
                  highest number</i>."

if __name__ == '__main__':
	app = DigitalSourceApp()
	app.launch(port=9090)


      
     
