"""
MUHAMMAD HANIF
Web         : http://hanifmu.com
Email       : moehammadhanif[@]gmail.com
Telegram    : https://t.me/hanifmu
"""

import xml.etree.ElementTree as ET
import textwrap
import filecmp
import os

os.chdir("/opt/info-gempa-bumi-telegram/dirasakan")
os.system("wget --no-check-certificate -N http://data.bmkg.go.id/gempadirasakan.xml -O gempadirasakan.xml")


def data_gempa(xml):
    data_gempa = {}

    for data in xml.findall('Gempa'):
        data_gempa['tanggal'] = data.find("Tanggal").text
        data_gempa['posisi'] = data.find("Posisi").text
        data_gempa['magnitude'] = data.find("Magnitude").text
        data_gempa['kedalaman'] = data.find("Kedalaman").text
        data_gempa['keterangan'] = data.find("Keterangan").text
        data_gempa['dirasakan'] = data.find("Dirasakan").text

        break

    return data_gempa


def peta_gempa(tanggal):
    tanggal_waktu = tanggal.split('-')
    url_tanggal = tanggal_waktu[0][6:11] + \
        tanggal_waktu[0][3:5] + tanggal_waktu[0][:2]
    url_waktu = tanggal_waktu[1][:2] + \
        tanggal_waktu[1][3:5] + tanggal_waktu[1][6:8]
    url = 'https://ews.bmkg.go.id/tews/data/' + url_tanggal + url_waktu + '.mmi.jpg'

    return url


def tulis_file(file, data):
    file = open(file, "w")
    file.write(data + "\n")
    file.close()


data = data_gempa(ET.parse('gempadirasakan.xml').getroot())

tulis_file("gempa_baru.txt", peta_gempa(data['tanggal']))

if filecmp.cmp('gempa_lama.txt', 'gempa_baru.txt'):
    print(0)
else:
    os.system("wget --no-check-certificate -N " +
              peta_gempa(data['tanggal']) + " -O gempa_dirasakan.jpg")

    pesan = """
    *.:: GEMPA BUMI DIRASAKAN ::.*

    *Tanggal* : {}
    *Posisi* : {}
    *Magnitudo* : {}
    *Kedalaman* : {}
    *Keterangan* : {}
    *Dirasakan* : {}

    Sumber data: [BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)](https://www.bmkg.go.id/)
    """.format(data['tanggal'], data['posisi'], data['magnitude'], data['kedalaman'], data['keterangan'], data['dirasakan'])

    tulis_file("pesan.txt", textwrap.dedent(pesan))

    tulis_file("gempa_lama.txt", peta_gempa(data['tanggal']))

    os.system("cat pesan.txt | telegram-send --format markdown --stdin")
    os.system("telegram-send -i gempa_dirasakan.jpg")
