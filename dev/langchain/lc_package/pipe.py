import torch
from transformers import pipeline, AutoModel, AutoModelForCausalLM, AutoTokenizer
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

def get_model_and_tokenizer(model_path, load_in_8bit: bool=False):
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map='auto', torch_dtype=torch.bfloat16, load_in_8bit=load_in_8bit)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return (model, tokenizer)
    
def adjust_option(model, tokenizer, task: str, max_new_tokens: int=512, temperature: float=0.6, top_p: float=0.95, repetition_penalty: float=1.2):
    hf_pipe = pipeline(task=task, model=model, tokenizer=tokenizer, max_new_tokens=max_new_tokens, do_sample=True, temperature=temperature, top_p=top_p, repetition_penalty=repetition_penalty)
    lc_pipe = HuggingFacePipeline(pipeline=hf_pipe)
    return lc_pipe

def make_llm(model_path: str, task: str, max_new_tokens: int=512, temperature: float=0.6, top_p: float=0.95, repetition_penalty: float=1.2, load_in_8bit: bool=False):
    model, tokenizer = get_model_and_tokenizer(model_path, load_in_8bit)
    return adjust_option(model, tokenizer, task, max_new_tokens, temperature, top_p, repetition_penalty)