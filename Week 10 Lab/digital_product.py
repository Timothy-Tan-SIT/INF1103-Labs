from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    # A digital product IS-A Product.
    # It is downloaded, so it does not implement CanBeShipped.

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock_quantity, supplier)

        if isinstance(download_size, bool) or not isinstance(download_size, (int, float)):
            raise ValueError("Download size must be a number.")

        if download_size < 0:
            raise ValueError("Download size cannot be negative.")

        self.__download_size: float = download_size

    @property
    def download_size(self) -> float:
        return self.__download_size

    # ----- Overridden methods (reuse the parent, then add download size) -----

    def display_information(self) -> None:
        super().display_information()
        print(f"    Download Size: {self.__download_size} MB")

    def display_details(self) -> None:
        super().display_details()
        print(f"Download Size: {self.__download_size} MB")

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    # ----- Abstract method from Product -----

    def get_fulfilment_info(self) -> str:
        return "Digital product: delivered digitally via download."