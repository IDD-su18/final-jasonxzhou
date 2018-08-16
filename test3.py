import plotly.plotly as py
import plotly.graph_objs as go
import plotly as plotly

plotly.tools.set_credentials_file(username='jsn_', api_key='9qX0m5gunDfmdAF71K3v')


for i in range(100):
	trace0 = go.Scatter(
	    x=[i, i],
	    y=[i, i]
	)
	data = [trace0]
	plot_url = py.plot(data, filename='extend plot', fileopt='extend')