
cache_dir=.cache

modelid_list=(
    Qwen/Qwen2-0.5B
    Qwen/Qwen2-0.5B-Instruct
    Qwen/Qwen2-1.5B
    Qwen/Qwen2-1.5B-Instruct
    Qwen/Qwen2-7B
    # Qwen/Qwen2-7B-Instruct
)
possible_compressed_file_suffixes=(
    .tar.gz
    .tgz
    .tar.xz
    .txz
    .tar.bz2
    .tbz2
    .tar
    .zip
)

for modelid in "${modelid_list[@]}"; do
    if [ -d "$cache_dir/$modelid" ]; then
        echo "Weights for $modelid already exist."
    else
        found_compressed_file=false
        for suffix in "${possible_compressed_file_suffixes[@]}"; do
            compressed_file="$cache_dir/$modelid$suffix"
            if [ -f "$compressed_file" ]; then
                echo "Decompressing $compressed_file..."
                modelgroup=$(echo $modelid | cut -d'/' -f1)
                mkdir -p "$cache_dir/$modelgroup"
                if [[ "$suffix" == ".zip" ]]; then
                    unzip -o "$compressed_file" -d "$cache_dir/$modelgroup"
                else
                    tar -xf "$compressed_file" -C "$cache_dir/$modelgroup"
                fi
                echo "Decompressing weights for $modelid: $compressed_file"
                found_compressed_file=true
                break
            fi
        done
        if [ "$found_compressed_file" = false ]; then
            echo "Weights for $modelid not found."
        fi
    fi
done