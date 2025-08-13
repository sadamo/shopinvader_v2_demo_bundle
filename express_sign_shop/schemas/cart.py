from pydantic import BaseModel


class CartConfirmResponse(BaseModel):
    success: bool
    message: str
    order_id: int
    order_name: str
