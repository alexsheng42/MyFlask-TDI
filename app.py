from flask import Flask,render_template,request,redirect
import requests
import simplejson as json
import pandas as pd
import numpy as np
import os
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

app = Flask(__name__)

app.vars={}
#choices = ['Close','Adj. Close','Open','Adj. Open']

@app.route('/index_sheng',methods=['GET','POST'])
def index_sheng():
    if request.method == 'GET':
        return render_template('Small Project.html')
    else:
        app.vars['ticker'] = request.form['ticker']
        app.vars['select'] = request.form.values()
        return redirect('/chart')

@app.route('/chart',methods=['GET','POST'])
def chart():
    ticker = app.vars['ticker']
    select = app.vars['select'][1]
    res = requests.get("https://www.quandl.com/api/v3/datasets/WIKI/"+str(ticker)+".json?start_date=2017-05-01&end_date=2017-06-01&frequency=daily&api_key=mRVPnQBf9hpYoxLWA_iA")
    df = pd.DataFrame(res.json()['dataset']['data'],columns=res.json()['dataset']['column_names']).set_index('Date')   
    def datetime(x):
        return np.array(x, dtype=np.datetime64)
    p = figure(x_axis_type="datetime", title=str(ticker)+" "+str(select))
    p.grid.grid_line_alpha=0.5
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.line(datetime(df.index), df[select],color='#B2DF8A')
    #p.legend.location = "top_left"
    path = os.path.join(os.getcwd(),'templates')
    filename = os.path.join(path,'stocks.html')
    output_file(filename, title="stocks.py example")
    show(p)
    return	render_template('stocks.html')

if __name__ == "__main__":
    app.run(debug=True)



