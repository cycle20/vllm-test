source /home/tusnady/csongor/venv-vllm-cuda/bin/activate
model=neuralmagic/DeepSeek-R1-Distill-Llama-70B-quantized.w4a16
log_dir=logs

mkdir -p "$log_dir"
vllm serve "$model"  --gpu-memory-utilization 0.9 --max-model-len 9000 &> "$log_dir/vllm.log" &

# embedding version:
# vllm serve "$model"  --gpu-memory-utilization 0.9 --max-model-len 9000 --task embed
