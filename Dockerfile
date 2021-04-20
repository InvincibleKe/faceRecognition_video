FROM python:3.6
ADD requirements.txt /
RUN pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
ADD . /main_flask
WORKDIR /main_flask
EXPOSE 8080
CMD ["python", "main_flask.py"]