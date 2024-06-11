project_path="~/project/toyllm"
env_name="toyllm"

model_group="Qwen"
model__name="Qwen2-7B-Instruct"

model_id="$model_group/$model__name"
model_path="~/data/$model_group/$model__name"

quan_type="int8"
device="CPU"

cd $project_path
source ~/.bashrc
eval "$(conda shell.$(basename $SHELL) hook)"
conda activate $env_name

which python

# export
echo "  -- [START] Export model $model_id ($model_path) with quantization $quan_type on device $device"
python export.py \
    -m $model_id \
    -w $model_path \
    -q $quan_type \
    -d $device
