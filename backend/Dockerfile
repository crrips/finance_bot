FROM python:3.11

WORKDIR /backend

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY . .

EXPOSE 8000

CMD ["/wait-for-it.sh", "db:5432", "--", "python", "src/main.py"]