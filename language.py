# tested with python2.7 and 3.4
from spyre import server
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import conn
sns.set(color_codes=True)

class LanguageApp(server.App):
	title = "<font color='white'><b>The Top Languages of the Tweets</b></font>"

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
					"tab" : "Language"},
				{"type" : "table",
					"id" : "table_id",
					"control_id" : "load_table",
					"tab" : "Data"},
				{"type" : "html",
					"id" : "custom_html",
					"tab" : "Description"}]

	tabs = ["Language", "Data", "Description"]

	def getData(self, params):
          '''Return dataframe '''
          top = int(params['top'])
          data = conn.createDataframe()
          data = data['lang'].value_counts()
          lang = [item for item in data.keys()]
          count = [item for item in data]
          language = pd.read_csv('language.csv', sep=',', encoding='utf-8')
          languageAbbr = {language.iloc[i][0]:language.iloc[i][1] for i in np.arange(len(language))}
          lang = [languageAbbr[item] if item in list(language['Abbreviation']) else item for item in lang]
          df = pd.DataFrame({'Language': lang, 'Count':count})
          df = df[['Language', 'Count']]
          return df[:top]
        
	def getPlot(self, params):
		output_id = params['output_id']
		data = self.getData(params)  # get data
		fig = plt.figure()  # make figure object
		splt = fig.add_subplot(1,1,1)
		ind = np.arange(len(data['Language']))
		width = 0.85  
		splt.bar(ind,data['Count'], width, color='r')
		splt.set_ylabel('Number of tweets', fontweight='bold')
		#splt.set_title('The top Languages of the Tweets', fontsize=20, fontweight='bold', color='r')
		#xTickMarks = ['Group'+str(i) for i in range(1,6)]
		splt.set_xticks(ind+width/2)
		splt.set_xticklabels(data['Language'].tolist())
		fig.autofmt_xdate(rotation=45)
		return fig

	def getHTML(self, params):
		return "<b>App Description: </b> <i>This application includes Bar chart, Aggregated data and description. \
                   In addition, the application has a filter scale, which could be used to select the number of languages to be presented. \
                   The Filter can scale from 0 to 20, meaning that maximum of top 20 language of the tweets and minimum of 1. The filter scale cannot generate \
                   charts and aggregated data by itself without pushing of the bottons. Two buttons are included into the application to trigger chart and aggregated data after the filter scale has selected into the appropriate number.. \
                   The first button is to plot the chart while the second is to present the data behind the graph.</i>"

if __name__ == '__main__':
	app = LanguageApp()
	app.launch(port=9092)

