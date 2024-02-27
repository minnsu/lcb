import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

def download_model_tokenzier(model_repo: str, path: str):
    model = AutoModelForCausalLM.from_pretrained(model_repo, cache_dir=path)
    tokenizer = AutoTokenizer.from_pretrained(model_repo, cache_dir=path)
    return (model, tokenizer)

def make_pipe(model_path: str, task: str, max_new_tokens: int):
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map='auto', torch_dtype=torch.float16)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    pipe = pipeline(task, model=model, tokenizer=tokenizer, max_new_tokens=max_new_tokens)
    return pipe

available_model_paths = [
    '/workspace/llms/Mistral-7B-Instruct-v0.2',
]