from typing import Any
import os
from .example_prompts import *


class LLMBase(object):
    def __init__(self, *args):
        super(LLMBase, self).__init__(*args)


class ChatGpt(LLMBase):
    def __init__(self, *args):
        super(ChatGpt, self).__init__(*args)
        from openai import OpenAI
        import httpx
        from dotenv import load_dotenv

        load_dotenv(".llm_config")
        api_key = os.environ.get("OPENAI_API_KEY")
        http_proxy = os.environ.get("http_proxy")
        proxies = {"http": f"{http_proxy}", "https": f"{http_proxy}"}
        self.client = OpenAI(
            api_key=api_key,
            http_client=httpx.Client(proxy=proxies["https"]),
        )

    def __call__(self, prompt: str) -> Any:
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=prompt,
            response_format={"type": "json_object"},
            # max_tokens=4096,
            # temperature=0
        )
        info_dict = completion.choices[0].message.to_dict()
        return info_dict


class OllamaLLm(LLMBase):

    def __init__(self, sever_host="http://localhost:11434"):
        super(OllamaLLm, self).__init__()
        from ollama import Client

        self.client = Client(host=sever_host)

    def __call__(self, prompt: str) -> Any:
        response = self.client.chat(
            model="llama3.1",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            format="json",
        )
        info_dict = eval(response["message"]["content"])
        return info_dict


def call_llm(prompt, llm_model="ollama"):
    if llm_model == "chatgpt":
        llm = ChatGpt()
    elif llm_model == "ollama":
        llm = OllamaLLm()
    return llm(prompt)


def ask_newobject(object_name, scene_info: str = ""):
    prompt = add_object_prompt(object_name, scene_info)
    return call_llm(prompt)


def ask_nextobject(scene_info):
    prompt = ""
    return call_llm(prompt)