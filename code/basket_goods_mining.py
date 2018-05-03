import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from collections import defaultdict, Iterable
from Apriori import Apriori
from pandas import  DataFrame
from ast import literal_eval

csv_path = 'goods.csv'

# handle department.csv
# result_path = 'department_result.txt'
# data = pd.read_csv('department.csv')
# data_merged = data.groupby('order_id').agg({'name':lambda x: ','.join(x)})
# data_merged.name = data_merged.name.str.replace("\"","")
# data_merged['name'].to_csv(csv_path)
# dataset = csv.reader(open(csv_path, "r"))
# minSup = 0.03
# minConf = 0.88

# handle aisle.csv
# result_path = 'aisle_result.txt'
# data = pd.read_csv('aisle.csv')
# data_merged = data.groupby('order_id').agg({'name':lambda x: ','.join(x)})
# data_merged.name = data_merged.name.str.replace("\"","")
# data_merged['name'].to_csv(csv_path)
# dataset = csv.reader(open(csv_path, "r"))
# minSup = 0.02
# minConf = 0.7

# handle product.csv
result_path = 'product_result.txt'
data = pd.read_csv('product.csv')
data_merged = data.groupby('order_id').agg({'name':lambda x: ','.join(x)})
data_merged.name = data_merged.name.str.replace("\"","")
data_merged['name'].to_csv(csv_path)
dataset = csv.reader(open(csv_path, "r"))
minSup = 0.01
minConf = 0.1

# handle order_products__train.csv
# result_path = 'product_result.txt'
# data = pd.read_csv('order_products__train.csv')
# data_merged = data.groupby('order_id')['product_id'].apply(list).to_frame()
# data_merged['product_id'].to_csv(csv_path)
# dataset = csv.reader(open(csv_path, "r"))
# minSup = 0.002
# minConf = 0.1

# handle the test data: product.xls
# result_path = 'test_result.txt'
# data = pd.read_excel('product.xls')
# # data_merged = data.groupby('CUSTOMER')['PRODUCT'].apply(list).to_frame()
# data_merged = data.groupby('CUSTOMER').agg({'TIME':'sum','PRODUCT':lambda x: ','.join(x)})
# data_merged.PRODUCT = data_merged.PRODUCT.str.replace("\"","")
# # data_merged.PRODUCT = data_merged.PRODUCT.apply(literal_eval)
# data_merged['PRODUCT'].to_csv(csv_path)
# dataset = csv.reader(open(csv_path, "r"))
# minSup = 0.1
# minConf = 0.9

a = Apriori(dataset, minSup, minConf)

# Mining the frequent item sets
df_fis = pd.DataFrame.from_dict({"sets":"","support":""}, orient = 'index')


count_i = 0
frequentItemsets = a.gen_associations()
print("Frequent Itemsets:")
if os.path.exists(result_path):
    os.remove(result_path)
fp = open(result_path,'a')
fp.writelines("Number of transactions:"+str(len(a.transList))+"\n")
fp.writelines("Min Support:"+str(minSup)+" Min Confidence:"+str(minConf)+"\n")
fp.writelines("Frequent Itemsets:\n")
for k, item in frequentItemsets.items():
    for i in item:
        # if k >= 2:
        count_i += 1
        print(count_i, ":  ", i, "\tsupport=", round(a.support(a.freqList[i]),4))
        fp.writelines(str(count_i)+":  "+str(i)+"\tsupport="+str(round(a.support(a.freqList[i]),4))+"\n")
        df_fis = df_fis.append({"rules":i,"support":round(a.support(a.freqList[i]),4)}, ignore_index=True)

fp.writelines("There are "+str(count_i)+" frequent itemsets\n")
df_fis.plot(kind = 'bar')
plt.savefig("fis.png")
plt.clf()

# Mining the confident association rules
df_car = pd.DataFrame.from_dict({"rules":"","confidence":""}, orient = 'index')
count_r = 0
rules = a.gen_rules(frequentItemsets)
print("Confident Rules:")
fp.writelines("Confident Rules:\n")
for i, rule in enumerate(rules):
    count_r += 1
    fp.writelines("Rule"+str(i + 1)+":\t "+str(rule[0])+"\t-->"+str(rule[1])+"\t [sup="+str(round(rule[2],4))+" conf="+str(round(rule[3],4))+" lift="+str(round(rule[4],4)) if not isinstance(rule[4],str) else rule[4]+"]\n")
    print("Rule", i + 1, ":\t ", rule[0], "\t-->", rule[1], "\t [sup=", round(rule[2],4), " conf=", round(rule[3],4)," lift=",round(rule[4],4) if not isinstance(rule[4],str) else rule[4], "]\n")
    df_car = df_car.append({"rules":str(rule[0])+"-->"+str(rule[1]),"confidence":round(rule[3],4)}, ignore_index=True)
fp.writelines("There are "+str(count_r)+" confident rules\n")
fp.close()
print("There are", count_r, "confident rules\n")
df_car["confidence"].plot(kind = 'bar')
plt.savefig("car.png")
plt.clf()
