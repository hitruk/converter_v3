

import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
import re

class Model:
    def __init__(self, value):
        if type(value) not in [int, float]:
            # значение(value) должно быть целым числом или числом с плавающей запятой.
            raise TypeError(f'In class Model, method __init__: value must be an integer or float')
        if value < 0:
            # значение(value) не должно быть отрицательным, 
            # но только как прараметр класса, при создании экземпляра класса. 
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
        options = {'padx':2, 'pady':2}
        self.label_title = ttk.Label(self, text='Convert Miles to Km', font=("Helvetica", 14))
        self.label_title.grid(column=0, row=0, columnspan=3, sticky=NW, **options)

        self.label_left = ttk.Label(self, text='miles (mi)')
        self.label_left.grid(column=0, row=1, **options)

        self.label_right = ttk.Label(self, text='kilometers (km)')
        self.label_right.grid(column=2, row=1, **options)

        # ENTRY LEFT
        vcmd = (self.register(self.validate_left), '%P')
        #ivcmd = (self.register(self.on_invalid),)
        self.entry_left_type = tk.StringVar(value=1)
        self.entry_left = ttk.Entry(self, textvariable=self.entry_left_type)
        self.entry_left.bind('<KeyRelease>', self.change_entry_left)
        self.entry_left.config(validate='key', validatecommand=vcmd)#, invalidcommand=ivcmd)
        self.entry_left.grid(column=0, row=2, **options)

        # ENTRY RIGHT
        vcmd_r = (self.register(self.validate_right), '%P')
        self.entry_right_type = tk.StringVar(value=1.609344)
        self.entry_right = ttk.Entry(self, textvariable=self.entry_right_type)
        self.entry_right.bind('<KeyRelease>', self.change_entry_right)
        self.entry_right.config(validate='key', validatecommand=vcmd_r)
        self.entry_right.grid(column=2, row=2, **options)

        # Label_swap
        self.label_swap_type = tk.BooleanVar() # defoult False
        self.label_swap = ttk.Label(self,  text='<==>')
        self.label_swap.grid(column=1, row=2)
        self.label_swap.bind('<Button-1>', self.label_swap_cliked)


        # set controller
        self.controller = None

        # swith converter необходим для переключения конвертера mi_to_km/km_to_mi
        self.switch = False

        print(f'Entry left value defoult  {self.entry_left_type.get()}')

    def set_controller(self, controller):
        self.controller = controller

    def change_entry_left(self, event):
        print(f'entry_left_get {self.entry_left.get()}')
        if self.controller:
            try:
                if self.entry_left_type.get() == '' or self.entry_left_type.get() == '.':
                    self.entry_right_type.set('?')
                    return
                entry_left_value = float(self.entry_left.get())
                self.controller.convert_left(entry_left_value)
            except ValueError as error: # TypeError as error:
                print(f'In class View, method name: change_entry_left {error}')

    def change_entry_right(self, event):
        print('entry right')
        if self.controller:
            try:
                if self.entry_right_type.get() == '' or self.entry_right_type.get() == '.':
                    self.entry_left_type.set('?')
                    return
                entry_right_value = float(self.entry_right.get())
                self.controller.convert_right(entry_right_value)
            except ValueError as error: # TypeError as error:
                print(f'In class View, method name: change_entry_right {error}')

    def label_swap_cliked(self, event):
        '''switch swap'''
        if self.controller:
            try:
                self.entry_left_type.set(1)
                if self.switch:
                    self.entry_right_type.set(1.609344)
                    self.label_left['text'] = 'miles (mi)'
                    self.label_right['text'] = 'kilometers (km)'
                    self.label_title['text'] = 'Convert Miles to Km'
                    self.switch = False
                else:
                    self.entry_right_type.set(0.62137119)
                    self.label_left['text'] = 'kilometers (km)'
                    self.label_right['text'] = 'miles (mi)'
                    self.label_title['text'] = 'Convert Km to Miles'
                    self.switch = True
            except ValueError as error: # TypeError as error:
                print(f'In class View, method name: label_swap_cliked {error}')

    def entry_right_value(self, value):
        self.entry_right_type.set(value) 

    def entry_left_value(self, value):
        self.entry_left_type.set(value)
    
    #  /* VALIDATE ENTRY
    def validate_left(self, value):
        ''' Validate entry left '''
        if re.search(r'[^\d \.]', value):
            return False

        if re.search(r' ', value):
            return False

        res = re.findall(r'\.', value)
        if len(res) > 1:
            self.entry_right_type.set('?')
            return False
        return True


    def validate_right(self, value):
        ''' Validate entry right '''
        if re.search(r'[^\d \.]', value):
            return False

        if re.search(r' ', value):
            return False

        res = re.findall(r'\.', value)
        if len(res) > 1:
            self.entry_left_type.set('?')
            return False
        return True
    # */ END Validate


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def convert_left(self, x):
        try:
            self.model.value = x
            print(x)
            if self.view.switch:
                res = self.model.km_to_mi()
                self.view.entry_right_value(res)
                print(f'km_to_mi: {res}')
            else:
                res = self.model.mi_to_km()
                self.view.entry_right_value(res)
                print(f'mi_to_km: {res}')
        except TypeError as error:
            print(f'Wow!!!In class Controller: {error}: {type(x)}')


    def convert_right(self, x):
        try:
            self.model.value = x
            if self.view.switch:
                res = self.model.mi_to_km()
                self.view.entry_left_value(res)
                print(f'mi_to_km: {res}')
            else:
                res = self.model.km_to_mi()
                self.view.entry_left_value(res)
                print(f'km_to_mi: {res}')
        except TypeError as error:
            print(f'Wow!!!In class Controller: {error}: {type(x)}')


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Hello converter!')
        self.geometry('400x400')
        
        model = Model(1)
        view = View(self)

        controller = Controller(model, view)
        
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()
