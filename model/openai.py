from .model import Chatbot
from typing import Optional
import openai
import os

class GPTChatbot(Chatbot):

    def _get_response(self, add_to_context : bool = True, generation_config : Optional[dict] = None) -> str:
        
        generation_config = {} if generation_config is None else generation_config
        new_message = self.client.chat.completions.create(
            model=self.model,
            messages=self.context,
            **generation_config
        )
        text_response = new_message.choices[0].message.content
        if add_to_context:
            assistant_response = {
                "role" : "assistant",
                "content" : text_response
            }
            self.context.append(assistant_response)
        
        return text_response


    def __init__(
            self, 
            context : Optional[list[dict]] = None, 
            system_prompt : Optional[str] = None,
            model : str = 'gpt-4o-2024-11-20'
    ):
        
        super().__init__(context, system_prompt, model)
        self.client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        
        if self.context is None:
            if self.system_prompt is not None:
                self.context = [{"role": "system", "content": system_prompt}]
            else:
                self.context = []