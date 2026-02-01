import tkinter as tk
import strings
from tkinter import ttk

class GameView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(strings.APP_TITLE)
        self.geometry("1000x800")
        self.configure(bg="#f5f5f5")
        self._create_layout()
        self._create_header()
        self._create_controls()
        self._create_table()
        self._create_details_panel()

    def _create_layout(self):
        self.container = tk.Frame(self, bg="#f5f5f5")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

    def _create_header(self):
        header = tk.Frame(self.container, bg="#fa5c5c")
        header.pack(fill="x", pady=(0, 20))
        tk.Label(header, text=strings.HEADER_TEXT, fg="white", bg="#fa5c5c",
                 font=("Helvetica", 18, "bold")).pack(pady=15)

    def _create_controls(self):
        ctrl = tk.Frame(self.container, bg="#f5f5f5")
        ctrl.pack(fill="x", pady=10)
        self.btn_scrape = tk.Button(ctrl, text=strings.BTN_SCRAPE_TEXT, bg="#27ae60", fg="white",
                                    font=("Arial", 10, "bold"), padx=20)
        self.btn_scrape.pack(side="left", padx=5)
        self.btn_load = tk.Button(ctrl, text=strings.BTN_LOAD_TEXT, bg="#2980b9", fg="white",
                                  font=("Arial", 10, "bold"), padx=20)
        self.btn_load.pack(side="left", padx=5)

    def _create_table(self):
        frame = tk.Frame(self.container)
        frame.pack(fill="both", expand=True)
        cols = (strings.COL_TITLE, strings.COL_PRICE, strings.COL_DISCOUNT, strings.COL_OS)
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.column(strings.COL_TITLE, width=400, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

    def _create_details_panel(self):
        self.prev_frame = tk.LabelFrame(self.container, text=strings.TABLE_HEADER_PREVIEW, bg="white")
        self.prev_frame.pack(fill="x", pady=(20, 0))
        self.img_label = tk.Label(self.prev_frame, bg="white", text=strings.SELECT_GAME_PROMPT)
        self.img_label.pack(pady=15)

    def update_data(self, df):
        self.tree.delete(*self.tree.get_children())
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(row[strings.COL_TITLE], row[strings.COL_PRICE],
                                                row[strings.COL_DISCOUNT], row[strings.COL_OS]),
                                                tags=(row[strings.COL_IMG],))

    def set_image(self, photo):
        self.img_label.config(image=photo, text="")
        self.img_label.image = photo