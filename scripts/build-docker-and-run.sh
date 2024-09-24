TAG=$(date +%Y-%m%d-%H%M%S)
TAG=latest
IMAGE_TAG="toyllm:$TAG"

ARG_NOCACHE="--no-cache"
# ARG_PROGRESS="--progress=plain"
# -- Multi-platform builds: https://docs.docker.com/build/building/multi-platform/
# ARG_PLATFORM="--platform=linux/amd64"
# ARG_PLATFORM="--platform=linux/arm64"
docker build \
    --tag $IMAGE_TAG \
    --file dockerfiles/Dockerfile \
    $ARG_NOCACHE $ARG_PROGRESS $ARG_PLATFORM .

USER_NAME=ubuntu
WORKDIR=/home/$USER_NAME/$(basename $PWD)
docker run -it --rm \
    -v $PWD:$WORKDIR \
    -w $WORKDIR \
    $IMAGE_TAG cat /etc/os-release
docker run -it --rm \
    -v $PWD:$WORKDIR \
    -w $WORKDIR \
    $IMAGE_TAG /bin/bash --login