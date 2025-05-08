#!/usr/bin/env python3

from googlesearch import search
from src import banner
from time import sleep
import requests
import random
import threading as trd
import sys

### Edit This Beforehand ###
site           = "your site here"
wordlist_file  = "./src/wordlists.txt"
output_file    = "./out/out.txt"
search_res     = 12
search_tick    = 0
chunk_size     = 10

domain = f'site:{site}'
with open(wordlist_file, 'r') as word_list:
    word_list = word_list.read().splitlines()

def split_list(input_list, chunk_size):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def print_stats():
    stats = f'''________________________________________
                   |
[*] Search on site | {site}
[*] Using wordlist | {wordlist_file}
[*] Output file    | {output_file}
[*] Search Result  | {search_res}    
[*] Search Tick    | {search_tick}
[*] Word Chunk     | {chunk_size}
___________________|____________________
'''
    return stats

def search_in_google(word_chunk):   
    for keyword in word_chunk:
        query = f'{domain} {keyword}'
        search_title = f"[*] searching for: {query}"
        return search_title
        print(search_title)

        search_req = search(query, num_results=search_res, sleep_interval=3)
        for result in search_req:
            if keyword is not None:                      
                link = f'[{keyword}]: {result}'
                return link
            else:
                pass
            sleep(search_tick)
        print('')

# Enabling multiThread for CAPTCHA evasion
def multi_thread():
    word_chunk = split_list(word_list, chunk_size)
    th1 = trd.Thread(target=search_in_google(word_chunk[0]))
    th2 = trd.Thread(target=search_in_google(word_chunk[1]))
    th3 = trd.Thread(target=search_in_google(word_chunk[2]))
    th4 = trd.Thread(target=search_in_google(word_chunk[3]))

    th1.start()
    th2.start()
    th3.start()
    th4.start()

    th1.join()
    th2.join()
    th3.join()
    th4.join()

    
def write_output(output):
    with open(output, 'w') as autput:
        autput.write(banner.b1)
        autput.write(print_stats())
        autput.write(search_in_google(word_list))
    
    print(banner.b2)
    print(print_stats())
    sleep(2)
    print(search_in_google(word_list))


def main():
    try:
        write_output(output_file)
    except requests.exceptions.HTTPError:
        print("")
        print("The operation is blocked by CAPTCHA :(")
    except KeyboardInterrupt:
        print("")
        print("Process terminated by user")
    

main()
