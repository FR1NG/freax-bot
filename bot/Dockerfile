FROM python:3.11.5-bullseye as dev

RUN rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY ./requirements.txt ./

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

RUN pip install --upgrade pip \
  && pip install -r requirements.txt

COPY ./deploy_tools/entry.sh /usr/local/bin/entry
RUN chmod +x /usr/local/bin/entry

EXPOSE 8000

ENTRYPOINT ["entry"]

CMD ["flask", "--app", "server", "--host=0.0.0.0" "--port=80"]






FROM python:3.11.5-bullseye as prod

RUN rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --upgrade pip\
&& pip install -r requirements.txt
RUN pip install gunicorn
COPY . .
COPY ./deploy_tools/entry.sh /usr/local/bin/entry
RUN mkdir -p /gunicorn
COPY ./deploy_tools/gunicorn.config.py /gunicorn/gunicorn.config.py

EXPOSE 8000
RUN chmod +x /usr/local/bin/entry
ENTRYPOINT ["entry"]
CMD ["gunicorn", "-c", "/gunicorn/gunicorn.config.py", "server:app"]
