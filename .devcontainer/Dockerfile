FROM ubuntu:20.04

ENV TZ=Australia/Melbourne

RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update -y && apt-get install sudo -y

RUN DEBIAN_FRONTEND=noninteractive \
    && sudo apt-get install software-properties-common -y \
    && sudo apt-get install tzdata -y \
    && sudo ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && sudo apt-get update -y \
    && sudo apt-get dist-upgrade -y \
    && sudo apt-get install awscli -y \
    && sudo apt-get install git -y \
    && sudo apt-get install npm -y \
    && sudo apt-get install python3.8 -y \
    && sudo apt-get install python3-pip -y \
    && sudo apt-get install python3-venv -y \
    && sudo npm install -g npm@latest \
    && sudo npm install -g aws-cdk \
    && python3 -m pip install --upgrade pip

EXPOSE 10004