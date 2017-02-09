FROM python:3.5-alpine

ENV DEST_ROOT_PATH /tmp/comics_strips/
ENV CLONE_PATH /comics_app
ENV DEBIAN_FRONTEND noninteractive

RUN apk update && apk add git
<<<<<<< HEAD
RUN git clone https://github.com/nocsagnauj/get_comics.git &&\
    mkdir $DEST_ROOT_PATH

VOLUME "$DEST_ROOT_PATH"

WORKDIR /get_comics
CMD ["python3","./comics.py"]
=======
RUN git clone -b develop https://github.com/nocsagnauj/get_comics.git "$CLONE_PATH" &&\
    pip install -r $CLONE_PATH/requirements.txt &&\
    mkdir -p $DEST_ROOT_PATH

VOLUME "$DEST_ROOT_PATH"

WORKDIR "$CLONE_PATH"
CMD ["python3","./comics.py"]
>>>>>>> develop
