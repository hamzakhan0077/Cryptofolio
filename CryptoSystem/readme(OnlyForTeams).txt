
Steps to Initiate the project

1. Copy this in your PycharmProject Directory in C://
2. Create a virtual environment in this VinylShop Directory here --> C:\Users\Hammozi\PycharmProjects\VinylShop>
(NOT INSIDE THE VinylShop Directory that is Inside)

3. To create a virtual environment simply -- > run command  --- > python -m venv vinylvenv
Note vinylvenv  can be a different name as well .

4. Once you are successfull in creating the venv then cd into vinylvenv/Scripts -
then simply type in --  activate.bat.

5. your virtual environment is now up and running --

6. Install everything in the requirements.txt to do so simply cd back into top directory (VinylShop)
this is where requirements.txt is

7. run --> pip install -r requirements.txt

8. now you are ready to launch the server , symply call python run.py



----------------------------------------------------------------

In the templates I fixed as many urls as possible however-

Look how to use template inheritance
 See
 https://flask.palletsprojects.com/en/2.0.x/patterns/templateinheritance/

Consider Template B is inheriting from template A


-- Template A -- (Main template that all other are inheriting from)
<html>
all shit header naves and shit thjat are suppose to be there in others blah blah blah

{% block someDifferentHtml %} {% endblock %}


In template B
{% extends template A %}

{% block someDifferentHtml  %}
 <P>
    SOME STUFF FROM db MAYBE etc etc
 </P>

{% endblock someDifferentHtml%}

<html>

note those % has to be there exactly where they are otherwise it wont work

---------------------------------

URL FOR


in Html when referring to images, js,css,etc
all of these are in static folder

use
EG
href="{{ url_for('static', filename='styles/media-queries.css') }}"


For Links that are relative
<li><a href = "{{url_for('index')}}">Home</a></li>

where index is a html file
u dont need to mention html extension
_____________________



















----------------------------------------------------------------