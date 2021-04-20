FROM python:3.6
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD . /main_flask
WORKDIR /main_flask
EXPOSE 8080
CMD ["python", "main_flask.py"]