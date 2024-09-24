$TAG = Get-Date -Format 'yyyy-MMdd-HHMMSS'
$TAG = "latest"
$IMAGE_TAG = "toyllm:$($TAG)"

docker build . -t $IMAGE_TAG -f dockerfiles\Dockerfile --no-cache --progress=plain

docker run -it --rm $IMAGE_TAG /bin/bash