# Openpointcloudmap

Vario-Scale point cloud integration

## Team

- Weiran Li
- Brenda Olsen
- Jippe van der Maaden
- Marc-Julien Veenendaal
- Tom Hemmes

## Support

- TU Delft
- Fugro Geoservices

## Credits

- Django<br>
https://github.com/django/django

- PostgreSQL PostGIS<br>
https://github.com/postgis/postgis

- Laspy<br>
https://github.com/laspy/laspy

- Scipy (spatial)<br>
https://github.com/scipy/scipy/tree/master/scipy/spatial

- ThreeGeoJSON<br>
https://github.com/jdomingu/ThreeGeoJSON

- ProjectPointless<br>
https://github.com/ivodeliefde/ProjectPointless

- three.js<br>
https://github.com/mrdoob/three.js/

## Introduction

The aim of this project is to provide methods to realise the OpenPointcloudMap proposed by Fugro and TU Delft. This idea entails a platform to which anyone could contribute by uploading any point cloud data set, much like OpenStreetMap is for 2D vector maps.

The process of enabling contributors to upload data, integrating these data sets, visualising and redistributing, involves many challenges. Among them, our group focuses on handling different scales and granularity of point clouds from different scanners and environments. Solving this challenge will enable appealing visualisation, usability for low and high computation powers and geometrical consistency for analysis. These are the aspects we think are needed to create a platform that will be engaging for a community of users and contributors.

## Start using

- Install Django, psycopg2 and laspy
- Open Version2_2/Version2_2/settings.py and configure the name and password of the database
- Open uploadModule and do the same configuration in line 52
- In command line, change directory to Version2_2 (the first folder, with manage.py in it), run the following:<br>
$ python manage.py migrate<br>
$ python manage.py runserver
- Go to browser, localhost:8000/grind
- Feel free to make changes, but if the models.py is changed, please remember to run the following command lines:<br>
$ python manage.py makemigrations<br>
$ python manage.py migrate
- The random importance array can be replaced by importance.py and ptred.py, which are both in grind folder
