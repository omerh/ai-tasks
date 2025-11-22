from pydantic import BaseModel


class AmazonItem(BaseModel):
    asin: str
    name: str
    description: str
    url: str
    price: str
    discount_amount: str
    rating: str
    amount_of_reviews: str
    review_summary: str | None = ""
