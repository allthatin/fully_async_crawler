FROM python:3.11.4

ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq && apt-get install -y \
    # std libs
    git curl vim wget bash-completion gettext \
       
    # redis
    && apt-get clean && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/* \
    && addgroup --system gustabo \
    && adduser --system --ingroup gustabo gustabo

WORKDIR /app

COPY ./deployments/crawler/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY --chown=gustabo:gustabo ./deployments/crawler/cmds/* /cmds/
RUN sed -i 's/\r$//g' /cmds/* \
    && chmod -R +x /cmds \
    && mkdir -p /var/log/ \
    && chown -R gustabo /cmds /var/log/

COPY --chown=gustabo:gustabo . .

USER root