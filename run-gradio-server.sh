source /home/tusnady/csongor/venv-vllm-cuda/bin/activate
log_dir=logs

python -u src/grad-app.py &> "$log_dir/gradio-server.log" &

