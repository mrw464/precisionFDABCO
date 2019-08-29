FROM python:3.7-alpine
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /
WORKDIR . /
CMD ["BCO_Writer_Tool.py", "BCO_Conformance_Tool.py"]