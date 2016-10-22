# Youtube Scikit Learn Machine Learning Tutorial with Python p. 7
import pandas as pd 
import os
import time
from datetime import datetime

path = "source/"

def Key_Stats(gather="Current Ratio (mrq)"):
	statpath = path +  '_KeyStats'
	each_stockname = [x[0] for x in os.walk(statpath)]
	for stockpath in each_stockname[1:]:
		each_file = os.listdir(stockpath)
		if len(each_file) > 0:
			for file in each_file:
				print(stockpath)
				full_file_path = stockpath + '/' + file
				sourcecode = open(full_file_path,'r').read()
				value = sourcecode.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
				print (value)
Key_Stats()