# install pytorch according to the CUDA version
if [ ! -z "${CUDA_VERSION}" ]; then
    python3 -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu$(echo $CUDA_VERSION | tr -d '.')
else
    python3 -m pip install torch torchvision
    echo "CUDA_VERSION is not set. Installing CPU version of PyTorch."
fi
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt


# freeze the requirements 
# python3 -m pip list --format=freeze > requirements.version.txt