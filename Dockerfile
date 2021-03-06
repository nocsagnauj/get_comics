FROM python:3.5-alpine

ENV DEFAULT_DEST_ROOT_PATH /tmp/comics_strips/
ENV CLONE_PATH /comics_app
ENV DEBIAN_FRONTEND noninteractive

RUN apk update && apk add git &&\
    git clone https://github.com/nocsagnauj/get_comics.git "$CLONE_PATH" &&\
    pip install -r $CLONE_PATH/requirements.txt &&\
    mkdir -p $DEFAULT_DEST_ROOT_PATH

VOLUME "$DEFAULT_DEST_ROOT_PATH"

WORKDIR "$CLONE_PATH"
CMD ["python3","./comics.py"]