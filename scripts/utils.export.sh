echo "Run in Python: $(which python)"

local_dir=~/data

model_list=(
    Qwen/Qwen2-0.5B
    Qwen/Qwen2-0.5B-Instruct
    Qwen/Qwen2-1.5B
    Qwen/Qwen2-1.5B-Instruct
    Qwen/Qwen2-7B
)

quan_type=(
    fp16
    int8
    int4
)

for mi in "${model_list[@]}"; do
    for qt in "${quan_type[@]}"; do
        echo "Run: 'python export.py -m $mi -q $qt'"
        python export.py \
            -m $mi \
            -w $local_dir/$mi \
            -q $qt
    done
done