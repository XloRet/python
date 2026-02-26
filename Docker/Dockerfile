FROM python:3.11
WORKDIR /myprog 
RUN pip install --no-cache-dir googletrans==3.1.0a0
ADD . . 
CMD [ "python", "main.py" ]