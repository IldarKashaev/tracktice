FROM ubuntu #Setting an original image Ubuntu
RUN apt-get update #Updating Ubuntu
RUN apt-get install python3 -y #Installing python3
RUN apt-get install python3-pip -y #Installing pip
RUN pip install Flask #Installing Flask
WORKDIR /app #Setting a workdir
COPY . /app #Copying prog to a folder
EXPOSE 5000 #Exposing a port
CMD ["python3", "-m", "flask", "--app", "main.py", "run", "--host=0.0.0.0"] #Running a prog
