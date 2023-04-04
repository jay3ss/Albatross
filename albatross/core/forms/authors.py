from pydantic import BaseModel, validator


class NewAuthorForm(BaseModel):
    name: str | None = None


class CreateAuthorForm(BaseModel):
    name: str

    @validator("name")
    def name_must_not_be_empty(cls, name: str) -> str:
        if not name:
            raise ValueError("'name' must not be empty")

        return name
