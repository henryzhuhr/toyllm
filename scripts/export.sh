echo "Run in Python: $(which python)"
data_dir=~/data
model_list=(
    Qwen/Qwen2-0.5B
    Qwen/Qwen2-0.5B-Instruct
    Qwen/Qwen2-1.5B
    Qwen/Qwen2-1.5B-Instruct
    Qwen/Qwen2-7B
    Qwen/Qwen2-7B-Instruct
    Qwen/Qwen2-72B
    Qwen/Qwen2-72B-Instruct
)
quan_type=( fp16 int8 int4 )

for mi in "${model_list[@]}"; do
    for qt in "${quan_type[@]}"; do
        echo
        echo "  -- Run: 'python export.py -m $mi -q $qt'"
        echo
        python export.py \
            -m $mi \
            -w $data_dir/$mi \
            -q $qt
    done
done