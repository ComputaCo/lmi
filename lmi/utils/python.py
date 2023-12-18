from abc import ABC, abstractmethod


class HasPostInit(ABC):
    @abstractmethod
    def __post_init__(self):
        pass
    def __init_subclass__(cls) -> None:
        old_init = cls.__init__
        def new_init(self, *args, **kwargs):
            old_init(self, *args, **kwargs)
            self.__post_init__()
        cls.__init__ = new_init
        
class HasPreInit(ABC):
    @abstractmethod
    def __pre_init__(self):
        pass
    
    def __init_subclass__(cls) -> None:
        old_init = cls.__init__
        def new_init(self, *args, **kwargs):
            self.__pre_init__()
            old_init(self, *args, **kwargs)
        cls.__init__ = new_init