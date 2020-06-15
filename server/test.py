#tt=(('E1', '機械系'), ('E3', '化工系'), ('E4', '資源系'), ('E5', '材料系'), ('E6', '土木系'), ('E8', '水利系'), ('E9', '工科系'), ('F1', '系統系'), ('F4', '航太系'), ('F5', '環工系'), ('F6', '測量系'), ('F9', '醫工系'))

#tt={'E1': '機械系', 'E3': '化工系', 'E4': '資源系', 'E5': '材料系', 'E6': '土木系', 'E8': '水利系', 'E9': '工科系', 'F1': '系統系', 'F4': '航太系', 'F5': '環工系', 'F6': '測量系', 'F9': '醫工系'}
'''
for i in tt:
    print(i+":"+tt[i])
'''
'''
filename = 'mysqlpasswd.txt'
f = open(filename,'r')
ans=[]
for line in f:
    line=line.strip('\n')
    ans.append(line)
print(ans)
print(ans[0])
'''
t = ((0, 2, 'E94056233', 'Arduino UNO', 'Be careful', 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Arduino_Uno_-_R3.jpg/220px-Arduino_Uno_-_R3.jpg', 'ael2m', 30), (1, 2, 'E94056233', 'L298N', 'Be Careful', 'https://www.botsheet.com/cht/wp-content/uploads/l298n-motor-driver-module-01.jpeg', 'Ddl3i', 30))

item_list={}
for i in t:
    if i[0] == 1:
        item_list[i[3]] = [i[1],i[7],i[4],i[5]]
print(item_list)

for i in item_list.keys():
    print(item_list[i][0])


