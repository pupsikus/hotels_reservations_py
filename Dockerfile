FROM python:3
ADD . /code
WORKDIR /code
#ENV PATH=$PATH:/code
#ENV PYTHONPATH /code
RUN pip install -r requirements.txt
CMD [ "python", "-m", "unittest", "tests/test_reservations.py" ]