"""
MUHAMMAD HANIF
Web         : http://hanifmu.com
Email       : moehammadhanif@gmail.com
Telegram    : https://t.me/hanifmu
"""

import untangle
import filecmp
import os
import textwrap


def tulis_file(file, data):
    file = open(file, "w")
    file.write(data + "\n")
    file.close()


os.chdir("/opt/info-gempa-bumi-telegram/magnitudo-5")
autogempa = untangle.parse('http://data.bmkg.go.id/autogempa.xml')

tanggal_waktu = autogempa.Infogempa.gempa.Tanggal.cdata + \
    " " + autogempa.Infogempa.gempa.Jam.cdata

tulis_file("gempa_baru.txt", tanggal_waktu)

if filecmp.cmp('gempa_lama.txt', 'gempa_baru.txt'):
    print("tidak ada gempa")
else:
    os.system("wget -N http://data.bmkg.go.id/eqmap.gif -O eqmap.gif")

    koordinat = autogempa.Infogempa.gempa.Lintang.cdata + \
        " " + autogempa.Infogempa.gempa.Bujur.cdata
    magnitudo = autogempa.Infogempa.gempa.Magnitude.cdata
    kedalaman = autogempa.Infogempa.gempa.Kedalaman.cdata
    wilayah1 = autogempa.Infogempa.gempa.Wilayah1.cdata
    wilayah2 = autogempa.Infogempa.gempa.Wilayah2.cdata
    wilayah3 = autogempa.Infogempa.gempa.Wilayah3.cdata
    wilayah4 = autogempa.Infogempa.gempa.Wilayah4.cdata
    wilayah5 = autogempa.Infogempa.gempa.Wilayah5.cdata
    potensi = autogempa.Infogempa.gempa.Potensi.cdata

    pesan = """
    *.:: GEMPA BUMI MAGNITUDO >= 5 ::.*

    *Waktu* : {}
    *Magnitudo* : {}
    *Kedalaman* : {}
    *Potensi* : {}
    *Wilayah* :
     - {}
     - {}
     - {}
     - {}
     - {}
    *Koordinat* : {}

    Sumber data: [BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)](https://www.bmkg.go.id/)
    """.format(tanggal_waktu, magnitudo, kedalaman, potensi, wilayah1, wilayah2, wilayah3, wilayah4, wilayah5, koordinat)

    tulis_file("pesan.txt", textwrap.dedent(pesan))

    tulis_file("gempa_lama.txt", tanggal_waktu)

    os.system("cat pesan.txt | telegram-send --format markdown --stdin")
    os.system("telegram-send -i eqmap.gif")
