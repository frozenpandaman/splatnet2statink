FROM python:3-stretch

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "splatnet2statink.py", "-M" ]