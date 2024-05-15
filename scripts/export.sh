source .env/toyllm.venv/bin/activate

model_list=(
    Qwen/Qwen1.5-0.5b-Chat
    Qwen/Qwen1.5-1.8B-Chat
    Qwen/Qwen1.5-4b-Chat
    Qwen/Qwen1.5-7B-Chat
)

for model_id in "${model_list[@]}"; do
    python export.py --model_id $model_id --quan_type int4
    python export.py --model_id $model_id --quan_type int8
done