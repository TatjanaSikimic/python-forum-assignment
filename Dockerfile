FROM python:3.10.6
#-alpine3.16


WORKDIR /python-forum-assignment

COPY . /python-forum-assignment


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


# command to run on container start
CMD ["python", "main.py"]
#lastly we specified the entry command this line is simply running python ./main.py in our container terminal