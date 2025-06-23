from enum import Enum
from .model import Chatbot
from groq import Groq
from typing import Optional

class GroqChatbot(Chatbot):

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
            model : str = 'llama-3.1-8b-instant',
    ):

        super().__init__(context, system_prompt, model)
        self.client = Groq()
        if self.context is None:
            if self.system_prompt is not None:
                self.context = [
                    {"role" : "system", "content" : self.system_prompt}
                ]
            else:
                self.context = []