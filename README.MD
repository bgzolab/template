# flask-tutorial 

All Code From: https://flask.palletsprojects.com/en/2.0.x/tutorial/

use this command to run app

```shell
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Some Notes

Okey, let's write something to against the memory.

- [ ] the `temlpate` couldn't write the comments, which means that
I have to write another. That sounds not good enough. And this the
url for that tutorial: https://flask.palletsprojects.com/en/2.0.x/tutorial/templates/

```html
<!doctype html>
<title>{% block title %}{% endblock %} - Flaskr</title>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<nav>
  <h1>Flaskr</h1>
  <ul>
    {% if g.user %}
      <li><span>{{ g.user['username'] }}</span>
      <li><a href="{{ url_for('auth.logout') }}">Log Out</a>
    {% else %}
      <li><a href="{{ url_for('auth.register') }}">Register</a>
      <li><a href="{{ url_for('auth.login') }}">Log In</a>
    {% endif %}
  </ul>
</nav>
<section class="content">
  <header>
    {% block header %}{% endblock %}
  </header>
  {% for message in get_flashed_messages() %}
    <div class="flash">{{ message }}</div>
  {% endfor %}
  {% block content %}{% endblock %}
</section>

<!-- 
    1. {% block title %} will change the title displayed in the browser’s tab and window title.
    2. {% block header %} is similar to title but will change the title displayed on the page.
    3. {% block content %} is where the content of each page goes, such as the login form or a blog post. 
    
    the {% block %} tags define blocks that child templates can fill in. All the block tag does is tell the template engine that a child template may override those placeholders in the template. block tags can be inside other blocks such as if, but they will always be executed regardless of if the if block is actually rendered.-->
```

```html
{% extends 'base.html' %}
<!-- {% extends 'base.html' %} tells Jinja that this template should replace the blocks from the base template. All the rendered content must appear inside {% block %} tags that override blocks from the base template. -->

{% block header %}
 <h1>{% block title %}Register{% endblock %}</h1>
{% endblock %}
<!-- A useful pattern used here is to place {% block title %} inside {% block header %}. This will set the title block and then output the value of it into the header block, so that both the window and page share the same title without writing it twice. -->

{% block content %}
 <form method="post">
   <label for="username">Username</label>
   <input name="username" id="username" required>
   <!-- The input tags are using the required attribute here. This tells the browser not to submit the form until those fields are filled in. If the user is using an older browser that doesn’t support that attribute, or if they are using something besides a browser to make requests, you still want to validate the data in the Flask view. It’s important to always fully validate the data on the server, even if the client does some validation as well. -->
   <label for="password">Password</label>
   <input type="password" name="password" id="password" required>
   <input type="submit" value="Register">
 </form>
{% endblock %}
```

- [X] `pytest` couldn't run when you not package it and install 
it. just like the issue said:

> Sounds like you didn't install the project (pip install -e .)
> and you're running from inside the tests directory.
> 
> I do know all steps complete successfully when followed in 
> order, so without information about the issue there's not 
> much I can do here. If you figure out what's going on and 
> think the tutorial can be clearer, please submit a PR for 
> review.
> from: https://github.com/pallets/flask/issues/2908

the result is following:

```shell
$ pytest
============================================= test session starts =============================================platform linux -- Python 3.8.5, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /mnt/c/Users/15517/OneDrive/codelib/ILDemos, configfile: setup.cfg
collected 0 items / 1 error

=================================================== ERRORS ====================================================________________________________________ ERROR collecting test session ________________________________________/usr/lib/python3.8/importlib/__init__.py:127: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
<frozen importlib._bootstrap>:1014: in _gcd_import
    ???
<frozen importlib._bootstrap>:991: in _find_and_load
    ???
<frozen importlib._bootstrap>:975: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:671: in _load_unlocked
    ???
/home/bgzocg/.local/lib/python3.8/site-packages/_pytest/assertion/rewrite.py:170: in exec_module
    exec(co, module.__dict__)
/mnt/c/Users/15517/OneDrive/codelib/ILDemos/flask-tutorial/test/conftest.py:5: in <module>
    ???
E   ModuleNotFoundError: No module named 'flaskr'
=========================================== short test summary info ===========================================ERROR .. - ModuleNotFoundError: No module named 'flaskr'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!============================================== 1 error in 0.24s ===============================================
```


## link

- If you intrested in *Test Coverage*, you could see: [zh] https://www.infoq.cn/article/test-coverage-rate-role.
  - In my perspective, the test mostly playing a role in checking for useless part of code. Is this part of code necessary really? And how to simplify the code and finding the more useful schema and thinking is crucial.