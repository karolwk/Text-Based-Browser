import sys
import os
import re
import requests
from bs4 import BeautifulSoup
from collections import deque
from colorama import init

class Files:

    @staticmethod
    def save_file(file_name: str, dir: str, inp: str, encode: str) -> None:
        with open(f"{dir}\\{file_name}.txt", "w", encoding=encode) as file:
            file.write(inp)

    @staticmethod
    def load_file(file_name: str, dir: str, encode: str) -> str:
        output = ""
        with open(f'{dir}\\{file_name}.txt', "r", encoding=encode) as file:
            for line in file:
                output += line
        return output


class Browser:
    def __new__(cls, args):
        """ Validation of starting arguments"""
        if len(args) != 2:
            print("Not enough arguments or too many of them!")
            return None
        else:
            return object.__new__(cls)

    def __init__(self, args):
        self.args = args
        self.dir_name = self.args[1]
        self.mk_dir()
        self.saved_urls = []
        self.stack = deque()
        self.prev_www = ""
        self.encoding = "utf-8"

    def back(self, operation="POP", www=""):
        """Putting previous visited page on stack, to go back and visit it once more"""
        if operation == "PUSH" and www != "":
            self.stack.append(www)
        else:
            if len(self.stack) > 0:
                return self.stack.pop()
        return


    def check_valid_address(self, www) -> bool:
        """Check if the user has entered a valid URL. It must contain at least one dot."""
        if re.findall("^[a-zA-Z0-9]+[a-zA-Z0-9\.\-]+\.[a-zA-Z]+$", www):
            return True
        return False

    def mk_dir(self):
        """Making dir with starting arguments if it doesn't exist"""
        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)
        else:
            pass
            # print("Directory " , self.dir_name ,  " already exists")

    def main(self):
        while True:
            inp = input()
            if inp == "exit":
                break
            if inp == "back":
                print(self.get_www_content(self.back()))
                continue
            if self.check_valid_address(inp):
                self.back("PUSH", self.prev_www)
                print(self.get_www_content(inp))
                Files.save_file(self.slice_url(inp), self.dir_name, self.get_www_content(inp), self.encoding)
                self.saved_urls.append(self.slice_url(inp))
                self.prev_www = inp
            elif inp in self.saved_urls:
                print(Files.load_file(inp, self.dir_name, self.encoding))
            else:
                print("Error: Incorrect URL")


    def slice_url(self, str_):
        """Returns url without last dot and everything that comes after it."""
        for i in range(len(str_) - 1, 0, -1):
            if str_[i] == ".":
                return str_[:i]

    def get_www_content(self, inp):
        """ Return content of the page, only whitelisted tags, also hiperlinks are colored in blue"""
        try:
            init()
            r = requests.get(f'https://{inp}', timeout=10)
            soup = BeautifulSoup(r.content, 'html.parser')
            finders = soup.find_all(["title", "a", "p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "span"])
            result = ""
            for i in finders:
                if i.string is not None:
                    if i.name == "a":
                        result += f"\033[34m{i.string.strip()}\033[39m\n"
                    else:
                        result += f'{i.string.strip()}\n'
            return result
        except:
            print('Error')
            return 0


browser = Browser(sys.argv)
browser.main()