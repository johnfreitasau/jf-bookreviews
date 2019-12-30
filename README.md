# Project 1 - JF Book Reviews

JF Book Reviews - A Web application using Python and JavaScript

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites


### Step1: Install virtual environment 
If you are using Python3 than you don't have to install virtual environment because it already come with venv module to create virtual environments.

If you are using Python 2, the venv module is not available. Instead, install virtualenv.

On Linux, virtualenv is provided by your package manager:

#### Debian, Ubuntu
$ sudo apt-get install python-virtualenv

#### CentOS, Fedora
$ sudo yum install python-virtualenv

#### If you are on Mac OS X or Windows, download get-pip.py, then:
$ sudo python2 Downloads/get-pip.py
$ sudo python2 -m pip install virtualenv

#### On Windows, as an administrator:
...\python.exe Downloads\get-pip.py
...\python.exe -m pip install virtualenv

### Step 2: Create an environment
Create a project folder and a venv folder within:

mkdir myproject

cd myproject

python3 -m venv venv

#### On Windows:
py -3 -m venv venv

#### If you needed to install virtualenv because you are on an older version of Python, use the following command instead:
virtualenv venv

#### On Windows:
...\virtualenv.exe venv
Activate the environment

Before you work on your project, activate the corresponding environment:
. venv/bin/activate

#### On Windows:
venv\Scripts\activate
Your shell prompt will change to show the name of the activated environment.

### Step 3: Install Flask
Within the activated environment, use the following command to install Flask:
$ pip install Flask


## Installing

TBA

## Authors / Contributing

* **John Freitas** - *Initial work* - [PurpleBooth](https://github.com/me50/johnfreitasau)
