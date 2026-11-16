class Supplier:
    # Represents a supplier of products.
    # A Supplier is created independently of any Product (association, not ownership):
    # a supplier can exist with no products, and a product can outlive its supplier variable.

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if not isinstance(supplier_id, str) or supplier_id.strip() == "":
            raise ValueError("Supplier ID cannot be empty.")

        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Supplier name cannot be empty.")

        if not isinstance(contact_email, str) or "@" not in contact_email:
            raise ValueError("Supplier contact email must be a valid email address.")

        self.__supplier_id: str = supplier_id.strip()
        self.__name: str = name.strip()
        self.__contact_email: str = contact_email.strip()

    # ----- Read-only access to the attributes -----

    @property
    def supplier_id(self) -> str:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact_email(self) -> str:
        return self.__contact_email

    # ----- Behaviour -----

    def display_information(self) -> None:
        print(
            f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | "
            f"Email: {self.__contact_email}"
        )

    def to_dict(self) -> dict[str, str]:
        # Used by the file-handling code when saving a product's supplier to JSON.
        return {
            "id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email
        }