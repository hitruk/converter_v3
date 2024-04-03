

import tkinter as tk
from tkinter import ttk
from tkinter.constants import *


# не допускаются отрицательные значения в параметрах Model

class Model:
    def __init__(self, value):
        if type(value) not in [int, float]:
            # значение(value) должно быть целым числом или числом с плавающей запятой.
            raise TypeError(f'In class Model, method __init__: value must be an integer or float')
        if value < 0:
            # значение(value) не должно быть отрицательным
            raise ValueError(f'value must not be negative')

        self._value = value

    @property
    def value(self):
        self._value = value

    @value.setter
    def value(self, x):
        if type(x) in [int, float]:
            self._value = x
        else:
            raise TypeError(f'Invalid data type {type[x]}')

    def mi_to_km(self):
        km = self._value * 1.609344
        return km
    
    def km_to_mi(self):
        mi = self._value / 1.609344
        return mi


class View(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self['borderwidth'] = 1
        self['relief'] = SOLID
        self.pack(padx=2, pady=2, fill=BOTH, expand=True)
    
        # contant
        self.label_title = ttk.Label(self, text='Convert Miles to Km')
        self.label_title.pack()

        self.entry_left_type = tk.StringVar(value=1)
        self.entry_left = ttk.Entry(self, textvariable=self.entry_left_type)
        self.entry_left.pack() 

        self.label_left = ttk.Label(self, text='kilometers (km)')
        self.label_left.pack()


        # Label_swap
        # отображать label будет text ='asdas', но если задан textvariable='asdasd', то отобразится только текст variable
        # self.label_swap_type = tk.BooleanVar() # defoult False
        self.label_swap = ttk.Label(self,  text='<==>')  # textvariable=self.label_swap_type,
        self.label_swap.pack()
        # разобраться с bind !!!
        self.label_swap.bind('<Button-1>', self.label_swap_cliked)

        self.entry_right_type = tk.StringVar()
        self.entry_right = ttk.Entry(self, textvariable=self.entry_right_type)
        self.entry_right.pack()

        self.label_right = ttk.Label(self, text='miles (mi)')
        self.label_right.pack()

        self.label_result = ttk.Label(self, text='result')
        self.label_result.pack()

        # set controller
        self.controller = None

        # swith converter необходим для переключения mi_to_km/km_to_mi
        self.switch = True

    def set_controller(self, controller):
        self.controller = controller


    def label_swap_cliked(self, event):
        if self.controller:
            try:
                entry_left_value = float(self.entry_left_type.get()) 
                self.controller.convert(entry_left_value)
            except ValueError as error: # TypeError as error:
                print(f'In class View, method name: label_swap_cliked {error}')

    def switch_convert(self):
        if self.switch:
            self.switch = False
            self.label_left['text'] = 'miles (mi)'
            self.label_right['text'] = 'kilometers (km)'
            self.label_title['text'] = 'Convert Km to Miles'
            print(self.switch)
        else:
            self.switch = True
            print(self.switch)
            self.label_right['text'] = 'miles (mi)'
            self.label_left['text'] = 'kilometers (km)'
            self.label_title['text'] = 'Convert Miles to Km' 
        return self.switch

    def entry_right_value(self, value):
        self.entry_right_type.set(value) 


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.defoult_convert()

    def defoult_convert(self):
        try:
            x = float(self.view.entry_left_type.get())
            self.model.value = x
            res = self.model.mi_to_km()
            print(f'mi_to_km: {res}')
            self.view.entry_right_value(res)
        except TypeError as error:
            print(f'In class Controller: {error}: {type(x)}')

    def convert(self, x):
        try:
            self.model.value = x
            if self.view.switch_convert():
                # mi_to_km
                res = self.model.mi_to_km()
                print(f'mi_to_km: {res}')
                self.view.entry_right_value(res)
            else:
                # km_to_mi
                res = self.model.km_to_mi() 
                print(f'km_to_mi: {res}')
                self.view.entry_right_value(res)
        except TypeError as error:
            print(f'In class Controller, method convert: {error}: {type(x)}') 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Hello world!')
        self.geometry('300x400')
        
        model = Model(1)
        view = View(self)

        controller = Controller(model, view)
        
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    #view = View(app)
    app.mainloop()
