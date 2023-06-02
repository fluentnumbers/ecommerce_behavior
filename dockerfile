FROM  prefecthq/prefect:2.10.11-python3.10

COPY ./requirements.txt .
COPY ./.prefectignore .

# RUN pip install --upgrade pip
RUN pip install -r  requirements.txt