# Public Version of TAQ-Query-Scripts
Included are the client side-scripts for access to the TAQ-Clickhouse Database remotely with Python.

Reccomended for advanced users only who are familiar with GitHub, Conda, and Linux

Instructions for access through the SQL UI DBeaver are included in Accessing the TAQ-Clickhouse Database PDF

### Local Setup
- Pull the repo 'TAQ-Query-Scripts-Public' from Github
- Setup the conda environment using the query_user_environment.yml file
- Create a directory called `data` in the root directory of the repo
- Create subdirectories called `raw_data` and `features` in the data directory of the repo
- Create an .env file in the root directory of the repo with the following variables:

```
    host="ppolak5.ams.stonybrook.edu."
    server_user= 
    server_password= 
    db_user= 
    db_pass=
```

Conda Tips
- `environment.yml` is a file that contains all the dependencies for the conda environment
    - Will have to update path name on this yml file
- `query_user_environment.yml` is a file that contains all the dependencies for the conda environment for the query user on the server

Feel free to create a directory for your own research called `personal_research` in the root directory of the repo. This directory is ignored by git and can be used to store your own scripts and data
        
**Do not republish, distribute or utilize the sample data found in this repo for any purposes other than academic research**
