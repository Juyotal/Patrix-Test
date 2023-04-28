# Patrix-Test (F1 API)
A little middleware API that converts xml data from a call to Formula 1 racing results endpoint and transforms it to json data before returning.


# Installation and SetUp
1. Make sure your system has Python Installed. 
    you can enter do so from python installer  [Python.org](https://www.python.org/downloads/) 
    here you have access to different versions corresponding to your os system

    After installation, run a verification by entering in your terminal `$ python3 --version` 

2. After python is correctly installed, Install virtualenv on your system using command `pip3 install virtualenv`
    and then, In the app root folder, open the terminal run the command ` python<version> -m venv <virtual-environment-name>` this commads setsup virtual environment to your working directory and to activate, run `source env/bin/activate` in case of unix or `env/Scripts/activate.bat` in case of a windows system

3. with virtualenv activated, install the dependencies 
    `pip3 install -r requirements.txt`

4. Now you can run the api server on your local host with the command
    `python3 api/server.py` This will deploy your app to the port `5000` of your localhost

5. To kill the server, Press `Ctrl + C` for Windows OS or `cmd + C` for OSX in terminal
    Also, you can exit your virtual environment instance by typing in terminal `deactivate`

# Usage
## Endpoints.
Once our server is running, our api can only be accessed via 1 endpoint. `GET /api/<year>/<round>`

### Parameters
Our endpoint url takes in *2 parameters*: the year, which must be an integer value and within the range `(1950 <= year >= present)` and the round which is equally a `positive interger`.

### Response 
The Output Response is a Json representing the Race Tournament result for the Specific year and the Specific Round.

In your Browser, or with help of API Playground like Postman, make a call to url of the form following the example below http://127.0.0.1:5000/api/2000/3

# Testing.
Run tests to the API by running in terminal the command `pytest tests/api_tests.py -vv`
and new Tests can be added to the Tests Directory.

# Swagger UI
[Swagger UI](http://127.0.0.1:5000/api/) will give you a detailed view of the endpoints available to the API and you can run requests here aswell.