from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    role: str
    credits: int


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    api_key: str

    class Config:
        orm_mode = True


class CommandCreate(BaseModel):
    command_text: str


class CommandResponse(BaseModel):
    id: int
    command_text: str
    status: str
    credits_used: int

    class Config:
        orm_mode = True


class RuleCreate(BaseModel):
    pattern: str
    action: str


class RuleResponse(BaseModel):
    id: int
    pattern: str
    action: str

    class Config:
        orm_mode = True


class LogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    command_text: str

    class Config:
        orm_mode = True
