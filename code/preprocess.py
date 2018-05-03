import pandas as pd
from pandas import DataFrame

order_product = pd.read_csv("./order_products__train.csv",low_memory=False)
product = pd.read_csv("./products.csv",low_memory=False)
aisle = pd.read_csv("./aisles.csv",low_memory=False)
department = pd.read_csv("./departments.csv",low_memory=False)

product_result=DataFrame()
aisle_result=DataFrame()
department_result=DataFrame()

product_result= order_product.iloc[:,[0,1]][order_product.reordered == 1]
product_result['name']=None

order_row = order_product.iloc[:,0].size

aisle_result['order_id']=product_result['order_id']
department_result['order_id']=product_result['order_id']
aisle_result['aisle_id']=None
aisle_result['name']=None
department_result['department_id']=None
department_result['name']=None

for i in range(order_row):
	if order_product.loc[i,'reordered'] == 1:
		print i
		n = product_result.loc[i,'product_id']
		product_result.loc[i,'name'] = product.loc[n-1,'product_name']
		aisle_id = product.loc[n-1,'aisle_id']
		department_id = product.loc[n-1,'department_id']
		aisle_result.loc[i,'aisle_id'] = aisle.loc[aisle_id-1,'aisle_id']
		aisle_result.loc[i,'name'] = aisle.loc[aisle_id-1,'aisle']
		department_result.loc[i,'department_id'] = department.loc[department_id-1,'department_id']
		department_result.loc[i,'name'] = department.loc[department_id-1,'department']

product_result.to_csv("./result/product.csv",index=False)
aisle_result.to_csv("./result/aisle.csv",index=False)
department_result.to_csv("./result/department.csv",index=False)
