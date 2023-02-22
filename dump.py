# Recode aja gpp
import os, re, requests, random, json, time, sys
from time import sleep

class Main:
	def __init__(self):
		self.id = []
		self.loop = 0
		try:
			self.cookie = open("data/.cookies.log","r").read()
			self.token = open("data/.token.log","r").read()
			try:
				url = requests.get("https://graph.facebook.com/me?fields=id,name&access_token="+self.token,cookies={"cookie":self.cookie})
				nm_ = json.loads(url.text)["name"]
				id_ = json.loads(url.text)["id"]
				self.menu(id_,nm_,)
			except KeyError:
				self.login()
			except requests.exceptions.ConnectionError:
				print ('Koneksi jaringan tidak stabil')
				exit()
		except FileNotFoundError:
			self.login()
	def login(self):
		os.system("clear")
		cookie = input('Masukan cookies: ')
		try:
			headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','Cookie': cookie}
			url = requests.get('https://web.facebook.com/adsmanager?_rdc=1&_rdr', headers = headers)
			cari = re.findall('act=(.*?)&nav_source', url.text)
			if len(cari) == 0:
				print ('Login gagal coba ganti cookienya')
				sleep(3);self.login()
			else:
				for xenz in cari:
					web = requests.get(f'https://web.facebook.com/adsmanager/manage/campaigns?act={xenz}&nav_source=no_referrer', headers = headers)
					token = re.search('(EAAB\w+)', web.text).group(1)
					open("data/.token.log","w").write(token)
					open("data/.cookies.log","w").write(cookie)
				cek = requests.get("https://graph.facebook.com/me?fields=id,name&access_token="+token, cookies={"cookie":cookie})
				nama = json.loads(cek.text)["name"]
				print('Login sebagai '+nama);sleep(1.5)
				Main()
		except (Exception,AttributeError,KeyError):
			print ('Login gagal coba ganti cookienya')
			sleep(3);self.login()
	def menu(self, idku, nmku):
		os.system('clear')
		teks = f'''[•] Nama: {nmku}\n[•] Id: {idku}\n[•] Masukan id: '''
		user = input(teks)
		try:
			header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0"}
			req = requests.get("https://graph.facebook.com/v15.0/"+user+"?fields=friends.limit(5000){id,name}&access_token="+self.token,cookies={"cookie": self.cookie},headers=header).json()
			for res in req['friends']['data']:
				try:self.id.append(res['id'])
				except:continue
			self.tanya()
		except (KeyError,IOError):
			print ('[•] Id tidak publik')
	def tanya(self):
		print ('''[1] 10001      [6] 10006
[2] 10002      [7] 10007
[3] 10003      [8] 10008
[4] 10004      [9] 10009
[5] 10005      [0] 10000''')
		pilih = input('[•] Pilih id yg ingin di dump: ')
		if pilih =='1':self.dump_lagi('1')
		if pilih =='2':self.dump_lagi('2')
		if pilih =='3':self.dump_lagi('3')
		if pilih =='4':self.dump_lagi('4')
		if pilih =='5':self.dump_lagi('5')
		if pilih =='6':self.dump_lagi('6')
		if pilih =='7':self.dump_lagi('7')
		if pilih =='8':self.dump_lagi('8')
		if pilih =='9':self.dump_lagi('9')
		if pilih =='0':self.dump_lagi('0')
	def dump_lagi(self,target):
		print (f'[•] Hasil dump tersimpan di: /sdcard/dump/1000{target}.txt\n[•] Klik ctrl z untuk berhenti dump')
		for user in self.id:
			try:
				header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0"}
				req = requests.get("https://graph.facebook.com/v15.0/"+user+"?fields=friends.limit(5000){id,name}&access_token="+self.token,cookies={"cookie": self.cookie},headers=header).json()
				for res in req['friends']['data']:
					sys.stdout.write(f'\r[•] Mengumpulkan id: {self.loop}')
					try:
						inpo = res['id']
						if inpo[0:5] == f'1000{target}':
							open(f'/sdcard/dump/1000{target}.txt','a').write(res['id']+'|'+res['name']+'\n')
							self.loop+=1
						else:continue

					except:
						continue
			except (KeyError,IOError,AttributeError):continue

if __name__=='__main__':
	try:os.mkdir('data')
	except:pass
	try:os.mkdir('/sdcard/dump')
	except:pass
	Main()
