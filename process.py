import settings
import requests
import concurrent.futures

class Process:
    def __init__(self, profile, search_processes, option=None):
        self.profile = profile
        self.option = option
        self.search_processes = search_processes

    def add_search(self, search):
        self.search_processes.append(search)

    def remove_search(self, index):
        self.search_processes.pop(index)

    def run(self):
        while self.search_processes:
            for i in range(len(self.search_processes)):
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.submit(self.search_processes[i].run())




