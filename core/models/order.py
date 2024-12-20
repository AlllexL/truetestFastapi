from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base

# from .order_product_association import order_product_association_table

if TYPE_CHECKING:
    from . import Product
    from . import OrderProductAssociation


class Order(Base):

    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )

    # products: Mapped[list["Product"]] = relationship(
    #     secondary="order_product_association", back_populates="orders"
    # )

    product_association: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )
