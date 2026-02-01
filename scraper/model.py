import strings
from dataclasses import dataclass

@dataclass
class Game:
    title: str
    price: str
    discount: str
    os_systems: str
    img_url: str

    def to_dict(self):
        return {
            strings.COL_TITLE: self.title,
            strings.COL_PRICE: self.price,
            strings.COL_DISCOUNT: self.discount,
            strings.COL_OS: self.os_systems,
            strings.COL_IMG: self.img_url
        }