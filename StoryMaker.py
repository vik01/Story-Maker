from dotenv import dotenv_values
from openai import OpenAI

config = dotenv_values(".env")
open_ai_key = config["OPENROUTER_API"]

class StoryMaker:

    url = "https://openrouter.ai/api/v1"
    basic_prompt = "Write a paragraph length story about a hero who goes on a journey, meets alies, gets stronger, finds weapons and treasure, and defeats the demon king."
    main_model = "arcee-ai/trinity-large-preview:free"
    fallback_models = ["deepseek/deepseek-r1-0528:free", "meta-llama/llama-3.3-70b-instruct:free"]

    def __init__(self):
        self.client = OpenAI(base_url=self.url, api_key=open_ai_key)
        self.preserve_convo = {}
        
    def generate(self, prompt="", temp=1, stream_result=False, token_max=5000):
        if prompt == "":
            self.first_prompt = self.basic_prompt
        else:
            self.first_prompt = prompt
        
        response = self.client.chat.completions.create(
            model=self.main_model, 
            messages=[
                {   "role": "user", 
                    "content": self.first_prompt
                }
            ],
            extra_body={
                "models": self.fallback_models,
                "reasoning": {"effort": "low"}
            },
            max_tokens=token_max,
            # stream=stream_result,
            temperature=temp
        )

    def update(self):
        pass

    @classmethod
    def create_story_prompt(cls):
        pass

    @classmethod
    def get_api_url(cls):
        return f"Base url: {cls.url}"
    
    @classmethod
    def get_main_model(cls):
        return f"Main model: {cls.main_model}"
    
    @classmethod
    def get_basic_prompt(cls):
        return f"If you do not specify a story prompt, you will get the following prompt:\n {cls.basic_prompt}"
    
    @classmethod
    def get_fallback_model(cls):
        fallback_str = "The following are fallback models in case the main model doesn't work:\n"
        for index, model in enumerate(cls.fallback_models):
            fallback_str += f"({index}) {model}, \n"
        return fallback_str
