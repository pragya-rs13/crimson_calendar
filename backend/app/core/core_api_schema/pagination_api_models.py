from pydantic import BaseModel

class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_pages: int
    total_items: int