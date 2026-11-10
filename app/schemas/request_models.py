from pydantic import BaseModel, field_validator

class ContCreate(BaseModel):
    description : str | None = None
    amount : float

class ContUpdate(BaseModel):
    description: str | None = None
    amount: float | None = None

    @field_validator("amount")
    def validate_amount(cls, value):
        if value is None:
            raise ValueError("Amount cannot be null!")
        return value


