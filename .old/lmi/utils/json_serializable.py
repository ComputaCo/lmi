from __future__ import annotations
from abc import ABC
from typing import Union

from pydantic import BaseModel, Field
from pydantic.tools import parse_obj_as

from lmi.utils.union import make_union

JSON = bool | int | str | list["JSON"] | dict[str, "JSON"]


class JSONSerializable(BaseModel, ABC):
    type: str = None

    def __init__(self):
        super().__init__(type=self.__class__.__name__)

    @classmethod
    def nonabstract_subclasses(cls):
        for subclass in cls.__subclasses__():
            if not subclass.__abstractmethods__:
                yield subclass

    @classmethod
    def RootParseModel(cls):
        if len(cls.__subclasses__()) == 0:
            return cls
        if len(cls.nonabstract_subclasses()) == 0:
            raise Exception("No non-abstract children to deserialize")

        return type(
            "RootParseModel",
            (BaseModel,),
            {
                "__root__": Field(..., descriminator="type"),
                "__annotations__": {
                    "__root__": make_union(cls.nonabstract_subclasses()),
                },
            },
        )

        # class ParseRootModel(BaseModel):
        #     __root__: make_union(cls.nonabstract_subclasses()) = Field(
        #         ..., descriminator="type"
        #     )

        return ParseRootModel

    @classmethod
    def from_json(cls, json):
        return parse_obj_as(cls.RootParseModel(), json)

    def to_json(self):
        return self.model_dump()

    # @classmethod
    # def subclass_with_pydantic_type(cls, name) -> type[JSONSerializable]:
    #     # Making this a classmethod allows us to automatically restrict the
    #     # scope of available options to whatever the base's subclasses are.
    #     for sub in cls.__subclasses__():
    #         if sub.__name__ == name:
    #             return sub
    #     else:
    #         raise ValueError(f"Invalid pydantic_type: {name}")
    #
    # @classmethod
    # def from_json(cls, json: JSON) -> JSONSerializable:
    #     if isinstance(json, (bool, int, str)):
    #         return json
    #     elif isinstance(json, list):
    #         return [JSONSerializable.from_json(item) for item in json]
    #     elif isinstance(json, dict):
    #         if "pydantic_type" in json:
    #             pydantic_type = json["pydantic_type"]
    #             pydantic_cls = cls.subclass_with_pydantic_type(pydantic_type)
    #             params = cls.from_json(json)
    #             return pydantic_cls.parse_raw(params)
    #         else:
    #             return {
    #                 key: JSONSerializable.from_json(value)
    #                 for key, value in json.items()
    #             }
    #     else:
    #         raise ValueError(f"Invalid JSON: {json}")
