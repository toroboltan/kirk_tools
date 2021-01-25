import requests
import pandas as pd

vista_simple = '111'
vista_full = '152&c='+','.join([str(s) for s in list(range(0,71))])

url = f'https://finviz.com/screener.ashx?v={vista_full}&f=an_recom_strongbuy,fa_epsyoy1_high,ind_biotechnology&ft=2'

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

print(url)