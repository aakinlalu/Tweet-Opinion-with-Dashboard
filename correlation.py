# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:29:03 2016

@author: adebayo
"""

from spyre import server
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import extract
import seaborn as sns
sns.set(color_codes=True)
rs = np.random.RandomState(7)

class CorrelationApp(server.App):
    title = "<font color='green'>Compare users' number of followers to friends</font>"
    
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
					"tab" : "Bar_Correlation"},
				{"type" : "table",
					"id" : "table_id",
					"control_id" : "load_table",
					"tab" : "Data"},
				{"type" : "html",
					"id" : "custom_html",
					"tab" : "Description"}]
    tabs = ["Bar_Correlation", "Data", "Description"]
     
     
    def getData(self, params):
         top = int(params['top'])
         df = extract.createDataframe()
         df.sort_values(by='followers_count', ascending=False, inplace=True)
         df2 = df[['screen_name','followers_count', 'friends_count']]
         return df2[:top]
         
    def getPlot(self, params):
        output_id = params['output_id']
        df = self.getData(params)
        #fig = plt.figure()  # make figure object
        #splt = fig.add_subplot(1,1,1)
        fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
        ind = np.arange(len(df['screen_name']))
        width = 0.85  
        ax0.bar(ind,df['followers_count'], width, color='g')
        ax1.bar(ind,df['friends_count'], width, color='y')
        ax0.set_ylabel('No of Followers')
        ax1.set_ylabel('No of Friends')
		#splt.set_title('The top Languages of the Tweets', fontsize=20, fontweight='bold', color='r')
		#xTickMarks = ['Group'+str(i) for i in range(1,6)]
        ax0.set_xticks(ind+width/2)
        ax0.set_xticklabels(df['screen_name'].tolist())
        fig.autofmt_xdate(rotation=90)
        return fig
         
    def getHTML(self, params):
		return "<b>App Description: </b> <i>This application includes bar charts of user's friends and followers.</i>"

if __name__ == '__main__':
	app = CorrelationApp()
	app.launch(port=9093)


      
     
