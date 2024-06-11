git lfs install

download_from="https://www.modelscope.cn"
modelid_list=(
    Qwen/Qwen2-0.5B
    Qwen/Qwen2-0.5B-Instruct
    Qwen/Qwen2-1.5B
    Qwen/Qwen2-1.5B-Instruct
    Qwen/Qwen2-7B
    Qwen/Qwen2-7B-Instruct
    Qwen/Qwen2-72B
    Qwen/Qwen2-72B-Instruct
)

for mi in "${modelid_list[@]}"; do
    git clone $download_from/${mi}.git ~/data/$mi
done