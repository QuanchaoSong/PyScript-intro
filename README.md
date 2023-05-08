[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7907144.svg)](https://doi.org/10.5281/zenodo.7907144)

# PyScript for scientific projects: an introduction

### Abstract

The `pyscript` framework gives us a new way to use Python within web browsers in our everyday projects, which is especially useful for scientists, as Python is known for providing us with many scientific packages. Using `pyscript` to build a Python-based web page sounds exciting, but at the same time a bit adventurous, because `pyscript` is a new programming technology that is still in its early stages of development. Therefore, when you actually use it, you will encounter some non-acclimation. By presenting you how a `pyscript` project is constructed step by step from zero, this paper helps you to adapt to this new `pyscript` programming environment at a faster pace, which is especially beneficial for scientists.



### Introduction

Traditionally, when we build a web page, we write html, css and javascript code. We use html code to frame the UI of the page, css code to decorate the frame, and javascript code for the actions within the page.  However, from now on we can replace the javascript code with python code using `pyscript`. The revolutionary thing about `pyscript` is that we can now write Python code for the actions of html elements. As we know, python is widely used in scientific fields, and it also provides us with tons of excellent packages like "numpy", "scipy", "matplotlib", etc. The following procedures show the path to utilize `pyscript` to build a web page for scientific purposes. Note that since graph drawing functions are used quite often, we include two ways to draw graphs, through the famous packages `matplotlib` and `bokeh`. In addition, at the end of this paper, we offer small tips to make your web pages more robust and user-friendly, according to our development experience while using `pyscript`.

### Procedures 

#### 1. "Install" the `pyscript ` framework

To use `pyscript`, we don't actually need to install it the way we install other tools. Very simply, we just add two lines of code inside the `<head>` tag, in an html file, let's say `index.html`.

```html
<!-- index.html -->
<html>
    <head>
        <title>Pyscript Introduction</title>
        <meta charset="utf-8">

        <!-- Add the following 2 lines to utilize `pyscript` -->
        <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
        <script defer src="https://pyscript.net/latest/pyscript.js"></script>
	</head>
</html>
```

The "installation" is not at all sophisticated. Let's continue.

#### 2. Add UI elements

The next thing we should do is write html code inside the `<body>` tag to implement the UI for our page.

As an example, we will write a few lines of html code to create a very simple page containing a `<input>` element of type `file` and a simple button that allows users to select a `.txt` file from the local disk and get the square value of that number.

```html
<html>
    <head>
        ...
    </head>
    
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
</html>
```

Now open this `index.html` file with any web browser, you should see that the UI is rendered properly, at the same time a loading animation widget for `pyscript` is automatically displayed. After a few seconds of downloading essential materials for the `pyscript` environment, the loading animation widget will disappear.

<img width="1172" alt="Screen Shot 2023-05-05 at 4 01 20 PM" src="https://user-images.githubusercontent.com/47345588/236534910-0d3b8d32-d7ee-4338-af2c-ff6000004501.png">

#### 3. Configure

Now that the UI is working, we can move on to implementing functions using `pyscript`. But before we do that, we need to do some configuration for its Python environment within this `pyscript`-based web page.

When we write Python code, we usually import some non-native packages like `numpy`, `pandas`, `matplotlib`, etc. In `pyscript` we can do this too, and this is what makes `pyscript` cool. To import Python packages or modules, we simply add a `<py-config>` tag with `<body>`.  Also, it's better practice to add the `<py-config>` tag after the UI works.

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

In the above example, we tell `pyscript` that we want to use two packages: `numpy` and `matplotlib`, and `pyscript` will then go to download these two packages along with their dependencies.

We can also import some Python files here as modules, or files of any kind. For example, if we have a `test_pyscript.py` in the same folder as `index.html`, we can import it like this:

```html
<py-config>
    packages = ["numpy", "matplotlib"]

    [[fetch]]
    files = ["./test_pyscript.py"]
</py-config>
```

In some cases we may want to import Python files or other resources from a remote server.      To do this, simply add the URL of that file as follows:

```html
<py-config>
    packages = ["numpy", "matplotlib"]

    [[fetch]]
    # just an example
    from = "https://web-docs.gsi.de/~ssanjari/pyscript-webpage/"
    files = ["operations.py"] # here the files can be of any type. Not only python files.
</py-config>
```

Then `pyscript` will download all the files mentioned in the `files` list from the server and store them in a specific folder (`/home/pyodide/`) in the virtual file system maintained by `pyscript`.

#### 4. Execute Python codes

After getting the required packages & files, we can use them inside `<py-script>` tag. Inside the `<py-script>` tag, all codes & comments should be in Python style.

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

In the codes above, we define a function `calculate` to get the square value of a number, then we call it and change the rendering result(`innerHTML`) of the html element with `calculation-result` as id.

If we refresh our html page now, the value after "`Result is:`" should be displayed.

For the `calculate` function, we can also move it to the `test_pyscript.py` file mentioned above, and import this function inside the `<py-script>` tag, and it should work the same way.

Firstly, create `test_pyscript.py`:

```python
# caculate the square of the number
import numpy as np

def calculate(x):    
    return np.square(x)
```

The core parts of `index.html` becomes as follows:

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

If we now refresh this html page, we will most likely get an error like this:

<img width="1051" alt="Screen Shot 2023-05-05 at 4 21 17 PM" src="https://user-images.githubusercontent.com/47345588/236535042-220fbc03-ea1b-4f1f-8c8d-903bea89e0aa.png">

In this case we need to serve this folder with an http server. We have many options to start an http server on a specific folder, such as using [Servez](https://greggman.github.io/servez/), or running simple python commands in the terminal:

```bash
$ cd ~/.../your_project_folder
$ python3 -m http.server
# Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

Now enter `http://localhost:8000` in the web browser and the error should no longer appear.

In this section, the Python codes are triggered automatically after the page loads. In the next section, we will discuss how to trigger python codes to run when the user clicks on some UI elements.

#### 5.Handle event of html elements

As mentioned in the `Introduction`, `pyscript` provides a bridge between html elements and python functions, and we will now take advantage of this feature.  In our UI we have a file select button (`id="local-file"`) that allows us to select a `.txt` file from the local disk, and a button (`id="calculate-button"`) that calls the Python function `calculate`. Now we go on to execute the Python code as soon as we press the `Calculate` button.

Firstly we need to add `py-onClick` to the `calculate-button` element, as follows:

```html
<button id="calculate-button" py-onClick="my_calculate()">Calculate</button>
```

Then, we define a corresponding python function `my_calculate` within `<py-script>` tag:

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

However, the above code didn't include the file select button (`id="local-file"`) in the process. Now we need to handle it as well. To get the content of the selected local file, we have to access some properties of the `<input>` element. `Element` in `pyscript` is used to access any html element within the webpage, which is similar to `document.getElementById()` in javascript.

```python
local_input_element = Element("local-file").element
file_list = local_input_element.files.to_py()
```

Now we have the `file_list', although it only contains one file, as we didn't allow multiple file selections. Next, we can get the contents of the selected file by doing the following:

```python
for f in file_list:
    text_content = await f.text()    
```

Since `f.text()` is an asynchronous function, we need to add `await` to use it. So for the function `my_calculate` we need to add `async` in front of it, **because `async` and `await` should always be used in pairs**.  Now our `my_calculate` function should look like this:

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

By the way, `pyscript` transcribes many javascript functions into python functions, so if we need to look up the declared functions for an instance of a particular class, we can do so:

```python
# take the `f` in the above `<py-script>` as an example
for item in dir(f):
    print("item:", item)
```

#### 6. Use `matplotlib` & `bokeh` to draw a graph

##### 6.1 matplotlib

Since `matplotlib` is used very often in scientific projects, we will introduce the basic way of using it within `pyscript`.

First, we add a few lines of html code for graph drawing:

```html
<!-- Add the following html codes after `<p id="calculation-result">Result is: </p>` -->
<h4>Draw graph(Matplotlib)</h4>
<div>
    <button id="draw-button" py-onClick="my_draw_matplotlib()">Draw</button>
</div>
<div id="graph-area"></div>
```

In the codes above we have bound a button(`id="draw-button"`) to the `my_draw_matplotlib` function.

Within `<py-script>`, we define the handler function `my_draw_matplotlib` as the follows:

```html
<py-script>
    from test_pyscript import calculate
    import matplotlib.pyplot as plt
    import numpy as np
    
    # ... other codes
    
    def my_draw_matplotlib():
    	# y = x^2
    	x = np.random.randn(100)
    	y = np.square(x)
    	fig, ax = plt.subplots()
    	ax.scatter(x, y)
    	Element("graph-area").write(fig)
    	# or
    	# display(fig, target="graph-area")
</py-script>
```

In the `my_draw_matplotlib` function above, we are going to scatter some points according to a simple mathematical formula:
$$
y = x^2
$$
Note that to display the `fig` created by `matplotlib` we can use 2 ways. The 1st way is to use `Element("your-html-element-id").write`, the 2nd way is to use the `display` function. Both ways are demonstrated in the codes above. No matter which way we use, we need to make a connection between the instance `fig` in `matplotlib` and the html element `<div id="graph-area" ...>`.

Now, if we refresh the web page and click on the `Draw` button, a standard parabolic equation graph will appear on the page.

<img width="1172" alt="Screen Shot 2023-05-05 at 4 56 54 PM" src="https://user-images.githubusercontent.com/47345588/236535161-a35d4fce-213a-45a7-a4bf-97ab00ce244f.png">

This is how we can use `matplotlib` within `pyscript`.

##### 6.2 Bokeh

Although not as famous as `matplotlib`, `Bokeh` is also used to draw scientific plots, and it's actually a better option because it gives us a nicer UI and more operation tools like `zoom`, `select` and `animate`, etc. Next, we will show you how to make a basic use of `Bokeh`.

Firstly, unlike `matplotlib`, we need to add a few lines inside the `<head>` tag of the html to get the `Bokeh` js functions. Now our `<head>` should look like this:

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

Secondly, we add a few lines of html code for the plotting UI, similar to that for `matplotlib`:

```html
<!-- Add the following html codes after `<div id="graph-area"></div>` -->
<h4>Draw graph(Bokeh)</h4>
<div>
    <button id="draw-button-bokeh" py-onClick="my_draw_bokeh()">Draw</button>
</div>
<div id="graph-area-bokeh"></div>
```

Thirdly,   inside the `<py-config>` tag, we add `numpy` and `bokeh` as the packages we will use:

```html
<py-config>
    packages = ["numpy", "matplotlib", "bokeh", "xyzservices", "pandas"]
</py-config>
```

*Note that in the latest version of `Bokeh`, `xyzservices` & `pandas` packages should also be included for `packages` in the `<py-config>` tag, as they are needed by `bokeh`.*

Finally, inside the `<py-script>` tag, we implement our `my_draw_bokeh` function.

```html
<py-script>
    # ... other `imports`
    import numpy as np
    import json
    from js import Bokeh, console, JSON
    from bokeh.embed import json_item
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    
    # ... other codes omitted
    
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

Now refresh the web page, and click on the 2nd `Draw` button, a better-looking graph by `bokeh` should be displayed.

<img width="1172" alt="Screen Shot 2023-05-05 at 5 16 37 PM" src="https://user-images.githubusercontent.com/47345588/236535260-ca2f9dd7-0f87-4ad8-9a4d-ec7fd1accc9f.png">

#### 7. Move all operation codes into a single Python file

Now our `index.html` is getting a bit fat because there are many lines of Python code under the `<py-script>` tag. To make the file look concise and elegant, we can move all the python code inside a `<py-script>` into a separate file.

Let's create a file called `operations.py` in the same folder as `index.html` and move all the python code inside the `<py-script>` tag into it. It will look like this:

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

Also remember to change the `<py-script>` part of the `index.html` as follows:

```html
<py-script src="./operations.py">        
</py-script>
```

Now refresh the page, and everything should work properly as before.

#### 8.  Dealing with the problem when the server doesn't support `.py` files

##### 8.1 The process of changing the extension names of Python files

In some (rare) cases, your server may not support the web browser to download `.py` files, e.g., the server will give you an `500: internal server` error if you try to access a python file stored in the server. Under these circumstances, the `pyscript` project won't work properly because it can't fetch the python code it needs. For this situation, we have some tricks to make it work.

Firstly, rename the extensions of our Python files from `.py' to any other extension, let's say `.pyy'.

```bash
# in the project folder
$ mv all_operations.py all_operations.pyy
$ mv test_pyscript.py test_pyscript.pyy
```

Secondly, change the corresponding names of the sourced Python files within `<py-config>` and `<py-script>` tags.

```bash
### Within <py-config>
files = ["./test_pyscript.py"] -> files = ["./test_pyscript.pyy"]

### For <py-script>
<py-script src="./operations.py"> -> <py-script src="./operations.pyy">
```

Now, if you refresh the web page, an error like `ModuleNotFoundError: No module named 'test_pyscript'` should pop up, which is because python goes to look for modules by the extension name `.py` by default, but, now that these `.py` files have been changed to `.pyy`, python is "blind" to them.

Fortunately, we can solve this problem with the following procedure, which essentially involves changing the extension from `.pyy` back to `.py` so that python can "see" these files and then load them as modules.

What we need to do is to add another `<py-script>` tag of code after the `<py-config>` tag and before the `<py-script src="./all_operations.pyy">` tag:

```html
<py-config>
    ...
</py-config>

<!-- Add the following codes, to rename the `.pyy` files back to `.py` -->
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

<py-script src="./operations.pyy">
</py-script>
```

The above codes are used to check every file with the extension `.py` in the default working directory `/home/pyodide` in the virtual file system maintained by `pyscript`, and then rename them back to `.py`. This will allow python to find files with the `.py` extension and load them as modules. Now we refresh the web page, everything should work perfectly.

##### 8.2 About the virtual file system maintained by `pyscript`

In fact, every time we refresh the web page, `pyscript` will create a Linux-like virtual file system inside the sandbox folder that the web browser has assigned to this web page. For example, if we run the following Python scripts within a `<py-script>` tag:

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

The output will be as follows:

```bash
Pwd: /home/pyodide

tmp
home
dev
proc
lib
```

Each of the folders has its special use case through `pyscript`. This virtual file system actually gives us a lot of freedom to do whatever cool things we want, e.g. download a zip file and extract it, upload some created files to our server, download a song and play it, download a movie and process it, etc. By default, all files declared in the `<py-config>` tag are downloaded and placed in the `home/pyodide/` folder.

#### 9. Use a zip file to pack all the Python files (and other resources) on the server.

Sometimes, you may need to load a lot of Python files from your server or other servers, e.g., 

```html
<py-config>
    packages = ["numpy", "matplotlib", "bokeh", "xyzservices", "pandas"]

    [[fetch]]
    from = "http://localhost:8000/"
    files = ["f1.py", "f2.py", "f3.py", ..., "f100.py"]
</py-config>
```

In this case, you will have to include many python files in the `files` list under `[[fetch]]`  of  `<py-config>`, which is quite repetitive and dull. 

To reduce pointless repetition, we can put all these python files into a zip file, then have `pyscript` automatically download them, and finally unzip this zip file so that these files can be loaded as modules by python.

Let's say we put all these Python files `f1.py`, `f2.py`, `f3.py`, ..., `f100.py`, etc, in a folder called `python_files` and zip this folder as `python_files.zip`. To make the example easier, we can just add very simple code to these python files, for example, for `f1.py` we write the following code:

```python
def test1():
    print("test1 function works!")
```

Now in the `<py-config>` tag, we write as the follows:

```html
<py-config>
    packages = ["numpy", "matplotlib", "bokeh", "xyzservices", "pandas"]
    
    [[fetch]]
    files = ["./test_pyscript.py"]

    [[fetch]]
    from = "http://localhost:8000/python_files.zip"
    to_folder = "/home/Downloads/"
    to_file = "python_files.zip"
</py-config>
```

Within the last `fetch` part, `from` means the url address of the zip file, which can be on your server or on other servers, e.g. GitHub; `to_folder` means into which folder of the virtual file system of `pyscript` you want to download this zip file, here we make it `/home/Downloads/`; `to_file` means the name for the downloaded zip file, here in our case we make it the same as its original name.

Now let's refresh our web page, in the web page's`Console` we will see a message like `[pyscript/main] fetching path: http://localhost:8000/python_files.zip`, which means that the `pyscript` is downloading the zip file.

Afterwards, we have to unpack the downloaded zip file into the current working dir of `pyscript`, i.e., `home/pyodide/`. We can use the native `zipfile` package of python to do this.

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

Now we can add a small `<py-script>` tag to test if it works:

```html
<!-- Remember: must add this part after the above `<py-script>` part -->
<py-script>
    from python_files.f1 import test1

    test1()
</py-script>
```

If we refresh the web page, after everything is loaded in few seconds, we will see a message `"test1 function works!"` being printed out in a black area at the bottom of the web page.

<img width="1056" alt="Screen Shot 2023-05-05 at 6 11 16 PM" src="https://user-images.githubusercontent.com/47345588/236535351-949d8c2b-03ba-46bd-b0a0-9c5c5d3872f9.png">

Now everything works fine in this way to load Python files. Surely this can be applied to other resources such as an image file, an audio file or any other formatted file.

#### 10. Little things to make your `pyscript` web page nicer

##### 10.1 Remove the black area at the bottom of the web page

As long as you use Python's `print` function inside the `<py-script>` tag, a black area containing all the printed messages will be displayed at the bottom of the web page. So when you publish your web page in production, remember to comment out or delete all lines of `print(...)` code.

##### 10.2 Remove the blank space at the bottom of the web page

In some cases (not always), when you use the `<py-script>` tag, an empty white area will appear at the bottom of your web page. This issue doesn't really affect the beauty of your web page. However, if you are a perfectionist and really want to remove it, simply add a `style` property to each `<py-script>` like the following to ensure that the `<py-script>` tag does not take up any extra space:

```html
<py-script style="height: 0;">
    # your python codes
</py-script>
```



### Conclusion

Through the above procedures, we have demonstrated the potential of `pyscript` and proved the usability of this intelligent tool for our daily scientific work. The `pyscript` framework is a very creative and avant-garde project that allows us to implement complex functions within a web page, taking advantage of python's countless & super powerful packages, as well as the convenience of html pages since we have web browsers on every laptop. For scientists, `pyscript` can significantly increase their efficiency in using Python for scientific data analysis.
