from pydantic import ValidationError

from app.dto.product_dto import ProductRequestDto


def validate_product_data(data: dict | ProductRequestDto) -> ProductRequestDto:
    try:
        if isinstance(data,ProductRequestDto):
            return data

        return ProductRequestDto(**data)
    except ValidationError as e :
        raise ValueError(str(e))