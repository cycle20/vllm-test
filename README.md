# Input file

TmAlphaFold article: https://github.com/cycle20/vllm-test/blob/main/gkac928.pdf

## Input as markdown

[Result-Intermediate-Text-Extraction-From-PDF.md](test-results/Result-Intermediate-Text-Extraction-From-PDF.md)

# Prompt

```python
md_text = pymupdf4llm.to_markdown(args.pdf_file)
chat_completion = client.chat.completions.create(
    messages=[{
        "role": "system",
        "content": "You are a helpful assistant."
    }, {
        "role": "user",
        "content": f"What is TmAlphaFold based on this text:\n\n  {md_text}?"
    }],
    model=args.model,
)
```

# Summary

| File Name                                                              | Device | Time     |
|------------------------------------------------------------------------|--------|----------|
| [Result-DeepSeek-R1-Distill-Qwen-1.5B.md](test-results/Result-DeepSeek-R1-Distill-Qwen-1.5B.md)                                | cpu    | 1m21     |
| [Result-DeepSeek-R1-Distill-Qwen-1.5B-with-special-cmd-params.md](test-results/Result-DeepSeek-R1-Distill-Qwen-1.5B-with-special-cmd-params.md)        | cpu    | 2m22s    |
| [Result-DeepSeek-R1-Distill-Qwen-32B.md](test-results/Result-DeepSeek-R1-Distill-Qwen-32B.md) **FAILED**                      | cpu    | 26m44s   |
| [Result-DeepSeek-R1-Distill-Qwen-7B.md](test-results/Result-DeepSeek-R1-Distill-Qwen-7B.md)                                  | cpu    | 2m53     |
| [Result-DeepSeek-R1-Distill-Qwen-7B-cuda-0.5-gpu-mem.md](test-results/Result-DeepSeek-R1-Distill-Qwen-7B-cuda-0.5-gpu-mem.md)                                  | cuda    | **32s**     |
| [Result-DeepSeek-R1-Distill-Llama-70B-quantized.w4a16.md](test-results/Result-DeepSeek-R1-Distill-Llama-70B-quantized.w4a16.md)                                  | cuda    | 1m9s  |
| [Result-DeepSeek-R1-Distill-Llama-70B-quantized.w4a16-less-input-max-length-4096.md](test-results/Result-DeepSeek-R1-Distill-Llama-70B-quantized.w4a16-less-input-max-length-4096.md) / model length: 4096 | cuda | **58s** |
| [Result-Mistral-7B-Instruct-v0.3-cuda-0.5-gpu-mem.md](test-results/Result-Mistral-7B-Instruct-v0.3-cuda-0.5-gpu-mem.md)                                     | cuda    | **9s**    |
| [Result-Mistral-7B-Instruct-v0.3.md](test-results/Result-Mistral-7B-Instruct-v0.3.md)                                     | cpu    | 1m16s    |
| [Result-Mistral-7B-Instruct-v0.3-run-2.md](test-results/Result-Mistral-7B-Instruct-v0.3-run-2.md)                               | cpu    | 1m2s     |
| [Result-Qwen2.5-1.5B-Instruct.md](test-results/Result-Qwen2.5-1.5B-Instruct.md)                                        | cpu    | **47s**      |
| [Result-Qwen2.5-1.5B-Instruct-with-special-cmd-params.md](test-results/Result-Qwen2.5-1.5B-Instruct-with-special-cmd-params.md)                | cpu    | **40s**      |
| [Result-Qwen2.5-7B-Instruct-AWQ.md](test-results/Result-Qwen2.5-7B-Instruct-AWQ.md) **FAILED**                           | cpu    | 27m+     |
| [Result-Qwen2.5-7B-Instruct-AWQ-cuda-0.5-gpu-mem.md](test-results/Result-Qwen2.5-7B-Instruct-AWQ-cuda-0.5-gpu-mem.md)                     | cuda   | **10s**      |
| [Result-Qwen2.5-7B-Instruct-AWQ-cuda.md](test-results/Result-Qwen2.5-7B-Instruct-AWQ-cuda.md) (A6000)  | cuda   | **10s**      |
| [Result-Qwen2.5-7B-Instruct-AWQ-2GPUs.md](test-results/Result-Qwen2.5-7B-Instruct-AWQ-2GPUs.md) (2 x A4500) | cuda | **18s** |

# Appendix A - Qwen2.5 Speed Benchmark

https://qwen.readthedocs.io/en/latest/benchmark/speed_benchmark.html
