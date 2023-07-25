**CREATING A DOCKER IMAGE WITH A COMMAND: **
*docker build . -t docker-flask* #Image has a name "docker-flask"

**RUNNING A CONTAINER ON A PORT 80 WITH FORWARDING FROM 5000 AND IMMEDIATELY DELETING WHEN CONTAINER STOPS**
*docker run -p 80:5000 -it --rm --name flask docker-flask*  #Container has a name "flask"
