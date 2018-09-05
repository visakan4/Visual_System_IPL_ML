# Project Description



# Technologies

### Languages: Python, JavaScript, HTML, CSS
### Libraries: ReactJS ,pandas, sklearn, NumPy, Flask, d3.js, Bootstrap
### Tools: Heroku, Git, PyCharm, Sublime Text

# Installation

### 1) Clone the repository
* Make sure git is installed locally
* To clone the repo: `git clone git@bitbucket.org:sd877278/vat_backend.git`

### 2) Prerequisites
#### 2.1) Windows Prerequisites
* `py -m pip --version`
* `py -m pip install --upgrade pip`
* `py -m pip install --user virtualenv`
* `py -m virtualenv env`
* `.\env\Scripts\activate`


#### 2.2) Mac/Unix Prerequisites
* `python3 -m pip --version`
* `python3 -m pip install --upgrade pip`
* `python3 -m pip install --user virtualenv`
* `python3 -m virtualenv env`
* `source env/bin/activate`


### 3) Start server

* Install project dependencies with this line : `pip install -r requirements.txt`
* Run this in termimal to start the backend server ` gunicorn index:app --log-file=-`



### 4) Test app
* In the browser, test the index route where the server is running
For example: If the server started on port 8000, then the root path `localhost:8000` should return the text "test index route"
