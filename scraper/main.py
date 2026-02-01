from view import GameView
from scraper_service import ScraperService
from controller import GameController

if __name__ == "__main__":
    v = GameView()
    s = ScraperService()
    c = GameController(v, s)
    v.mainloop()