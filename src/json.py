import json

d = {'liver': {}, 'tumour':{}}
d['liver'].update({1:{1:[2,3,4,5]}})
d['liver'].update({1:{2:[4,5,6,7]}})
d['liver'].update({1:{}})

d['tumour'].update({1:[1,1,1,1]})
d['tumour'].update({2:[1,1,1,1]})
print(d)
with open("record.json","w") as f:
     json.dump(d,f)
     print("加载入文件完成...")