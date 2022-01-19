FROM python:3.9.5

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

RUN chmod u+x ./boot.sh
ENTRYPOINT ["./boot.sh"]