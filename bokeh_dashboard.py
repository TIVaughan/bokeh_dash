from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Slider, Select
from bokeh.layouts import row, column, widgetbox
from bokeh.models.widgets import Panel, Tabs
import pandas as pd

# File Read, date formatting
otp = pd.read_csv("otp_scores.csv")
otp['date']=pd.to_datetime(otp['date'])
ap = pd.read_csv("ap_scores.csv")
ap['date']=pd.to_datetime(ap['date'])
otp.head()

# Hover tool creation with tooltips
hover = HoverTool(tooltips=[
    ('Score', '@value'),
    ('Success', '@succ_1'),
    ('Failure', '@fail_0'),
    ('Duration (top)', '@dur_8'),
    ('Page Load (top)', '@page_8')
], mode='vline')

# Creating P1 Figure (OTP Composite)
p1 = figure(title='One Time Payment Composite', x_axis_label='Date', y_axis_label='Score', tools=[hover, 'crosshair', 'box_select'], plot_width=640, x_axis_type='datetime')
p1.line('date', 'value', source=otp, line_width = 3, line_alpha = .6)
p1.title.align = "center"
p1.title.text_font_size = "25px"

# Creating P2 Figure, (AP Composite)
p2 = figure(title='Autopay Composite', x_axis_label='Date', y_axis_label='Score', tools=[hover, 'crosshair', 'box_select'], plot_width=640, x_axis_type='datetime')
p2.line('date', 'value', source=ap, line_width = 3, line_alpha = .6)
p2.title.align = "center"
p2.title.text_font_size = "25px"

# Variables for multi-line plot
xmulti = [otp['date'], ap['date']]
ymulti = [otp['value'], ap['value']]

# Creating P3 figure (combined view plot)
p3 = figure(title='Combined View', x_axis_label='Date', y_axis_label='Score', tools=['crosshair', 'box_select'], plot_width=1280, x_axis_type='datetime')
p3.multi_line(xmulti, ymulti, line_color = ['#008CFF', '#004366'], line_width = 3, line_alpha = .6,)
# Trying to fix HoverTool for combined view chart
p3.add_tools(HoverTool(tooltips=[
    ('Score', '@value')
], mode='vline'))
# Changing Layout for P3 Specifically
p3.background_fill_color = "grey"
p3.background_fill_alpha = 0.3
p3.title.align = "center"
p3.title.text_font_size = "25px"

# Matching Ranges to have better comparisons
p1.x_range = p2.x_range = p3.x_range
p1.y_range = p2.y_range = p3.y_range

# Creating Tables for Shared Outcome Tab
p4 = figure(title='Crash Rate', x_axis_label='Date', y_axis_label='Score', tools=['crosshair', 'box_select'], plot_width=1280, x_axis_type='datetime')
p4.multi_line(xmulti, ymulti, line_color = ['#008CFF', '#004366'])
# Again, trying to fix HoverTool
p4.add_tools(HoverTool(tooltips=[
    ('Score', '@value')
], mode='vline'))
# P4 Customizations
p4.background_fill_color = "grey"
p4.background_fill_alpha = 0.3
p4.title.align = "center"
p4.title.text_font_size = "25px"

# Figure for Experimentation Metrics
p5 = figure(title='Experimentation Composite', x_axis_label='Date', y_axis_label='Score', tools=[hover, 'crosshair', 'box_select'], plot_width=640, x_axis_type='datetime')
p5.line('date', 'value', source=otp)
p5.title.align = "center"
p5.title.text_font_size = "25px"

# Creating Drop Down Filter Object
menu = Select(options=['All', 'BHN', 'TWC', 'CHTR'], value='All', title='Footprint')

# Filter Definitions TBD


# Creating Panel Objects for Tabs
quality = Panel(child=column(menu, row(p1, p2), p3), title='Quality Composite Scores')
shared = Panel(child=p4, title='MSA Shared Outcomes')
experiments = Panel(child=p5, title='Experimentation')
customer = Panel(child=row(p1,p2), title='Customer Feedback')

# Tabbed layout
tabs= Tabs(tabs=[quality, shared, experiments, customer])

output_file('metrics.html')
show(tabs)
