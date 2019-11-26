# Project 2

Web Programming with Python and JavaScript

## Welcome to KuraKani

It is an online messaging service made using Flask, similar in spirit to **Slack**, aka _Flack_. Here, you can sign into your site with a display name, create channels (i.e. chatrooms) to communicate in, as well as see and join existing channels. Once a channel is selected, you will be able to send and receive messages with one another in real time. If your connection is lost due to some technical issue, then no problem, you can see the messages sent by your fellow chatmates in your absence. 

`application.py` is the Flask application.

`templates/` folder contains HTML5 jinja2 templates.

`static` contains JavaScript codes for the real time data transfer between client and server using websocket.

***
You can test or run this app by installing the requirements first by running:

`pip install -r requirements.txt`

**being on the directory containing `application.py`.**

Databases isn't used but session variables and localstorage is used.
