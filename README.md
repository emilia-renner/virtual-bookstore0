# Item Catalog

This repository contains code for an application that provides a catalog of books as well as a user registration and authentication system. Registered users will have the ability to post, edit and delete their own book categories and books.


## Getting Started

This project uses the Flask framework to run a web server in Python that will allow user to view existing categories and books in a database as well as add their own.

### Prerequisites

In order for the files in this repository to work, you will need a terminal, such as Git Bash, a virtual machine, and a version of Python.

### Installing

Git Bash can be downloaded and installed from the [Git Bash website](https://git-for-windows.github.io/).

The virtual machine can be accessed using [Virtual Box](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/downloads.html).

If you do not have Python installed on your computer, the most recent version can be downloaded from the [Downloads page on the Python Software Foundation website](https://www.python.org/downloads/). My code is written in Python 3.

Once these steps have been completed, the repository should be downloaded and saved in the shared vagrant directory.

### Running the Files

The first thing that needs to be done is loading the data into the virtual machine.  To do that, first log into the virtual machine using **vagrant ssh**.  After logging in, cd into the **/vagrant** shared directory.  Once the virtual machine is up and running, the initial database needs to be created.  First, cd into the **/catalog** folder. Then run **python3 database_setup.py** and then **python3 populate_db.py** to populate the database with some initial data.  Once these steps are complete, the web server can be launched by entering **python3 application.py** and navigating to http://localhost:8000.  From there, the existing data can be viewed, or the user can log in to add new data.

### Known Errors

- When editing a book, a user must edit the book name or create a new book name in order to edit additional information. The fix for this is being worked on.