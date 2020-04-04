from tkinter import *


class NewTask(object):

    root = None

    def __init__(self):
        """
        msg = <str> the message to be displayed
        dict_key = <sequence> (dictionary, key) to associate with user input
        (providing a sequence for dict_key creates an entry for user input)
        """

        self.top = Toplevel(NewTask.root)

        frm = Frame(self.top, borderwidth=4, relief='ridge')

        frm.pack(fill='both', expand=True)

        label = Label(frm, text="New Task")
        label.pack(padx=4, pady=4)

        b_cancel = Button(frm, text='Cancel')
        b_cancel['command'] = self.top.destroy
        b_cancel.pack(padx=4, pady=4)
