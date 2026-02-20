from dotenv import dotenv_values
from openai import OpenAI

config = dotenv_values(".env")
open_ai_key = config["OPENROUTER_API"]

class StoryMaker:

    # Base URL
    url = "https://openrouter.ai/api/v1"
    
    # Models to use and fallbacks
    main_model = "arcee-ai/trinity-large-preview:free"
    fallback_models = ["deepseek/deepseek-r1-0528:free", "meta-llama/llama-3.3-70b-instruct:free"]

    # system and prompts
    basic_prompt = "Write a one paragraph story about a hero who goes on a journey, meets alies, gets stronger, finds weapons and treasure, and defeats the demon king."
    init_sys_prompt = "You are a master storyteller known for bestselling and critically acclaimed novels. Your writing is cinematic, emotionally immersive, and rich with atmosphere. \
                       Show, don’t tell. Use sensory detail, internal monologue, and layered description. Build tension naturally. Characters should feel psychologically real and complex. \
                        Avoid generic phrasing, shallow description, and mechanical structure."
    
    # All conversations
    __all_convo = {}

    def __init__(self, system_prompt:str=""):
        self.client = OpenAI(base_url=self.url, api_key=open_ai_key)

        # make sure some values are set.
        self.temp = 1
        self.max_tokens = 1000
        self.stream_result = False
        self.preserve_convo = []

        if system_prompt != "":
            self.preserve_convo.append({
                    "role": "system", 
                    "content": self.init_sys_prompt
                }
            )
        else:
            self.preserve_convo.append({
                    "role": "system", 
                    "content": system_prompt
                }
            )


    def __chat(self):
        response = self.client.chat.completions.create(
            model=self.main_model, 
            messages=self.preserve_convo,
            extra_body={
                "models": self.fallback_models
            },
            max_tokens=self.max_tokens,
            stream=self.stream_result,
            temperature=self.temp
        )

        if self.stream_result:
            complete_response = ""

            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    complete_response += content
                    print(content, end="", flush=True)
            print()
            
            self.preserve_convo.append({
                    "role": "assistant", 
                    "content": complete_response,
                }
            )
            return complete_response

        else:
            self.preserve_convo.append({
                    "role": "assistant", 
                    "content": response.choices[0].message.content,
                }
            )
            return response.choices[0].message.content

        
    def generate(self, prompt:str=""):  
        # Initialize the prompt.    
        if prompt == "":
            message = {"role": "user", "content": self.basic_prompt}
        else:
            message = {"role": "user", "content": prompt}
        self.preserve_convo.append(message)
        
        # chat with the model.
        model_response = self.__chat()

        return model_response


    def update(self, **kwargs):
        if len(self.preserve_convo) == 1:
            raise "Error: You need to run `generate()` first to get a basic story. Then run `update()` again to make updates to it."

        # Make the message
        message = {"role":"user", "content": "Update the story you have created with the following parameters:\n"}
        for key, value in kwargs.items():
            message["content"] += f"{key}: {value}\n"
        
        # chat with the model.
        model_response = self.__chat()

        return model_response


    def create_story_prompt(self, prompt:str="", **kwargs):
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
