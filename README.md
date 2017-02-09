# get_comics
Download comics' images from gocomics.com

***TO DO***: get the parameters as environnement variables


## comics.ini
This is the configuration file to list:

- The destination directory
- The chosen comics

Later, the **comics.py** script will take into account the start and end dates

The chosen comics must have their own category fields

\[COMIC_NAME\]
COMIC\_URL\_NAME = ${DEFAULT:SITE\_PATH}/internet\_comic\_name/

I have not (yet) coded the exception raise when the category is not found


## docker/Dockerfile
There is a Dockerfile to dockerize the application

Usage:
- Download the docker/Dockerfile
- Build and run the docker
- If you specify the volume bind, the local host directory has to be created before running the docker
\# docker build -t comics:test .
\# docker run -it -v /tmp/comics:/tmp/comics_strips --name comics comics:test

The docker creates an internal volume on '/tmp/comics_strips' where it is supposed to save the comics' strips.

This directory has to be the same as in comics.ini

Later on, when the comics.py will read the environnement variables, 
the destination directory in comics.ini would not be useful anymore
