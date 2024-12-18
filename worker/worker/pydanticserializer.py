import json
from pydantic import BaseModel
import schemas


class PydanticSerializer(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseModel):
            return o.model_dump() | {"__type__": type(o).__name__}
        else:
            return json.JSONEncoder.default(self, o)


def pydantic_decoder(obj):
    if "__type__" in obj:
        if obj["__type__"] in dir(schemas):
            cls = getattr(schemas, obj["__type__"])
            return cls.parse_obj(obj)
    return obj


# Encoder function
def pydantic_dumps(obj):
    return json.dumps(obj, cls=PydanticSerializer)


# Decoder function
def pydantic_loads(obj):
    return json.loads(obj, object_hook=pydantic_decoder)
