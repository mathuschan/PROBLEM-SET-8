# Running Django Dockerfile

In your developer console or terminal, navigate to this directory containing the Dockerfile.

1. Build image that is able to run the project.

```
docker build . -t my_docker_image
```

2. Run image.

```
docker run --detach --publish 8000:8000 my_docker_image
```

  * `--detach` makes it run in the background and only shows you the id of the current process it started.
  * `--publish` allows us to reach port 8000 inside the docker the container from outside.

3. List running images

```
docker ps

# CONTAINER ID   IMAGE             COMMAND                \
# 1473df75c2a8   my_docker_image   "python3 manage.py r…" \

# CREATED          STATUS          PORTS     NAMES
# 54 seconds ago   Up 53 seconds             festive_kirch
```

4. Stop an image.

```
docker stop 14
```

(only the first few characters of the image suffices)

5. Delete container.

```
docker rm 14
```

(again, first few characters suffice)

6. Delete image (if necessary).

```
docker rmi my_docker_image
```
