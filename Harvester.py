import requests
from bs4 import BeautifulSoup
import threading
import time
from colorama import init, Fore, Style
import ctypes
from queue import Queue
import os

def set_window_title(title):
    title_ansi = title.encode('ansi', 'ignore')
    ctypes.windll.kernel32.SetConsoleTitleA(title_ansi)

set_window_title('BwE Website Harvester')

version = "1.0.0"  

def print_banner():
    print(Fore.MAGENTA + "*-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*")
    print(Fore.MAGENTA + "|" + Fore.WHITE + "            __________          __________               " + Fore.MAGENTA + "|")
    print(Fore.MAGENTA + "|" + Fore.WHITE + "            \\______   \\ __  _  _\\_   ____/               " + Fore.MAGENTA + "|")
    print(Fore.MAGENTA + ":" + Fore.WHITE + "             |    |  _//  \\/ \\/  /|  __)_                " + Fore.MAGENTA + ":")
    print(Fore.MAGENTA + "." + Fore.WHITE + "             |    |   \\\\        //       \\               " + Fore.MAGENTA + ".")
    print(Fore.MAGENTA + ":" + Fore.WHITE + "  /\\_/\\      |______  / \\__/\\__//______  /               " + Fore.MAGENTA + ":")
    print(Fore.MAGENTA + "|" + Fore.WHITE + " ( O.o )            \\/" + Fore.MAGENTA + "  Web Harvester  " + Fore.WHITE + "\\/" + version + "           " + Fore.MAGENTA + "|")
    print(Fore.MAGENTA + "|" + Fore.WHITE + " (>   <)                                                 " + Fore.MAGENTA + "|")
    print(Fore.MAGENTA + "*-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*\n" + Style.RESET_ALL)

print_banner()

bruteforce_queue = Queue()

last_checked_file = "last_checked.txt"
successful_file = "successful.txt"
failed_file = "failed.txt"

def save_to_file(file_name, data):
    with open(file_name, "a") as file:
        file.write(data + "\n")

def bruteforce_db():
    while not bruteforce_queue.empty():
        value = bruteforce_queue.get()
        try:
            url = f'https://www.bwe.bwe/{value}'
            headers = {'User-Agent': 'Mozilla/5.0 (PlayStation; PlayStation 5/2.26) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15'} #https://deviceatlas.com/blog/list-of-user-agent-strings
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 404:
                
                print(f"Value: {value} Not Found (404). Skipping...", end='\r')
                
                save_to_file(failed_file, value)
                bruteforce_queue.task_done()
                continue
            if response.status_code == 403:
                print((Fore.RED + "Error 403: You were IP banned or rate limited! Session Ended - Retry Later\r" + Style.RESET_ALL))
                save_to_file(failed_file, value)
                input()
                os._exit(0)

            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            value_search_span = soup.select_one(".onion h1 span") #Put here the area you want to grab, in this example it is in the onion div class, a h1 header and within a span.
            value_description_p = soup.select_one(".onion p") #Do the same for the other value you want to grab. In this example its in the same onion div class but within a paragraph.

            value_search = value_search_span.text.strip() if value_search_span else "Value Not Found"
            value_description = value_description_p.text.strip() if value_description_p else "Description Not Found"

            result_line = f"Value: {value_search}, Description: {value_description}"
            print(Fore.GREEN + result_line + Style.RESET_ALL)
            save_to_file(successful_file, result_line)

        except requests.exceptions.RequestException as e:
            print(f"Request Error For {value}: {e}")
            save_to_file(failed_file, value)

        finally:
            # Update last checked code and mark task as done
            save_to_file(last_checked_file, value)
            bruteforce_queue.task_done()

def read_bruteforce_list_into_queue(file_name):
    try:
        with open(file_name, "r") as file:
            for line in file:
                bruteforce_queue.put(line.strip())
    except FileNotFoundError:
        print("A BruteForce Dictionary (list.txt) Required!")
        print("\nPress Enter to Exit...")
        input()
        os._exit(0)
    

bruteforce_list_filename = "list.txt"
read_bruteforce_list_into_queue(bruteforce_list_filename)

num_threads = 10  # Adjust according to your requirement
for _ in range(num_threads):
    threading.Thread(target=bruteforce_db).start()

bruteforce_queue.join() 
print("All tasks have finished.")
print("\nPress Enter to Exit...")
input()
os._exit(0)
