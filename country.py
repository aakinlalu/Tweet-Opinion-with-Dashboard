from spyre import server
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import extract
sns.set(color_codes=True)


class CountryApp(server.App):
    title = "<font color='#fffaf1'><b>The Top 5 Countries of the Tweets</b></font>"
    
    inputs = [{ "type": 'dropdown',
                "label": 'Top',
                "options" : [   {"label": "Top 5 Countries", "value": 5}],
                "variable_name": 'top',
                "value": 5,
                "action_id": 'submit_plot'
                }]
             
    controls = [{"control_type": 'hidden',
                  "label": 'plot',
                  "id": 'submit_plot'}]

                   
    outputs = [{"output_type": "plot",
                "output_id": "plot",
                "control_id": 'submit_plot',
                "tab": 'Country'
                },

                {"output_type": 'table',
                "output_id": 'table_id',
                "control_id": 'submit_plot',
                "tab": 'Data',
                "on_page_load" : "true"},
               {"type" : "html",
                  "id" : "custom_html",
                  "tab" : "Description",
                  "on_page_load" : "true"}]
                 
    tabs = ["Country", "Data", "Description"]


    def getData(self, params):
        top = int(params['top'])
        df = extract.createDataframe()
        #tweet_by_country = df[df['country'] != 'no text']
        tweet_by_country = df['country'].value_counts()
        country = [item for item in tweet_by_country.keys()]
        count = [item for item in tweet_by_country]
        tweet_by_country = pd.DataFrame({'Country':country, 'Count': count})
        tweet_by_country = tweet_by_country[['Country', 'Count']]
        return tweet_by_country[:top]

    def getPlot(self, params):
        output_id = params['output_id']
        data = self.getData(params)
        fig = plt.figure(1, figsize=(6,6))
        spl = fig.add_subplot(1,1,1)
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'purple']
        explode = (0.1, 0, 0, 0,0)  # explode 1st slice
        spl.pie(data['Count'], explode=explode, labels=data['Country'].tolist(), colors=colors, 
                autopct='%1.1f%%', shadow=True, startangle=90)
        #spl.set_ylabel('Number of tweets')
        #spl.set_title('The 5 Top Countries of the tweets', fontsize=20, fontweight='bold', color='#680000')
        spl.axis('equal')
        return fig
    
    
    def getHTML(self, params):
        return "<b>App Description: </b> <i>This application includes pie chart to present number of countries the tweets are from. Due to the less flexibility of pie chart, the application limits the pie chart to the top five ccountries.</i>"

if __name__ == '__main__':
  app = CountryApp()
  app.launch(port=9091)   