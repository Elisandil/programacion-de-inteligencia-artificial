import pandas as pd
import os
import requests
import strings
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
from datetime import datetime


class GameController:
    def __init__(self, view, service):
        self.view = view
        self.service = service
        self.view.btn_scrape.config(command=self.run_scraping)
        self.view.btn_load.config(command=self.load_csv)
        self.view.tree.bind("<<TreeviewSelect>>", self.on_select)

    def run_scraping(self):

        try:
            if not os.path.exists(strings.DATA_FOLDER):
                os.makedirs(strings.DATA_FOLDER)

            games = self.service.get_games_from_web(pages=3)
            df = pd.DataFrame([g.to_dict() for g in games])

            timestamp = datetime.now().strftime(strings.DATE_FORMAT)
            filename = f"{strings.FILE_PREFIX}{timestamp}{strings.CSV_EXTENSION}"
            file_path = os.path.join(strings.DATA_FOLDER, filename)

            df.to_csv(file_path, index=False, encoding=strings.FILE_ENCODING)
            self.view.update_data(df)
            messagebox.showinfo(strings.MSG_SUCCESS_TITLE, strings.MSG_SUCCESS_SCRAPE.format(len(games), file_path))
        except Exception as ex:
            messagebox.showerror(strings.MSG_ERROR_TITLE, strings.MSG_ERROR_SCRAPE.format(ex))

    def load_csv(self):
        initial_dir = strings.DATA_FOLDER if os.path.exists(strings.DATA_FOLDER) else "."
        file_path = filedialog.askopenfilename(initialdir=initial_dir, title=strings.FILE_DIALOG_TITLE,
                                               filetypes=strings.FILE_TYPES)

        if file_path:
            try:
                df = pd.read_csv(file_path, encoding=strings.FILE_ENCODING)
                self.view.update_data(df)
            except Exception as ex:
                messagebox.showerror(strings.MSG_ERROR_TITLE, strings.MSG_ERROR_LOAD.format(ex))

    def on_select(self, event):
        sel = self.view.tree.selection()

        if not sel: return
        url = self.view.tree.item(sel[0], "tags")[0]

        if url:
            try:
                r = requests.get(url, timeout=10)
                img = Image.open(BytesIO(r.content)).resize((300, 225), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.view.set_image(photo)
            except:
                self.view.set_image(None)