FROM python:3.5-alpine

ENV DEST_ROOT_PATH /tmp/comics/

RUN apk update && apk add git
RUN git clone -b develop https://github.com/nocsagnauj/get_comics.git &&\
    mkdir $DEST_ROOT_PATH

VOLUME "$DEST_ROOT_PATH"

WORKDIR /get_comics
CMD ["python3","./comics.py"]