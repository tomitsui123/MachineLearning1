import pandas as pd 
import os
import time
from datetime import datetime

path = "intraQuarter"

def Key_Stats(gather="Total Debt/Equity (mrq)"):
	statspath = path+ '/_KeyStats'
	
	stock_list = [x[0] for x in os.walk(statspath)]
	
	df = pd.DataFrame(columns = ['Date',
								 'Unix',
								 'Ticker',
								 'DE Ratio',
								 'Price',
								 "stock_p_change",
								 "SP500",
								 'sp500_p_change'])

	sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_SPY.csv")

	ticker_list=[]
	
	for each_dir in stock_list[1:]:

		each_file = os.listdir(each_dir)
		ticker = each_dir.split("/")[1]
		ticker_list.append(ticker)

		starting_stock_value = False
		starting_sp500_value = False
		
		if len(each_file) > 0:
			for file in each_file:
				date_stamp = datetime.strptime(file,'%Y%m%d%H%M%S.html')
				# print("file:",file)
				unix_time = time.mktime(date_stamp.timetuple())
				
				full_file_path = each_dir+'/'+file
				
				source = open(full_file_path,'r').read()
				try:
					value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])

					try:
						sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
						row = sp500_df[(sp500_df.index == sp500_date)]
						sp500_value = float(row["Adjusted Close"])
					except:
						sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
						row = sp500_df[(sp500_df.index == sp500_date)]
						sp500_value = float(row["Adjusted Close"])

					stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
					# print("stock_price:",stock_price,"ticker:", ticker)


					if not starting_stock_value:
						starting_stock_value = stock_price
					if not starting_sp500_value:
						starting_sp500_value = sp500_value



					stock_p_change = (stock_price - starting_stock_value)
					sp500_p_change = (sp500_value - starting_sp500_value)




					df = df.append({'Date':date_stamp,
									'Unix':unix_time,
									'Ticker':ticker,
									'DE Ratio':value,
									'Price':stock_price,
									'stock_p_change':stock_p_change,
									'sp500_p_change':sp500_p_change,
									"SP500":sp500_value}, ignore_index=True)
					print(file)
				except Exception as e:
					
					pass
			
	save = gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')
	print(save)
	df.to_csv(save)

Key_Stats()
print("Yea")