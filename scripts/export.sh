source scripts/create-python-env.venv.sh

print_info "Run in Python: $(which python)"


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
        print_success "Run: 'python export.py -m $mi -q $qt'"
        python export.py -m $mi -q $qt
    done
done