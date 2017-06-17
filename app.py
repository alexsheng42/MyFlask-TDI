from flask import Flask,render_template,request,redirect
import requests
import pandas as pd
import os
import numpy as np
import bokeh
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
bv = bokeh.__version__

app = Flask(__name__)

app.vars={}

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
    app.vars['desc'] = res.json()['dataset']['name'].split(',')[0]

    def datetime(x):
        return np.array(x, dtype=np.datetime64)
    
    plot = figure(x_axis_type="datetime", title=str(ticker)+" "+str(select))
    plot.grid.grid_line_alpha=0.5
    plot.xaxis.axis_label = 'Date'
    plot.yaxis.axis_label = 'Price'
    plot.line(datetime(df.index), df[select],color='#B2DF8A')
    #p.legend.location = "top_left"
    script,div = components(plot)

    return	render_template('graph.html', bv=bv, ticker=app.vars['ticker'], script=script, div=div)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port,debug=True)
	#app.run(debug=True)




