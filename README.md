# RIS
Radiology Information System for CMPUT 391

# Development Environment Installation Instructions

On the local machine (if necessary):
<code>$ easy_install pip</code>
<code>$ pip install virtualenv</code>


Pull the repo:
<code>$ git pull https://github.com/MarkGalloway/RIS/ ~/myLocation </code>
<code>$ cd ~/myLocation </code>


Create the isolated python evironment:
<code>$ mkdir ~/env</code>
<code>$ mkdir ~/env/RIS</code>
<code>$ virtualenv -p /usr/local/bin/python3.4 ~/env/RIS</code>
<code>$ source ~/env/RIS/bin/activate</code>
<code>(RIS) $ pip install -r requirements.txt </code>


Verify that packages have been installed:
<code>(RIS) $ yolk -l</code>
You should see something along the lines of...
Flask - 0.10.1
Jinja2 - 2.7.3
etc..


Test launching the local dev server:
<code>(RIS) $ python hello.py</code>
You should see a message saying that the server is running.
Navigate to http://127.0.0.1:5000/ and see if it displays.


Done working for the day?
Either close the terminal or deactivate virtual env
<code>$ deactivate</code>
