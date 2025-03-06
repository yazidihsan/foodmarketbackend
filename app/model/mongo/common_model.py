from bson import ObjectId
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, handler) -> ObjectId:
        if not isinstance(v, ObjectId):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            v = ObjectId(v)
        return v

    @classmethod
    def __get_pydantic_json_schema__(
            cls,
            _schema_generator: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string"}
