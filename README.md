# get_comics
Download comics' images from gocomics.com

Last version gets the parameters as environnement variables or from config file
The config file is organized as:
\[SECTION1\]
KEY1 = value
KEY2 = value

\[SECTION2\]
KEY3 = value
KEY4 = value
(...)

The environnement variables must have the format: SECTION_KEY="value"


## comics.ini
This is the configuration file to list:

- The destination directory
- The chosen comics
- Start and End dates
- The ending url for each comic

The chosen comics must have their own category fields

\[COMIC_NAME\]
COMIC\_URL\_NAME = ${DEFAULT:SITE\_PATH}/internet\_comic\_name/

Comics.py now manages the exceptions when:
- variable not found in the environnement
- section or key not found

## docker/Dockerfile
There is a Dockerfile to dockerize the application

Usage:
- Download the docker/Dockerfile
- Build and run the docker
- If you specify the volume bind, the local host directory has to be created before running the docker
- You can pass environnement variables with the '-e' option
\# docker build -t comics:test .
\# docker run -it -v /tmp/comics:/tmp/comics_strips --name comics comics:test

The docker creates an internal volume on '/tmp/comics_strips' where it is supposed to save the comics' strips.

This directory is stored in the environnement variable DEFAULT\_DEST\_ROOT\_PATH so it overrides the content in the comics.ini file
