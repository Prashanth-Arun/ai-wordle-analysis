from .model import Chatbot
from mistralai import Mistral
from typing import Optional
import os

class MistralChatbot(Chatbot):

    def _get_response(self, add_to_context : bool = True, generation_config : Optional[dict] = None) -> str:
        
        generation_config = {} if generation_config is None else generation_config

        new_message = self.client.chat.complete(
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
            model : str = 'mistral-large-latest',
    ):
        super().__init__(context, system_prompt, model)
        self.client = Mistral(os.environ['MISTRAL_API_KEY'])
        if self.context is None:
            if self.system_prompt is not None:
                self.context = [{"role": "system", "content": system_prompt}]
            else:
                self.context = []