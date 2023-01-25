FROM python:3

# Setup env
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Setup App
RUN mkdir -p /Flask_App

COPY . /Flask_App

WORKDIR /Flask_App

EXPOSE 5001

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]