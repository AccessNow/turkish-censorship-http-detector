#!/usr/bin/python
#This script written entirely by Access Technologist Samir Allous
import socket
from sys import argv, exit
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument("-u", help="the URL to test",metavar="url",required=True)
parser.add_argument("-H", help="the host field in the http header",metavar="host")
parser.add_argument("-p", help="the proxy ip:port(http or https proxy)",metavar="proxy")
parser.add_argument("-t", help="timeout, default is 10 secs",metavar="timeout", default="10", type=float)
parser.add_argument("-f", help="the output file", metavar="file")
args = parser.parse_args()

s = requests.Session()
s1 = requests.Session()
status = True
n = 0
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"})
while(status):
  n = n + 1
  if args.H is not None: s.headers.update({'Host': args.H})
  try:
    if args.p is not None:
      proxies = {
        "http": "http://" + args.p,
        "https": "http://" + args.p,
      }
      ip =  s1.get("http://bot.whatismyipaddress.com/", proxies=proxies, timeout=10).content
      if (n == 1): print "\n[*] My IP: " + ip
      res = s.get(args.u, proxies=proxies, timeout=args.t, verify=False)
    else:
      ip =  s1.get("http://bot.whatismyipaddress.com/", timeout=10).content
      if (n == 1): print "\n[*] My IP: " + ip
      res = s.get(args.u, timeout=args.t, verify=False)
    status = False
    if args.f is not None:
      f = open(args.f,"w")
      f.write(res.content)
      f.close()
    else:
      print "[*] Response content: \"" + str(res.content) + "\""
    print "[*] Response header: " + str(res.headers)
    print "[*] Response code: " + str(res)
  except socket.timeout:
    print "[*] Socket timeout"
    status = True
  except requests.exceptions.Timeout:
    print "[*] Timeout"
    status = False
  except requests.exceptions.ConnectionError as e:
    print "[*] ERROR: " + str(e)
    status = True
  except requests.exceptions.TooManyRedirects:
    print "[*] Too many redirects"
    status = False
  except KeyboardInterrupt:
    print
    exit(0)
