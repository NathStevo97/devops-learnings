# 8.0 - Advanced Topics

## 11.1 - Advanced Topics

### Preparing Windows Server

- Ansible Control Machines can ONLY be Linux Machines
- This does not mean that Windows cannot be targets of Ansible
- Ansible can still connect to a Windows host by WinRM
- To allow this, the follwing requirements must be met on the control machine:
  - pywinrm module installed - pip instlal "pywinrm≥0.2.2"
  - Setup WinRM - example scripts available online e.g. ConfigureRemotingForAnsible.ps1
  - Use / Configure other methods of authentication e.g. Basic / Certificate / Kerberos
- Additional information available in the Windows Support section of the Ansible documentation.

---

### Ansible-Galaxy

- A free site for sharing and rating community-developed Ansible Roles
- You are free to download any existing roles via the ansible-galaxy CLI to integrate them into projects.

---

### Patterns

- Have previously seen only [Localhost](http://Localhost) as the target host for playbooks
- Alternative options are available:
  - Host1, Host2, Host3
  - Group1, Host1 (where host1 isn't part of group1)
  - Host*
  - *company.com
- Additional options are available via the Ansible documentation.

---

### Dynamic Inventory

- It's not always necessary to define information in inventory files
- If the project was to be integrated to a new environment, the inventory file would have to change completely.
- To overcome this, one can make an inventory Dynamic
  - Instead of specifying the inventory.txt, you would specify a script called inventory.py
  - [Inventory.py](http://Inventory.py) reaches out to whatever sources are defined and returns their associated information

[https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html](https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html)

---

### Developing Custom Modules

- Modules already exist to perform specific actions like the user, file, etc.
- All of these are python modules
- Custom modules can be developed by building a python script in a particular format.
- Further information is available in the Ansible Documentation

---

## 11.2 - Project Introduction

### Project Introduction

- Project Aim: Use Ansible to automate the provisioning of the Kodekloud Store
  - LAMP Stack Application (Linux - Apache - MySQL - PHP)
- Note: MariaDB will be used instead of MySQL
- Need to understand what we actually want to achieve.
- System:
  - CentOS / Linux target machines
    - Need to ensure Firewall is configured appropriately or installed if not there
  - Apache HTTPD Server needs to be installed:
    - install httpd
    - configure httpd
    - configure Firewall to allow httpd
    - Start httpd service
  - MariaDB needs to be set up and configured
    - Install MariaDB
    - Configure MariaDB
    - Start MariaDB
    - Configure Firewall
    - Configure Database
    - Load data
  - PHP
    - Install PHP
    - Configure Code
  - Configure any other system requirements
- For ease with the project, the steps will go:
  - Install firewall (system)
  - Install and setup MariaDB
  - Install and Setup Apache HTTPD Server
  - Download PHP Code and Run/Test it

---

### Firewall

```bash
sudo yum install firewalld # install firewalld package
sudo service firewalld start # start firewalld service
sudo systemctl enable firewalld # enable the firewalld service
```

### MariaDB

```bash
sudo yum install mariadb-server
sudo vi /etc/my.cnf # configure file with right port
sudo service mariadb start
sudo systemctl enable mariadb
## enable mariadb via firewall
sudo firewall-cmd --permanent --zone=public --add-port=3306/tcp
sudo firewall-cmd --reload
## Configure the DB and setup user(s)
mysql
MariaDB > CREATE DATABASE ecomdb;
MariaDB > CREATE USER 'ecomuser'@'localhost' IDENTIFIED BY 'ecompassword';
MariaDB > GRANT ALL PRIVILEGES ON *.* TO 'ecomuser'@'localhost';
MariaDB > FLUSH PRIVILEGES;
mysql < db-load-script.sql
```

---

### Apache

```bash
sudo yum install -y httpd php php-mysql
sudo firewall-cmd --permanent --zone=public --add-port=80/tcp
sudo firewall-cmd --reload

sudo vi /etc/httpd/conf/httpd.conf
## configures DirectoryIndex to use index.php instead of index.html

sudo service httpd start
sudo systemctl enable httpd
```

### Code

```bash
sudo yum install -y git
git clone https://github.com/application.git /var/www/html
##update index.php to use the right database address, name and credentials
curl http:://localhost # test code
```

---

### Setup Variations

- Could just run all of the above on a single node, however in practice, one would have a DB server and a web server.
  - The MariaDB instructions are to be carried out on one target
  - Apache and PHP-related operations on another
  - Firewall operations will need to be ran on both
- In a multi-node setup, the index.php file needs to be configured a bit differently
  - On the web server, configure with the IP address of the DB server
  - On the DB server, supply the IP Address of the web server to ensure it is given sufficient permissions in the MariaDB commands
- As far as the code goes, the only modification will be to index.php at around line 107 as this contains details regarding the MariaDB connection
- Repo link kodekloudhub/learning-app-ecommerce
