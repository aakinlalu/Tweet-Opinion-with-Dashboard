# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 17:26:03 2016

@author: adebayo
"""

from spyre import server
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import extract
sns.set(color_codes=True)


class countApp(server.App):
    title = "<font color='white'><b> Correlation of Friends and Followers</b></font>"
    
    inputs = [{	'type' : 'slider',
				"label": 'Range', 
				"min" : 0,"max" : 300000,"value": 0, 
				"key": 'range' }]
    
    controls = [{"type" : "hidden",
			"id" : "update_data"}]
   
    outputs = [{	"type" : "plot",
			"id" : "plot",
			"control_id" : "update_data",
			"tab" : "Correlation"},
		    {"type" : "table",
			"id" : "table_id",
			"control_id" : "update_data",
			"tab" : "Table",
			"on_page_load" : True },
               {"type" : "html",
			 "id" : "custom_html",
			"tab" : "Description"}]
   
    tabs = ["Correlation", "Table", "Description"]
    
    def getData(self, params):
          '''Return dataframe '''
          range = int(params['range'])
          df = extract.createDataframe()
          df = df[['followers_count', 'friends_count']]
          return df[:range]
    
    def getPlot(self, params):
         output_id = params['output_id']
         df = self.getData(params)
         fig = plt.figure()  # make figure object
         spl = fig.add_subplot(1,1,1)
         # Generate some sequential data
         x = df['followers_count']
         y = df['friends_count']
         spl.scatter(x, y)
         spl.set_ylabel("Number of followers")
         spl.set_xylabel("Number of friends")
         return fig
    
    def getHTML(self, params):
		return "<b>App Description: </b> <i>This application includes scatter chart of user's friends and followers.</i>"

if __name__ == '__main__':
	app = countApp()
	app.launch(port=9094)
