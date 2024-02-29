from transformers import pipeline, AutoModel, AutoModelForCausalLM, AutoTokenizer

available_model_paths = [
    '/workspace/llms/Mistral-7B-Instruct-v0.2',
    '/workspace/llms/Microsoft-phi-2',
]

def load_LLM_model(model_repo: str, path: str=None):
    model = AutoModelForCausalLM.from_pretrained(model_repo, cache_dir=path)
    tokenizer = AutoTokenizer.from_pretrained(model=model_repo, cache_dir=path)
    if path is None:
        model.save_pretrained(model_repo)
        tokenizer.save_pretrained(model_repo)
    return (model, tokenizer)

def load_embedding_model(model_repo: str, path: str=None):
    model = AutoModel.from_pretrained(model_repo)
    tokenizer = AutoTokenizer.from_pretrained(model_repo)
    if path is None:
        model.save_pretrained(model_repo)
        tokenizer.save_pretrained(model_repo)
    return (model, tokenizer)