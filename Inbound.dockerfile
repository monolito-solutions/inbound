FROM python:3.11

EXPOSE 6969/tcp

COPY requirements.txt /.
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]