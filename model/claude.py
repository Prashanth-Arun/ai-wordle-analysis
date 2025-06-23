from .model import Chatbot
from typing import Optional
import anthropic

class ClaudeChatbot(Chatbot):

    def _get_response(self, add_to_context : bool = True, generation_config : Optional[dict] = None) -> str:

        generation_config = {} if generation_config is None else generation_config
        
        new_message = self.client.messages.create(
            model=self.model,
            system="" if self.system_prompt is None else self.system_prompt,
            messages=self.context,
            max_tokens=512,
            **generation_config
        )
        
        text_response = new_message.content[0].text
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
            model : str = 'claude-3-5-haiku-20241022',
    ):
        super().__init__(context, system_prompt, model)
        if context is None:
            self.context = []
        self.client = anthropic.Anthropic()