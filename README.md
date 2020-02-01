# Hoshuko Library System

This can be deployed to a gunicorn docker image for 'production'.

In dev, run:

     python main.py

 If the SQLLite DB is not there, you can build it with

     flask db Migrate
     flask db upgrade
