import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview, TableRow

import tkbhack

from datetime import *
import random

WIDTH = 1200
HEIGHT = 480

def random_color():
    color = random.randrange(0, 2**24)
    hex_color = hex(color)
    return hex_color

class App(ttk.Window):

    def __init__(self):
        super().__init__(themename='superhero')

        x = self.winfo_screenwidth() // 2 - WIDTH // 2
        y = self.winfo_screenheight() // 2 - HEIGHT // 2
        self.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')

        self.title('TKB')
        
        # self.cbb_var = StringVar(value='Conchim')
        # self.cbb = CTkComboBox(self, values=['Hello', 'Conchim', 'Hay hot'], variable=self.cbb_var, command=self.emthaydoiroi)
        # self.cbb.grid(row=0, column=1, padx=20, pady=20)
        # cbb.set('Conchim')
        
        self.framing()
    

    def framing(self):
        self.class_choosen = ttk.Combobox(self, width=10, state='readonly')
        self.class_choosen.grid(row=0, column=1, padx=20, pady=20)
        self.class_choosen.set('Chọn môn')

        self.class_choosen.bind('<<ComboboxSelected>>', self.emthaydoiroi)

        mytime = datetime.now().time()
        if mytime.hour>11 or (mytime.hour>=11 and mytime.minute>=10):
            epic = 'TKB ngày mai là...'
        else:
            epic = 'TKB hôm nay là...'

        ttk.Label(self, text = epic, font=("Arial", 14)
                ).grid(row=1, column=0) 
        
        self.date_label = ttk.Label(self, text = 'TKB có tác dụng từ ngày: ...', font=("Arial", 14))
        self.date_label. grid(row=1, column=1)
        
        refesh_button = ttk.Button(self, text='🔄️', command=self.refesh,width=3)
        refesh_button.grid(row=3, column=0, padx=20, pady=20)

        self.status_label = ttk.Label(self, text='', font=("Arial", 14))
        self.status_label.grid(row=3, column=1, padx=20, pady= 20)

        self.refesh()

    def refesh(self):
        self.data, status = tkbhack.get_data()
        if status:
            self.status_label.configure(text=f'Lỗi: {type(status).__name__}. Tạm thời lấy data cũ, có thể sẽ không đúng...', bootstyle='danger')
        else:
            self.status_label.configure(text="Lấy data thành công!", bootstyle='success')
        self.date_label.config(text=f'TKB có tác dụng từ ngày: {self.data['date']}')
        self.class_choosen['values']=self.data['classlist']
        

        if self.class_choosen.get() not in self.data['classlist']:
            self.class_choosen.set('Chọn môn')
            self.newtkb()
        if self.class_choosen.get() == 'Chọn môn': return
        self.newtkb(self.data['tkb'][self.class_choosen.get()][0],
                    self.data['tkb'][self.class_choosen.get()])

    def emthaydoiroi(self, *args, **kwargs):
        # self.class_choosen.get()
        self.newtkb(self.data['tkb'][self.class_choosen.get()][0],
                    self.data['tkb'][self.class_choosen.get()])


    def newtkb(self, lessontoday:list=None, lessonall:list=None):
        self.tkbtoday(lessontoday)
        self.tkball(lessonall)
    
    def tkbtoday(self, lesson:list=None):
        """
        data struct:
        [1, 2, 3, 4, 5]
        """
        
        coldata = [
            {"text": "Tiết", 'width': 40},
            {"text": "Môn", 'stretch': True}
        ]
        if not lesson: rowdata = list([i+1, ''] for i in range(5))
        else: rowdata = list([i+1, lesson[i]] for i in range(5))
        
        today = Tableview(
            master=self,
            coldata=coldata,
            rowdata=rowdata,
            bootstyle=SUCCESS,
            height=10,
        )
        today.grid(row=2, column=0, padx=20)
    
    def tkball(self, lesson:list=None):
        """
        data struct:
        [
            [1, 2, 3, 4, 5], # 2
            [1, 2, 3, 4, 5], # 3
            [1, 2, 3, 4, 5], # 4
            [1, 2, 3, 4, 5], # 5
            [1, 2, 3, 4, 5], # 6
            [1, 2, 3, 4, 5] # 7
        ]
        """
        coldata = [{"text": "Tiết", 'width': 40}] + list({"text": f"Thứ {i}", 'width': 140} for i in range(2, 8))
        if not lesson: rowdata = list([i] + ['' for i in range(5)] for i in range(1,7))
        else: rowdata = list([i+1] + list(lesson[j][i] for j in range(6)) for i in range(5))

        allday = Tableview(
            master=self,
            coldata=coldata,
            rowdata=rowdata,
            bootstyle=PRIMARY,
            height=10,
        )
        allday.grid(row=2, column=1, padx=20)



app = App()
app.mainloop()

