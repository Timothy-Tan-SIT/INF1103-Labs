from product import Product


class DigitalProduct(Product):
    # A digital product IS-A Product.
    # It is downloaded, so it does not implement CanBeShipped.

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)

        if isinstance(download_size, bool) or not isinstance(download_size, (int, float)):
            raise ValueError("Download size must be a number.")

        if download_size < 0:
            raise ValueError("Download size cannot be negative.")

        self.__download_size = download_size

    @property
    def download_size(self):
        return self.__download_size

    # ----- Overridden methods (reuse the parent, then add download size) -----

    def display_information(self):
        super().display_information()
        print(f"    Download Size: {self.__download_size} MB")

    def display_details(self):
        super().display_details()
        print(f"Download Size: {self.__download_size} MB")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    # ----- Abstract method from Product -----

    def get_fulfilment_info(self):
        return "Digital product: delivered digitally via download."
