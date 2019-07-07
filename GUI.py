from tkinter import *
from tkinter.ttk import *

class GUI(object):

    def __init__(self):
        self.window = Tk()
        self.window.title("Earcon Setup")

        uriLabel = Label(self.window, text="URI")
        uriLabel.grid(column=0, row=0)
        self.uriInput = Entry(self.window, width=68)
        self.uriInput.grid(columnspan=3, column=1, row=0, sticky='w')

        # Select which type of earcon you want to make
        # 1. Frequency
        # 2. Length
        # 3. Frequency + Length
        # TODO: 4. Frequency + Volume
        # TODO: 5. Frequency + Length + Volume

        earconTypeOptionsLabel = Label(self.window, text="Earcon Type")
        earconTypeOptionsLabel.grid(column=0, row=1)

        self.earconTypeOption = Combobox(self.window)
        self.earconTypeOption['values'] = ("1: Frequency", "2: Length", "3: Frequency & Length")
        self.earconTypeOption.current(2)
        self.earconTypeOption.grid(column=1, row=1)

        motiveTypeOptionsLabel = Label(self.window, text="Earcon Motive")
        motiveTypeOptionsLabel.grid(column=0, row=2)

        self.motiveTypeOptions = []
        for i in range(3):
            self.motiveTypeOptions.append(Combobox(self.window))
            self.motiveTypeOptions[i]['values'] = ("nodes",
                                                   "in_degree min",
                                                   "in_degree max",
                                                   "in_degree mean",
                                                   "out_degree min",
                                                   "out_degree max",
                                                   "out_degree mean")
            self.motiveTypeOptions[i].current(0)
            self.motiveTypeOptions[i].grid(column=i+1, row=2)

        btn = Button(self.window, text="Generate", width=19, command=self.onclick)
        btn.grid(column=3, row=3)

        self.window.mainloop()

    def onclick(self):
        global result
        self.uri = self.uriInput.get()
        self.type = self.earconTypeOption.get()
        self.motiveOrder = []

        for i in self.motiveTypeOptions:
            value = i.get()
            self.motiveOrder.append(value)

        self.window.destroy()

    def retrieveInput(self):
        return self.uri

    def retrieveEarconType(self):
        return self.type

    def retrieveMotiveOrder(self):
        return self.motiveOrder
