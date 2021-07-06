# set base image (host OS)
FROM nginx
FROM python:3.8
ADD  . /demo_code
WORKDIR /demo_code
RUN pip install -r requirements.txt
CMD [ "python", "ICAV_assignment.py" ]