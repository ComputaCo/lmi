from abc import ABC, abstractmethod


class LLMCanViewMixin(ABC):
    @abstractmethod
    def render(self, size) -> str:
        pass

    @abstractmethod
    def render_messages(self, size) -> str:
        pass
