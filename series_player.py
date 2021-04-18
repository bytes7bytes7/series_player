import requests, ctypes, lxml.html
from bs4 import BeautifulSoup

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True )

print('\n\n')
print('\033[34m{}'.format('╔═══╗╔═══╗╔═══╗╔══╗╔═══╗╔═══╗     ╔═══╗╔╗───╔═══╗╔╗──╔╗╔═══╗╔═══╗'))
print('\033[35m{}'.format('║╔═╗║║╔══╝║╔═╗║╚╣─╝║╔══╝║╔═╗║     ║╔═╗║║║───║╔═╗║║╚╗╔╝║║╔══╝║╔═╗║'))
print('\033[36m{}'.format('║╚══╗║╚══╗║╚═╝║─║║─║╚══╗║╚══╗     ║╚═╝║║║───║║─║║╚╗╚╝╔╝║╚══╗║╚═╝║'))
print('\033[37m{}'.format('╚══╗║║╔══╝║╔╗╔╝─║║─║╔══╝╚══╗║     ║╔══╝║║─╔╗║╚═╝║─╚╗╔╝─║╔══╝║╔╗╔╝'))
print('\033[38m{}'.format('║╚═╝║║╚══╗║║║╚╗╔╣─╗║╚══╗║╚═╝║     ║║───║╚═╝║║╔═╗║──║║──║╚══╗║║║╚╗'))
print('\033[39m{}'.format('╚═══╝╚═══╝╚╝╚═╝╚══╝╚═══╝╚═══╝     ╚╝───╚═══╝╚╝─╚╝──╚╝──╚═══╝╚╝╚═╝'))
print('\033[39m{}'.format(' '*50+'by bytes7bytes7'))

url='https://hd.seasonlast.ru/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate',
    'Connection':'keep-alive',
    'Content-Type': 'text/html; charset=utf-8',
    'DNT':'1'
}

moviename = input('\n\nНазвание сериала: ')

session = requests.session()
resp = session.get(url, headers=headers)

page = lxml.html.fromstring(resp.content)
form = page.forms[0]
form.fields['search'] = moviename

html = session.post(url, data=form.form_values()).text
parsed_html = BeautifulSoup(html,"html.parser")
movies = parsed_html.body.find_all('div',attrs={'class':'film-item'})

index=None
movies_data=[]
while 1:
	movies_data=[]
	if len(movies)==0:
		input('\nНет результатов :(')
		raise SystemExit
	print('\nРезультаты поиска:')
	for i in range(len(movies)):
		title = movies[i].find('span',attrs={'class':'link_film'}).text
		movie_href = movies[i].find('a')['href']
		print(str(i+1)+') '+title)
		movies_data.append([title,movie_href])
	if len(movies)==1:
		index=1
		break
	try:
		index=int(input('\nВаш выбор: '))
		if not (0<index<=len(movies)):
			raise Exception('Индекс вне диапазона')
		break
	except Exception as e:
		print('\nОшибка:\n'+str(e)+'\n\n')
		print('Попробуйте еще раз...')

try:
	html = session.get(movies_data[index-1][1]).text
	parsed_html = BeautifulSoup(html,"html.parser")
	player_link = parsed_html.find('div',attrs={'id':'preroll'}).find('div').find('iframe')['src']
except:
	input('\nВидео не доступно :(')
	raise SystemExit

html = session.get(player_link).text
html = html.replace('ads: adsConfig,','ads: null,')

with open('index.html', 'w',encoding='utf-8') as f:
	f.write(html)

input('\nОткройте файл index.html с помощью браузера. Приятного просмотра :)')