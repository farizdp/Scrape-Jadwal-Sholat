import requests, telepot, os
import prettytable as pt
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
id_telegram = os.getenv('ID_TELEGRAM')
token = os.getenv('TOKEN')
bot = telepot.Bot(token)

link = 'https://www.jadwalsholat.org/adzan/monthly.php?id=310'
r = requests.get(link)
if r.status_code == 200:
    html = BeautifulSoup(r.content, "html.parser")
    kota = html.select_one('option[selected]').string
    bulan = html.h2.string
    jadwal = html.find_all('tr', class_="table_highlight")
    results = []
    for row in jadwal:
        data = row.find_all('td')
        row_values = []
        for d in data:
            row_values.append(d.get_text(strip=True))
        results.append(row_values)
    table = pt.PrettyTable()
    table.title = results[0][0] + ' ' + bulan
    table.field_names = ['Waktu', 'Jam']
    table.align['Waktu'] = 'l'
    data = [
        ('Shubuh', results[0][2]),
        ('Dzuhur', results[0][5]),
        ('Ashr', results[0][6]),
        ('Maghrib', results[0][7]),
        ('Isya', results[0][8]),
    ]
    for waktu, jam in data:
        table.add_row([waktu, jam])
    text = "Jadwal sholat *{0}*\n\n```{1}```".format(kota, table)
else:
    text = "Not found!"

bot.sendMessage(id_telegram, text, 'Markdown')