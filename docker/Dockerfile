FROM python:3.5-alpine

ENV DEST_ROOT_PATH /comics/

RUN apk update && apk add git
RUN git clone https://github.com/nocsagnauj/get_comics.git &&\
    mkdir $DEST_ROOT_PATH

VOLUME "$DEST_ROOT_PATH"

CMD ["python3","/get_comics/comics.py"]