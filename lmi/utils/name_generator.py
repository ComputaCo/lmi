class UniqueNameMixin(ABC):
    # TODO: i just pulled this out of Component and it's broken

    __COMPONENT_NAMES: dict[Type, set[str]] = {}
    
    def __init__(self):
        if not self.name:
            self.name = self.generate_name()
        elif self.name in self._CLASS_COMPONENT_NAMES:
            self.name = self.generate_name()
        self._CLASS_COMPONENT_NAMES.append(self.name)

    @property
    @classmethod
    def _CLASS_COMPONENT_NAMES(cls) -> set[str]:
        if cls not in Component.__COMPONENT_NAMES:
            Component.__COMPONENT_NAMES[cls] = []
        return cls.__COMPONENT_NAMES[cls]

    @classmethod
    def generate_name(cls):
        for i in range(1, inf):
            name = f"{cls.__name__}{i}"
            if name not in cls._CLASS_COMPONENT_NAMES:
                return name
