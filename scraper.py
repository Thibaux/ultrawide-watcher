import os
import requests
from bs4 import BeautifulSoup
import smtplib
from decouple import config

priceWanted = 340;
verkopers = []


def Bol():
	bolsMonitor = []

	url = 'https://bol.com/nl/p/lg-35wn65c-qhd-curved-ultrawide-monitor-35-inch/9300000005464338/?s2a=#productTitle'
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.11 Safari/537.36'}
	page = requests.get(url, headers = headers)
	soup = BeautifulSoup(page.content, 'html.parser')

	lg_35WN65C = soup.find('span', {'class': 'promo-price'}).get_text()
	Bol_lg35WN65C_price = int(lg_35WN65C[:6])
	bolsMonitor.append(["Bol_lg35WN65C", Bol_lg35WN65C_price, url])


	url = 'https://www.bol.com/nl/p/philips-342b1c-full-hd-curved-monitor-34-inch/9200000122087022/?bltgh=oFPH4EnX9MqYQ1Kn0QJG9w.p9RidLfagZs7mKHdqgVNMw_0_48.51.ProductImage'
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.11 Safari/537.36'}
	page = requests.get(url, headers = headers)
	soup = BeautifulSoup(page.content, 'html.parser')

	Philips_342B1C = soup.find('span', {'class': 'promo-price'}).get_text()
	Philips_342B1C_price = int(Philips_342B1C[0:3])
	bolsMonitor.append(["Philips_342B1C", Philips_342B1C_price, url])
	
	return bolsMonitor


def Coolblue():
	url = 'https://www.coolblue.nl/product/871264/lg-35wn65c.html'
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.11 Safari/537.36'}
	page = requests.get(url, headers = headers)
	soup = BeautifulSoup(page.content, 'html.parser')

	lg_35WN65C = soup.find('span', {'class': 'sales-price js-sales-price'}).get_text()
	
	Coolblue_lg35WN65C_price = int(lg_35WN65C[:3]);

	return ["Coolblue_lg35WN65C", Coolblue_lg35WN65C_price, url]


def threshold():
	global priceWanted;
	global verkopers
	alleVerkopers = [];

	alleVerkopers.extend([Bol()[0], Bol()[1], Coolblue()])

	for verkoper in alleVerkopers:
		if verkoper[1] <= priceWanted:
			verkopers += verkoper;
			SendMail();
	
	quit();


def SendMail():
	global priceWanted;
	global verkopers
	senderAdres = config('EMAIL_RECIVER')
	senderPassword = config('EMAIL_SENDER_PASSWORD')
	reciverAdres = config('EMAIL_RECIVER')

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	server.login(senderAdres, senderPassword)

	subject = "Een van de ultrawides is in prijs gedaald!"
	body = f"""
	Yoo,

	De prijs van {verkopers[0]} is {verkopers[1]}!
	Dat is minder dan {priceWanted}, zoals je kan zien...
	Link: {verkopers[2]}

	Joee
	"""
	msg = f"Subject: {subject}\n\n{body}"

	server.sendmail(
		senderAdres,
		reciverAdres,
		msg
	)

	print('send')
	server.quit()


threshold();
