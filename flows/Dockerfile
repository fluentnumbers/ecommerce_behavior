FROM prefecthq/prefect:2.7.7-python3.9

COPY docker-requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir
RUN ls

# WORKDIR  /opt
COPY flows /opt/prefect/flows
RUN mkdir /opt/data/