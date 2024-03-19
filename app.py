from datetime import datetime
import random

import tkinter as tk
from PIL import Image

from CTkTable import CTkTable
import customtkinter as ctk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.deactivate_automatic_dpi_awareness()

import tkbhack

WIDTH = 1366
HEIGHT = 480

def random_color():
    color = random.randrange(0, 2**24)
    hex_color = hex(color)
    return hex_color

class Helpmenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title('Timetable Browser - Tutorial')

        self.width = 1695*0.5
        self.height = 635*0.5
        x = self.winfo_screenwidth() // 6 - self.width // 6
        y = self.winfo_screenheight() // 6 - self.height // 6
        self.geometry(f'{self.width}x{self.height}+{x}+{y}')

        self.protocol('WM_DELETE_WINDOW', self.die)
        
        self.framing()
    
    def framing(self):
        bg = ctk.CTkLabel(self,text='',image=ctk.CTkImage(dark_image=Image.open('static/tutorial.png'),size=(self.width,self.height)))
        bg.pack()
    
    def die(self):
        self.withdraw()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Timetable Browser')

        x = self.winfo_screenwidth() // 2 - WIDTH // 2
        y = self.winfo_screenheight() // 2 - HEIGHT // 2
        self.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')
        self.resizable(False, False)

        self.helpmenu = Helpmenu()
        self.helpmenu.withdraw()
        self.framing()
    
    def framing(self):
        # Pick subject
        self.class_choosen = ctk.CTkComboBox(self, width=200, state='readonly', command=self.tkbchange, font=(None, 21))
        self.class_choosen.grid(row=0, column=1, padx=20, pady=20, columnspan=2)
        self.class_choosen.set('Chọn lớp')


        # Labels
        self.todaylabel = ctk.CTkLabel(self, text='', font=ctk.CTkFont('Arial', 24, underline=True))
        self.todaylabel.grid(row=1, column=0, padx=20, pady=20)
        
        self.date_label = ctk.CTkLabel(self, text='TKB có tác dụng từ ngày: ...', font=ctk.CTkFont('Arial', 24, underline=True))
        self.date_label.grid(row=1, column=1, columnspan=2)

        self.status_label = ctk.CTkLabel(self, text='', font=("Arial", 17))
        self.status_label.grid(row=3, column=1, padx=20, pady= 20)
        

        # Refesh button
        refesh_button = ctk.CTkButton(self, image=ctk.CTkImage(dark_image=Image.open('static/loading.gif'),size=(50,50)),
                                      width=1, fg_color='transparent', bg_color='transparent', text='', hover=False,
                                      command=self.refesh)
        refesh_button.grid(row=3, column=0, padx=20, pady=20)


        # Help button
        help_button = ctk.CTkButton(self, image=ctk.CTkImage(dark_image=Image.open('static/question.webp'),size=(50,50)),
                              width=1, fg_color='transparent', bg_color='transparent', text='', hover=False,
                              command=self.open_helpmenu)
        help_button.grid(row=3, column=2, padx=20, pady=20)


        # Today
        coldata = ['Tiết', 'Môn',]
        rowdata = [coldata] + list([i+1, ''] for i in range(5))

        self.today = CTkTable(
            master=self,
            values=rowdata,
            font=(None, 17),
        )
        self.today.grid(row=2, column=0, padx=20)


        # Allweek
        coldata = ['Tiết'] + list(f"Thứ {i}" for i in range(2, 8))
        rowdata = [coldata] + list([i] + ['' for i in range(5)] for i in range(1,7))

        self.allday = CTkTable(
            master=self,
            values = rowdata,
            font=(None, 17),
            width=150,
        )
        self.allday.grid(row=2, column=1, padx=20, columnspan=2)

        self.today.edit_column(0, width=40)
        self.allday.edit_column(0, width=40)

    def refesh(self, *args, **kwargs):
        # Data get
        self.data, status = tkbhack.get_data()
        if status:
            self.status_label.configure(text=f'Lỗi: {type(status).__name__}. Tạm thời lấy data cũ, có thể sẽ không đúng...')
            self.status_label.configure(text_color='#bb2124')
        else:
            self.status_label.configure(text="Lấy data thành công!")
            self.status_label.configure(text_color='#22bb33')

        # Effective date
        self.date_label.configure(text=f'TKB có tác dụng từ ngày: {self.data['date']}')
        self.class_choosen.configure(values=self.data['classlist'])
        
        # Time, Week detect
        now = datetime.now()
        self.weekday = datetime.weekday(now) + int(now.hour>11 or (now.hour>=11 and now.minute>=10))
        self.todaylabel.configure(text=f'TKB ngày mai (thứ {self.weekday+2}) là...' if now.hour>11 or (now.hour>=11 and now.minute>=10) else f'TKB hôm nay (thứ {self.weekday+2}) là...')

        # Current displaying subject
        if self.class_choosen.get() not in self.data['classlist']: self.class_choosen.set('Chọn lớp')
        if self.class_choosen.get() == 'Chọn lớp': return
        self.tkbchange()

    def tkbchange(self, *args, **kwargs):
        data_all = self.data['tkb'][self.class_choosen.get()]
        data_today = data_all[self.weekday]

        tkbtoday = [['Tiết', 'Môn']] + list([i+1, data_today[i]] for i in range(5))
        sos = ['Tiết'] + list(f"Thứ {i}" for i in range(2, 8))
        tkball = [sos] + list([i+1] + list(data_all[j][i] for j in range(6)) for i in range(5))

        self.today.configure(values = tkbtoday)
        self.allday.configure(values = tkball)


    helpmenu: Helpmenu
    def open_helpmenu(self):
        self.helpmenu.deiconify()


    def run(self):
        self.after(1, self.refesh())
        self.mainloop()


app = App()
app.run()

