FROM python:3.7.4-slim
WORKDIR /home

RUN apt update
RUN apt-get install git -y
RUN apt-get install gnupg2 -y
RUN apt-get install wget -y
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' -y
RUN apt-get update
RUN apt-get install google-chrome-stable -y
RUN git clone https://github.com/RegionGroup/region_tarifs_parser.git
RUN cd region_tarifs_parser/ && pip install --no-cache-dir -r requirements.txt