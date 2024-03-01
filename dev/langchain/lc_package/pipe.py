import torch
from transformers import pipeline, AutoModel, AutoModelForCausalLM, AutoTokenizer
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

def get_model_and_tokenizer(model_path, load_in_8bit: bool=False):
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map='auto', torch_dtype=torch.bfloat16, load_in_8bit=load_in_8bit)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return (model, tokenizer)
    

def make_llm_pipe(model_path: str, task: str, max_new_tokens: int=512, temperature: float=0.6, top_p: float=0.95, repetition_penalty: float=1.2, load_in_8bit: bool=False):
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map='auto', torch_dtype=torch.bfloat16, load_in_8bit=load_in_8bit)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    hf_pipe = pipeline(task=task, model=model, tokenizer=tokenizer, max_new_tokens=max_new_tokens, do_sample=True, temperature=temperature, top_p=top_p, repetition_penalty=repetition_penalty)
    lc_pipe = HuggingFacePipeline(pipeline=hf_pipe)
    return lc_pipe

def make_llm_pipe_fast(model_path: str, task: str, max_new_tokens: int=512, temperature: float=0.6, top_p: float=0.95, repetition_penalty: float=1.2):
    lc_pipe = HuggingFacePipeline.from_model_id(
        model_id=model_path,
        device=0,
        task=task,
        pipeline_kwargs={
            'max_new_tokens': max_new_tokens,
            'do_sample': True,
            'temperature': temperature,
            'top_p': top_p,
            'repetition_penalty': repetition_penalty
        }
    )
    return lc_pipe