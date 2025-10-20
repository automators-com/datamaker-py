FROM python:3.13-slim

# install git
RUN apt-get update && apt-get install -y git

# update pip
RUN pip install --upgrade pip

# Install datamaker from github
RUN pip install git+https://github.com/automators-com/datamaker-py.git

# Install dependencies
RUN pip install requests pandas

# set env to prevent pip upgrade prompts
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

CMD ["python3"]