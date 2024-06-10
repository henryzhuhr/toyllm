git lfs install

download_from="https://www.modelscope.cn"

local_dir=downloads

model_group=(
    Qwen
)

modelid_list=(
    Qwen/Qwen2-0.5B
    Qwen/Qwen2-0.5B-Instruct
    Qwen/Qwen2-1.5B
    Qwen/Qwen2-1.5B-Instruct
    Qwen/Qwen2-7B
    Qwen/Qwen2-7B-Instruct
)

for mi in "${modelid_list[@]}"; do
    git clone $download_from/${mi}.git $HOME/data/$mi
done


if [ ! -d $local_dir ]; then
    mkdir -p $local_dir
fi

for mg in "${model_group[@]}"; do
    ln -s $HOME/data/$mg $local_dir/$mg
done
