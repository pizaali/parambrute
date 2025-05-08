import os
import sys
import requests
import urllib3
import argparse
from colorama import init, Fore


parser = argparse.ArgumentParser(description="Please use a valid parameter!")
parser.add_argument('-u', type=str, help="Target url.", default="")
parser.add_argument('-f', type=str, help="File name.", default="")
args = parser.parse_args()

init()
urllib3.disable_warnings()


def get_start_size(url):
    start_size = 0
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6301.219',
        'Referer': url,
        'Origin': url
    }
    try:
        res = requests.post(url=url, headers=header, verify=False, timeout=10)
    except Exception as e:
        return start_size
    else:
        return len(res.content)


def check_param(url, param, filename, start_size):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6301.219',
        'Referer': url,
        'Origin': url
    }
    data = {
        f'{param}': f'{filename}'
    }
    check_url = f'{url}?{param}={filename}'
    try:
        res = requests.post(url=check_url, headers=header, data=data, verify=False, timeout=10)
    except Exception as e:
        pass
    else:
        if res.status_code == 200 and len(res.content) != start_size:
            print(Fore.GREEN + f'[200][{len(res.content)}] {check_url}')
        else:
            pass


def read_file(filename):
    lines = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.strip() not in lines:
                lines.append(line.strip())
    return lines


def run():
    if os.path.exists('data/path_param.txt') and os.path.getsize('data/path_param.txt') != 0:
        params = read_file(filename='data/path_param.txt')
        total = len(params)
        init_size = get_start_size(url=args.u)
        print(Fore.GREEN + f'Initial size: {init_size}')
        for index, param in enumerate(params):
            print(Fore.WHITE + f'[{index + 1}/{total}] {param}')
            check_param(url=args.u, param=param, filename=args.f, start_size=init_size)
    else:
        print(Fore.RED + '[-] Params file is not exist or content is empty!')
        sys.exit()


if __name__ == '__main__':
    run()