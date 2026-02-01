import requests
import strings
from bs4 import BeautifulSoup
from model import Game

class ScraperService:
    def __init__(self):
        self.base_url = strings.BASE_URL
        self.headers = {"User-Agent": strings.USER_AGENT}

    def get_games_from_web(self, pages=3):
        game_list = []

        for p in range(1, pages + 1):
            url = f"{self.base_url}?page={p}"

            try:
                response = requests.get(url, headers=self.headers, timeout=15)
                response.encoding = "utf-8"
                response.raise_for_status()
            except:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            for cell in soup.select(".game_cell"):
                title_el = cell.select_one(".game_title a, .title")
                title = title_el.get_text(strip=True) if title_el else "N/A"

                discount_el = cell.select_one(".sale_tag")
                discount = discount_el.get_text(strip=True) if discount_el else "0%"

                price = "Gratis"
                price_el = cell.select_one(".price_tag, .price, .game_price_widget")

                if price_el:
                    raw_price = price_el.get_text(strip=True)
                    price = raw_price.replace(discount, "").strip()
                    if not price:
                        price = "Gratis"

                img_tag = cell.select_one(".game_thumb img")
                img_url = img_tag.get("data-lazy_src") or img_tag.get("src") if img_tag else ""

                platforms = []

                for icon in cell.select(".game_platform span, .button_config_widget span"):
                    info = icon.get("title", "").lower()
                    if "windows" in info: platforms.append("Windows")
                    if "macos" in info or "apple" in info: platforms.append("Mac")
                    if "linux" in info: platforms.append("Linux")

                os_str = ", ".join(sorted(set(platforms))) if platforms else "Web"
                game_list.append(Game(title, price, discount, os_str, img_url))

        return game_list