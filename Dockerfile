FROM ubuntu:20.04 
USER root 
RUN apt update 
RUN apt install -y curl 
RUN apt install -y python3.9 
RUN apt install -y python3.9-distutils 
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 
RUN python3.9 get-pip.py 
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"   
#RUN unzip awscliv2.zip 
#RUN ./aws/install 
#RUN ["apt-get", "install", "-y", "vim"] 
RUN apt-get install -y git 
RUN pip install dbt-core
USER root 
WORKDIR /app 
COPY dbt . 
RUN mkdir .dbt/ 
COPY ./dbt/profiles.yml .dbt/profiles.yml 
COPY ./dbt/dbt_project.yml dbt_project.yml 
#CMD ["/usr/local/bin/dbt","debug"] 

 
