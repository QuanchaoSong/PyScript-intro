# Using PyScript for scientific projects: an introduction

### Abstract

In the past, we just use Javascript codes to implement functions within a web page. However, from now on, we can use Python codes to implement functions within webpages, which is very beneficial for our scientific projects because Python has many powerful libraries, at the help of `Pyscript`. The following procedures shows the path to utilize `pyscript` into a webpage.



### Procedures 

#### 1. "Install" the `pyscript` library

To use `pyscript`, actually, we don't need to install it like we install other tools in a normal way. Very simply, we just add two lines of codes within the `<head>` tag, in an html file, let's say, `index.html`.

```html
<!-- index.html -->
<head>
    <title>Pyscript Introduction</title>
    <meta charset="utf-8">
    
    <!-- Add the following 2 lines to utilize `pyscript` -->
    <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
    <script defer src="https://pyscript.net/latest/pyscript.js"></script>
</head>
```

So simple? Yes, that's it! Now we can continue with it.

#### 2. Add UI elements

The next thing we should do is to write html codes within `<body>` tag to implement UI for your page. 

As an example, I write several lines of html codes to make a very simple page, containing an `<input>` element with `file` type and a simple button, which allows users to select a `.txt` file from local disk and get the squared value of that number.

```html
<body>
    <div id="ui-wrapper">
        <h4>Calculate the square of number:</h4>
        <p><i>select a file containing a number</i></p>
        <input id="local-file" type="file" accept=".txt" required />
        <br /><br />
        <div>
            <button id="calculate-button">Calculate</button>
        </div>
        <p id="calculation-result">Result is: </p>
    </div>
</body>
```

#### 3. Configure

After the UI works, we can move on with the functions provided by `pyscript`. But before it, we have to make some configuraton for the Python environment within this `pyscript` page. 

When we write Python codes, normally, we will import some packages like `numpy`, `pandas`, etc. In `pyscript`, we can also do it, and it is what make `pyscript` cool. To import Python packages or modules, we simply add `<py-config>` tag with `<body>`.  Besides, it's better practice to add the `<py-config>` tag after UI works.

```html
<body>
    <div id="ui-wrapper">
        <!-- your UI codes here -->
    </div>
    
    <py-config>
        packages = ["numpy", "matplotlib"]
    </py-config>
</body>
```

In the above example, we are telling `pyscript` that, we want to use 2 packages: `numpy` and `matplotlib`, and `pyscript` will then go to download these 2 packages along with their dependencies. 

In addition, we can also import some Python files here as modules, or files of whatever kind. For example, we have a `test_pyscript.py` at the same folder with `index.html`, we can import it like this:

```html
<py-config>
    packages = ["numpy", "matplotlib"]

    [[fetch]]
    files = ["./test_pyscript.py"]
</py-config>
```

In some cases, you might want to import python files or whatever resources from a remote server.      To achieve it, just add the url of that file as the following.

```html
<py-config>
    packages = ["numpy", "matplotlib"]

    [[fetch]]
    from = "https://web-docs.gsi.de/~ssanjari/pyscript-webpage/"
    files = ["operations.py"] # here the files can be of any type. Not only python files.
</py-config>
```

Then `pyscript` will go to download all files from the server and save them into a certain folder(`/home/pyodide/`) in the virtual file system that is maintained by `pyscript`.

#### 4. Run Python codes

After we get the needed packages & files, we can utilize them within `<py-script>` tag. Within `<py-script>` tag, all codes & comments should be in Python style.

```html
<py-script>
    import numpy as np

    # caculate the square of the number
    def calculate(x):
    	return np.square(x)

    res = calculate(3.3828)        
    print("res:", res)
    # update the UI element
    Element("calculation-result").element.innerHTML = ("Result is: " + str(res))
</py-script>
```

The above codes define a function `calculate` to get the square value of a number, and then call it and change the rendering result(`innerHTML`) of the html element with `calculation-result` as id. 

If you refresh your html page now, the value after "`Result is:`" should be displayed.

For the function `calculate`, we can also move it to the aforementioned `test_pyscript.py` file, and import this function within the `<py-script>` tag, and it should work the same.

`test_pyscript.py`:

```python
# caculate the square of the number
import numpy as np

def calculate(x):    
    return np.square(x)
```

The core parts of `index.html`:

```html
<py-config>
    packages = ["numpy", "matplotlib"]

    [[fetch]]
    files = ["./test_pyscript.py"]
</py-config>

<py-script>
    from test_pyscript import calculate
    
    res = calculate(3.3828)        
    print("res:", res)
    # update the UI element
    Element("calculation-result").element.innerHTML = ("Result is: " + str(res))
</py-script>
```

#### 5.Handle event of html element

In our UI, we have a file-choosing button (`local-file`) which allows us to select a `.txt` file from local disk, and a button(`calculate-button`) to call the function `calculate`. How to run Python codes as soon as we press the `Calculate` button?

The answer is to firstly add `py-onClick` to the `calculate-button` as the following:

```html
<button id="calculate-button" py-onClick="my_calculate()">Calculate</button>
```

then we define a corresponding Python function `my_calculate` within `<py-script>` tag:

```html
<py-script>
    from test_pyscript import calculate

    def my_calculate():
        res = calculate(3.3828)         
        print("res:", res)
        # update the UI element
        Element("calculation-result").element.innerHTML = ("Result is: " + str(res))
</py-script>
```

However, the above codes didn't take the file-choosing button (`local-file`) into the process. Now we need to handle it as well. To get the content of the selected local file, we have to access some properties of the `<input>` element. `Element` is used to access any html element within the webpage.

```python
local_input_element = Element("local-file").element
file_list = local_input_element.files.to_py()
```

Now we get the `file_list`, although it contains only one file. Next, we are able to get the content of the selected file by doing the following:

```python
for f in file_list:
    text_content = await f.text()    
```

Since `f.text()` is an asynchronous function, so we have to add `await` to use it. Therefore,  for the function `my_calculate`, we need to add `async` in front of it, **because `async` and `await` should always be used in pair**.  Now our `my_calculate` function should look like following:

```html
<py-script>
    from test_pyscript import calculate

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
</py-script>
```

Refresh the html page, select a file containing a pure number, and click the `Calculate` button, the correct result should be displayed.

By the way, `pyscript` transcript many javascript functions into python functions, when we need to look up the declared functions for an instance of a certain class, we can do like this:

```python
# take the `f` in the above section as an example
for item in dir(f):
    print("item:", item)
```

#### 6. Use Matplotlib & Bokeh to draw a graph

##### 6.1 Matplotlib

As `Matplotlib` is used very often in scientific projects, therefore I will introduce a basic usage of it within `pyscript`.

Firstly, we add several lines of html codes for the graph drawing:

```html
<h4>Draw graph(Matplotlib)</h4>
<div>
    <button id="draw-button" py-onClick="my_draw_matplotlib()">Draw</button>
</div>
<div id="graph-area"></div>
```

In the above codes, we have a button(`draw-button`) with `my_draw_matplotlib` function bounded. 

Within `<py-script>`, we define the handler function `my_draw_matplotlib` as followings:

```html
<py-script>
    import matplotlib.pyplot as plt
    import numpy as np
    
    # ... other codes
    
    def my_draw_matplotlib():
    	x = np.random.randn(100)
    	y = np.square(x)
    	fig, ax = plt.subplots()
    	ax.scatter(x, y)
    	Element("graph-area").write(fig)
    	# or
    	# display(fig, target="graph-area")
</py-script>
```

Note that, to display the `fig` created by `matplotlib`, we can use 2 ways. 1st way is to use `Element("your-html-element-id").write`, 2nd way is to use `display`. Both ways are demonstrated in the above codes. No matter which way we use, we have to build a connection between the python instance `fig` with the html element `<div id="graph-area" ...>`.

Now we refresh the webpage and click the `Draw` button, a graph will appear on the page. And this is how we can use `matplotlib` within `pyscript`.

##### 6.2 Bokeh

`Bokeh` is also used to draw graphs, although not as famous as `matplotlib`, it's actually a better option, because it provides us with prettier UI and more operation tools. Next, I will introduce how to make a basic usage of `Bokeh`.

Firstly, a bit different from `matplotlib`, we have to add several lines within html's `<head>` tag to fetch the `Bokeh` js functions. Now our `<head>` should look like the followings:

```html
<head>
    <title>Pyscript Introduction</title>
    <meta charset="utf-8">

    <!-- Add the following 2 lines to utilize `pyscript` -->
    <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
    <script defer src="https://pyscript.net/latest/pyscript.js"></script>

    <!-- The followings are for Bokeh -->
    <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-3.0.3.min.js"></script>
    <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-gl-3.0.3.min.js"></script>
    <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-widgets-3.0.3.min.js"></script>
    <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-tables-3.0.3.min.js"></script>
    <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-mathjax-3.0.3.min.js"></script>
</head>
```

Secondly, we add several lines of html codes for the graph drawing(similar to that for `matplotlib`):

```html
<h4>Draw graph(Bokeh)</h4>
<div>
    <button id="draw-button-bokeh" py-onClick="my_draw_bokeh()">Draw</button>
</div>
<div id="graph-area-bokeh"></div>
```

Thirdly,  within the `<py-config>` tag, we add `numpy` and `bokeh` as packages that we are going to use:

```html
<py-config>
    packages = ["numpy", "bokeh", "xyzservices", "pandas"]
</py-config>
```

*Note that, in the latest version of `Bokeh`, `xyzservices` & `pandas` packages should also be included in the `<py-config>` tag, as they are needed by `bokeh`.*

And finally, within the `<py-script>` tag, we implement our `my_draw_bokeh` function:

```html
<py-script>
    import numpy as np
    import json
    from js import Bokeh, console, JSON
    from bokeh.embed import json_item
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    
    def my_draw_bokeh():
        x = np.random.randn(100)
        y = np.square(x)
        p = figure(title="Graph", x_axis_label='x', y_axis_label='y')
        p.circle(x, y, size=3, line_color="navy", fill_color="orange", fill_alpha=0.5)
        p_json = json.dumps(json_item(p, "graph-area-bokeh"))
        Element("graph-area").element.innerHTML = ""
        Bokeh.embed.embed_item(JSON.parse(p_json))
</py-script>
```

Now refresh the webpage, and click the 2nd `Draw` button, a better-looking graph should appear.

#### 7. Move all operations to a single Python file

Now our `index.html` becomes a bit obese because there are many codes for `<py-script>` part. To make the file look concise and elegant, we can move all codes within a `<py-script>` into a separate file.

Let's create a file called `operations.py` under the same folder as `index.html`, and move all python codes within `<py-script>` into it. It will look like the following:

```python
# operations.py
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
    Element("graph-area").element.innerHTML = ""
    Bokeh.embed.embed_item(JSON.parse(p_json))
```

And remember to change the `<py-script>` in the `index.html` to the following:

```html
<py-script src="./operations.py">        
</py-script>
```

Now refresh the page & everything should work as properly as before.

#### 8.  Handle the problem when server doesn't support ".py" files

In some (rare) cases, your server will not support the web browser to download `.py` files, e.g., the server will give you an `500: internal server` error if you try to access a python file stored in the server, for which the `pyscript` project won't work properly. Under this circumstance, we need to use some tricks to get it work.

Firstly, rename the extension names of our python files from `.py` to any other extension names, let's say, `.pyy`. 

```bash
mv all_operations.py all_operations.pyy
mv test_pyscript.py test_pyscript.pyy
```

Secondly, change the corresponding names of the sourced python files. 

```bash
### Within <py-config>
files = ["./test_pyscript.py"] -> files = ["./test_pyscript.pyy"]

### For <py-script>
<py-script src="./operations.py"> -> <py-script src="./operations.pyy">
```

Now if you refresh the webpage, an error like `ModuleNotFoundError: No module named 'test_pyscript'` should be popped out, which is because Python goes to look for modules by the extension name `.py` by default, yet now these files become `.pyy`, for which Python becomes "blind". Luckily, we still have a trick to handle this issue.

Finally, we add one more `<py-script>` before the `<py-script src="./all_operations.pyy">`:

```html
<py-script>
    import os

    my_python_files_dir = '/home/pyodide/'
    files = os.listdir(my_python_files_dir)        
    for filename in files:
        print("filename:", filename)
        name, entension_name = os.path.splitext(filename)
        if (entension_name == ".pyy"):
        	os.rename(my_python_files_dir + filename, my_python_files_dir + name + ".py")
</py-script>
```

The above codes are used to check every file with the extension name of `.py`,  and then rename it back to `.py`. Through this operation, Python is able to find corresponding files of `.py` as extension as the modules. 

In fact, every time we refresh the webpage, `pyscript` will create a linux-like virtual file system within the sandbox folder that the web browser has assigned to `pyscript`. For example, if we run the following python scripts within a `<py-script>` tag:

```html
<py-script>
    import os

    print("Pwd:", os.getcwd())
    files = os.listdir('/')
    print()
    for f in files:
    	print(f)
</py-script>
```

The output will be:

```bash
Pwd: /home/pyodide

tmp
home
dev
proc
lib
```

By default, all files that are declared within `<py-config>` will be downloaded & stored in the `home/pyodide/` folder. 

#### 9. Using a zip file to pack all python files (and other resources) on the server

Sometimes, you might have to load a lot of python files from your server or other servers, e.g., 

```html
<py-config>
    packages = ["numpy", "matplotlib", "bokeh", "xyzservices", "pandas"]

    [[fetch]]
    from = "http://localhost:8000/"
    files = ["f1.py", "f2.py", "f3.py", ..., "f100.py"]
</py-config>
```

In this case, you will have to include many files within the `files` list under `<py-config>`, which is quite repetitive & dull. 

To reduce meaningless repetition, we can pack all these python files into a zip file, then let `pyscript` download them automatically, and finally in the `pyscript` webpage, we unpack the zip file so that these files can be loaded as modules by Python.

Let's say, we put all these python files `f1.py`, `f2.py`, `f3.py`, ..., `f100.py`, etc, into a folder `python_files`, and zip that folder as `python_files.zip`. Now in `<py-config>`, we write as the following:

```html
<py-config>
    packages = ["numpy", "matplotlib", "bokeh", "xyzservices", "pandas"]

    [[fetch]]
    from = "http://localhost:8000/python_files.zip"
    to_folder = "/home/Downloads/"
    to_file = "python_files.zip"
</py-config>
```

In the above, `from` means the the url address of the zip file, which can be held in your server or other servers like GitHub; `to_folder` means into which folder of the virtual file system of `pyscript` you want this zip file to be downloaded, here I make it be `/home/Downloads/`.; `to_file` indicates the name for the downloaded zip file, here in my case I will make it the same as its original name.

If you refresh your webpage now, in the  javascript `Console`, you will see a message like `[pyscript/main] fetching path: http://localhost:8000/python_files.zip`, which means the `pyscript` is downloading the zip file. 

Afterwards, we have to unpack the downloaded zip file to the current working dir of `pyscript`, i.e., `home/pyodide/`. For this, we can use the `zipfile` lib of Python.

```html
<py-script>
    import zipfile
    import os

    zip_file_path = "/home/Downloads/python_files.zip"
    zip_file = zipfile.ZipFile(zip_file_path)
    zip_file.extractall("/home/pyodide/")
    zip_file.close()
    
    if (os.path.exists(zip_file_path)):
    	os.remove(zip_file_path)
</py-script>
```

Now we can add a small `<py-script>` to test if it works:

```html
<py-script>
    from python_files.f1 import test1

    test1()
</py-script>

<!-- 
The codes in `f1.py` are:

def test1():
    print("test1 function works!")
-->
```

If you refresh the webpage, after everything is loaded in few seconds, you will see a message `"test1 function works!"` being printed out in the bottom black area of the webpage. So, now everything works fine in this way to load python files. Surely, this way also can be applied to other resources like an image file, an audio file or any other format files.

#### 10. Trifles to make your `pyscript` webpage more beautiful

##### 10.1 Remove the black area at the bottom of the webpage

As long as you use Python's `print` function within the `<py-script>` tag, a black area containing all the printed messages will be displayed at the bottom of the webpage. So when you publish your webpage in production, remember to comment or delete every line of `print(...)` code.

##### 10.2 Remove the blank space in the bottom

In some cases(not always), when you use `<py-script>` tag, a blank space with white background will be displayed at the bottom of your webpage. This issue actually doesn't affect that much of the beauty of your webpage. However, if you are a perfectionist and really want to remove it, just add a `style` to each `<py-script>` like the following:

```html
<py-script style="height: 0;">
    # your python codes
</py-script>
```



### Conclusion

The `pyscript` project is an very creative project that allows us to implement complex functions within an webpage, at the benefit of Python's countless & super powerful packages. The above procedures demonstrate that it is simple to utilize this intelligent tool into our daily scientific works.
