FROM python:3.9

WORKDIR /app/

COPY requirements.txt /app/
COPY utils_functions.py /app/
COPY auto_browsing.py /app/
COPY __main__.py /app/

RUN pip install --upgrade pip  

RUN pip install -r requirements.txt

CMD ["python", "-u", "__main__.py"]