from customtkinter import*

set_appearance_mode("dark")
set_default_color_theme("green")

class ConnectWindow(CTk):
    def __init__(self):
        super().__init__()

        self.name = None
        self.host = None
        self.port = None

        self.title("Agario connect")
        self.geometry("320x460")
        self.resizable(False, False)

        CTkLabel(self, text="Agario", font=("Arial", 40, "bold"), text_color="blue").pack(pady=(30, 0))
        CTkLabel(self, text="Online edition", font=("Arial", 16), text_color="gray").pack(pady=(20, 0))

        self.name_entry = CTkEntry(self, placeholder_text="Enter your name", height=45, corner_radius=15)
        self.name_entry.pack(padx=30, pady=5, fill="x")

        self.host_entry = CTkEntry(self, placeholder_text="IP address", height=45, corner_radius=15)
        self.host_entry.pack(padx=30, pady=5, fill="x")

        self.port_entry = CTkEntry(self, height=45, corner_radius=15)
        self.port_entry.insert(0, "8080")
        self.port_entry.pack(padx=30, pady=5, fill="x")

        self.error_label = CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)

        CTkButton(self, text="Connect", command=self.open_game, height=45, corner_radius=15).pack(padx=30, pady=20, fill="x")


    def open_game(self):
        name = self.name_entry.get().strip()
        host = self.host_entry.get().strip()
        port = self.port_entry.get().strip()

        if name == "" or host == "":
            self.error_label.configure(text="Всі поля повинні бути заповнені")
            return

        if not port.isdigit():
            self.error_label.configure(text="Порт повинен бути числом")
            return

        self.name = name
        self.host = host   
        self.port = int(port)
        self.destroy()
