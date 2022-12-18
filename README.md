# Mi az a titleminer?

A titleminer egy eszköz a címek kinyerésére híroldalakról.
Ez egy parancssori eszköz, amely az URL-ek listáját veszi be bemenetként, és egy címlistát ad ki.
Python nyelven íródott, és a [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/) könyvtárat használja a HTML elemzéséhez.

# Telepítés

A titleminerhez Python 3.10 és poetry szükséges.

A titleminer telepítéséhez futtassa a következő parancsokat:

     poetry install

# Használat

A titleminer felveszi az URL-ek listáját egy szöveges fájlban, és kiírja a konzolba a weboldalak címében található leggyakoribb szavakat.
    
    poetry run titleminer feeds.txt

Lehetőség van wordcloud létrehozására a --wordcloud opcióval.

    poetry run titleminer feeds.txt --wordcloud

További lehetőségekért tekintse meg a súgót:

     poetry run titleminer --help