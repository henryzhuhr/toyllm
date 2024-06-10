$project_path="$env:USERPROFILE/project/toyllm"
$env_name="toyllm"

$model_group="Qwen"
$model__name="Qwen2-0.5B-Instruct"

$model_id="$model_group/$model__name"
$model_path="$env:USERPROFILE/data/$model_group/$model__name"

$quan_type="int8"
$device="CPU"

cd $project_path
conda activate $env_name

# export
python export.py `
    -m $model_id `
    -w $model_path `
    -q $quan_type `
    -d $device

# infer
python infer-chat.py `
    -m $model_id `
    -p weights/$model_id-IR-$quan_type `
    -q $quan_type `
    -d $device `
    -l 1024

