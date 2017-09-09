# Fortune lists grabber

I used Python 3.6 with anaconda(updated). I have also updated the files in the output folder.

## Previous ilyavorobiev/fortune-grabber info :
## Description
In this repository you can find scripts for obtaining [Fortune 1000](http://fortune.com/fortune500/) and [Global 500](http://fortune.com/global500/) companies lists and their data outputs. Scripts downloading and parsing information from the official site.

## Installation
 You should have Python 2.7 installed. In folder with cloned repository please run:
 
 ```terminal
 -sudo pip install virtualenv
 
 virtualenv env
 source env/bin/activate
 
 pip install -r requirements.txt
 ```
 
 This will install [virtaulenv](https://virtualenv.readthedocs.org) and all required libraries.
 
 ## Usage
 Don't forget to activate virtualenv if it isn't already done. To do that run:
 ```terminal
 source env/bin/activate
 ```
 
 To obtain Fortune 1000 companies list please run the following. This will generate csv file in output folder.
 ```terminal
 python fortune1000.py
 ```
 
 To obtain Global 500 companies list please run the following. This will generate csv file in output folder.
 ```terminal
 python global500.py
 ```
 
 ## Prepared data
 In this repository in [output folder](/output) you can find data that the scripts generate. It can be useful if you are looking only for data. 

