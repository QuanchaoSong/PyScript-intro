from test_pyscript import calculate
import numpy as np
import matplotlib.pyplot as plt
import json
from js import Bokeh, console, JSON
from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN

async def my_calculate():
    local_input_element = Element("local-file").element
    file_list = local_input_element.files.to_py()
    for f in file_list:
        text_content = await f.text()
        print("text_content:", text_content)
        res = calculate(float(text_content))
        print("result:", res)
        # update the UI element
        Element("calculation-result").element.innerHTML = ("Result is: " + str(res))

def my_draw_matplotlib():    
    x = np.random.randn(100)
    y = np.square(x)
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    Element("graph-area").write(fig)
    # or
    # display(fig, target="graph-area")

def my_draw_bokeh():
    x = np.random.randn(100)
    y = np.square(x)
    p = figure(title="Graph", x_axis_label='x', y_axis_label='y')
    p.circle(x, y, size=3, line_color="navy", fill_color="orange", fill_alpha=0.5)
    p_json = json.dumps(json_item(p, "graph-area-bokeh"))
    Element("graph-area-bokeh").element.innerHTML = ""
    Bokeh.embed.embed_item(JSON.parse(p_json))
