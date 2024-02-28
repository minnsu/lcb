from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

available_model_paths = [
    '/workspace/llms/Mistral-7B-Instruct-v0.2',
    '/workspace/llms/Microsoft-phi-2',
]

def download_model(model_repo: str, path: str):
    model = AutoModelForCausalLM.from_pretrained(model_repo, cache_dir=path)
    tokenizer = AutoTokenizer.from_pretrained(model_repo, cache_dir=path)