from pydantic import ValidationError

from app.dto.category_dto import CategoryRequestDto


def validate_category_data(data: dict | CategoryRequestDto) -> CategoryRequestDto:
    try:
        if isinstance(data,CategoryRequestDto):
            return data

        return CategoryRequestDto(**data)
    except ValidationError as e :
        raise ValueError(str(e))