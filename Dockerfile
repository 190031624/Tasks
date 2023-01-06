FROM python:3
EXPOSE 5000
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
CMD ["flask","run","--host","0.0.0.0"]