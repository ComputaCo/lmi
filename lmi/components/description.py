from abc import abstractmethod
from pathlib import Path
from gptos.lmi.components.text import Text
import stringcase
import tensorcode as tc

from gptos.lmi.components.component import Component
from gptos.lmi.misc.alignment import Alignment
from gptos.lmi.misc.truncation import truncate


class Description(Text):

    obj: object = None
    path: str | Path = None

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        assert (
            self.obj is not None or self.path is not None
        ), "Either obj or path must be provided"

        if self.obj:
            self.object = self.obj
        if self.path:
            self.object = self.loader(path=Path(self.path))

        if self.object:
            self.text = tc.text.describe(self.object)
        else:
            self.text = tc.text.describe(path=self.path)

    @abstractmethod
    def loader(self, path: Path = None):
        pass

    @staticmethod
    def variant(type_name=None, T=None, *, loader=None):
        if isinstance(type_name, type):
            T = type_name
            type_name = Description.__name__
        return type(
            type_name,
            (Description,),
            {
                **({"loader": loader} if loader else {}),
                **({"__annotations__": {"obj": T}} if T else {}),
            },
        )
