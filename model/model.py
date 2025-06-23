from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

class QueryStatus(Enum):
    TERMINATE_CONVERSATION  = 0
    CLEAR_CONTEXT           = 1
    NORMAL                  = 2

class Chatbot(ABC):

    @abstractmethod
    def _get_response(self, add_to_context : bool = True) -> str:
        pass

    def __init__(
            self, 
            context : Optional[list[dict]] = None, 
            system_prompt : Optional[str] = None,
            model : str = ""
    ):
        self.system_prompt = system_prompt
        self.context = context
        self.model = model


    def post_query(self, message : str, add_to_context : str = True, generation_config : Optional[dict] = None) -> tuple[str, QueryStatus]:

        if message.lower() in ['q', 'quit', 'exit']:
            return "", QueryStatus.TERMINATE_CONVERSATION
        elif message.lower() in ['clear', 'reset']:
            self.context = []
            return "Context cleared", QueryStatus.CLEAR_CONTEXT

        new_user_message = {
            "role" : "user",
            "content" : message
        }
        self.context.append(new_user_message)

        text_response = self._get_response(add_to_context=add_to_context, generation_config=generation_config)
        return text_response, QueryStatus.NORMAL
    
    def add_to_context(self, text : str, role : str = "assistant") -> None:
        new_item = {"role" : role, "content" : text}
        self.context.append(new_item)
    
    def clear_context(self):
        self.context = []

    def add_to_memory(self, new_context : list[dict]) -> None:
        self.context += new_context