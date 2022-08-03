FROM python:3.8-slim-buster

WORKDIR /
COPY test_harness_flows.py .
RUN pip install pytest
RUN pip install selenium
CMD [ "python3","/test_harness_flows.py" ]