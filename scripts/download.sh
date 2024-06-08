git lfs install
modelid_list=(
    Qwen/Qwen2-0.5B
    Qwen/Qwen2-0.5B-Instruct
    Qwen/Qwen2-1.5B
    Qwen/Qwen2-1.5B-Instruct
    Qwen/Qwen2-7B
    # Qwen/Qwen2-7B-Instruct
)

for mi in "${modelid_list[@]}"; do
    git clone https://huggingface.co/$mi .cache/$mi
done