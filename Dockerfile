FROM python:slim-bullseye

RUN useradd runuser -d /home/runuser && mkdir -p /home/runuser/code && chown -R runuser:runuser /home/runuser
COPY requirements.txt /tmp/requirements.txt
RUN pip install -U pip && pip install -r /tmp/requirements.txt && rm -f /tmp/requirements.txt
USER runuser
COPY static /home/runuser/code/static
COPY templates /home/runuser/code/templates
COPY link_shortener /home/runuser/code/link_shortener

WORKDIR /home/runuser/code