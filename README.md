# Linux Server Configuration for the Item Catalog Project

This repository contains code for an application that provides a catalog of books as well as a user registration and authentication system. Registered users will have the ability to post, edit and delete their own book categories and books.

## Setup

This project uses Amazon Lightsail to host the server for the Item Catalog project referenced above.

I first created a server instance using my Amazon Web Services account with Amazon Lightsail (using a Linux/Unix platform, and the cheapest plan level).

I then downloaded the Default Private Key to ssh into my server, and saved it in the .ssh folder in my local home folder and secured the key with "chmod 600".

I used Terminal to access the server with "ssh -i ~/.ssh/lightsail_key.rsa ubuntu@34.212.220.165".

I then installed the newest updates with the commands:

sudo apt-get update
sudo apt-get upgrade

To change the port number, I used `sudo nano /etc/ssh/sshd_config` and updated the port number to 2200.

I configured the firewall settings and then enabled it with sudo ufw enable.

In the Lightsail interface, under the Manage tab, I configured the settings to allow ports 80(TCP), 123(UDP), and 2200(TCP), and deny the default port 22.

Logged back in as ubuntu and created the grader user, and gave it sudo privileges.

Then, I created a new ssh key pair for the user grader, and added it to my .ssh file.

I installed Apache2 and mod_WSGI and then installed and configured PostgreSQL.

using sudo nano, I edited my files to reflect the change from sqlite to PostgreSQL.

I then had to log into my Google Developer Console and add the ip adress and the xip.io domain to my project.

Then, i installed all dependencies, and set up my Flask application.

I then ran database_setup.py, then populate_db.py, and finally __init__.py (formerly application.py).


### Using the Project

The website can be accessed at http://34.212.220.165/ (or http://34.212.220.165.xip.io/).

One can log in to the server with ssh -p 2200 -i ~/.ssh/grader_key.pub grader@34.212.220.165.

### Known Errors

- Not all the functions of the Item Catalog project are available on this server project and are being worked on.
