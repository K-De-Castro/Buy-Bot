import settings
import requests
import search_process
import buying_process
import concurrent.futures


class Process:
    def __init__(self, profile, lock, option=None):
        self.profile = profile
        self.option = option
        self.lock = lock
        self.search_processes = []

    def add_search(self, url, keywords, option):
        sprocess = None
        for search in self.search_processes:
            if search.base_url == url:
                sprocess = search
        if sprocess == None:
            sprocess = search_process.Searchprocess(url, keywords, self.lock, option)
            self.search_processes.append(sprocess)

        self.search_processes[-1].add_buy(buying_process.Buyingprocess(sprocess.id, self.profile, self.lock))


    def remove_search(self, index):
        self.search_processes.pop(index)

    def run(self):
        print(self.search_processes)
        while self.search_processes:
            for i in range(len(self.search_processes)):
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.submit(self.search_processes[i].run())




