#!/usr/bin/env python3

from googlesearch import search
from src import banner
from time import sleep
import requests
import argparse
import threading as trd
import sys



parser = argparse.ArgumentParser(prog="pSentinel.py", usage='python3 %(prog)s [options]')
parser.add_argument("-u", type=str, help="your domain here")    
parser.add_argument("-w", type=str, help="your wordlist here") 
args = parser.parse_args()                  

### Edit This Beforehand ###
site           = args.u
wordlist_file  = args.w
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
    print(banner.b2)
    print(f'''
____________________________________________
                   |
[*] Search on site | {site}
[*] Using wordlist | {wordlist_file}
[*] Output file    | {output_file}
[*] Search Result  | {search_res}    
[*] Search Tick    | {search_tick}
[*] Word Chunk     | {chunk_size}
___________________|________________________
''')

def search_in_google(word_chunk):   
    for keyword in word_chunk:
        query = f'{domain} {keyword}'
        search_title = f"[*] searching for: {query}"
        print(search_title)

        search_req = search(query, num_results=search_res, sleep_interval=3)
        for result in search_req:                    
            link = f'[{keyword}]: {result}'
            print(link)
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

    
def write_output(word_list):
    print_stats()
    sleep(2)
    search_in_google(word_list)

def main():
    try:
        write_output(word_list)
    except requests.exceptions.HTTPError:
        print("")
        print("The operation is blocked by CAPTCHA :(")
    except KeyboardInterrupt:
        print("")
        print("Process terminated by user")
    except requests.exeptions.ReadTimeout:
        print("Request timeout")
    
main()
