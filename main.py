import settings
import multiprocessing
from tkinter import *
from gui import newtaskdialog
from gui import newtask as nt
from tkinter import simpledialog
from search_process import Searchprocess
from buying_process import Buyingprocess
import json

with open("user_settings.json", "r") as jsonFile:
    print(jsonFile)
    data = json.load(jsonFile)
print(data)
# initializing
# base_url = settings.base_url  # url of shopify store homepage
# catalog = settings.catalog  # url for all items of shopify store
# checkout_info = settings.check_info  # user info for checkout
# lock = multiprocessing.Lock()
#
# app = Tk()
#
#
# ntask = newtaskdialog.NewTask
# ntask.root = app
#
# newtask_btn = Button(app, text="Add Task", command=lambda: ntask())
# newtask_btn.pack()
#
# app.title("Swift")
# app.geometry('700x350')
# # starts the app
# app.mainloop()

# process = Searchprocess(base_url, settings.keywords)
# for i in range(1):
#     process.add_buy(Buyingprocess(process.id, settings.check_info, lock))
# #
# # for buy in process.buys:
# #     print(buy.id)
# process.run()
