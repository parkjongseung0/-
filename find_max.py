def user():
    data = []
    for i in range(10):
        user_data=input(f"{i+1}번째의 데이터를 입력하시오.")
        data.append(int(user_data))
    return data

def find_max_recursive(data,a):
    if a==1:
        return data[0]
    else: 
        maxdata= find_max_recursive(data[1:],a-1)
        return max(data[0],maxdata)

def find_max_iterative(data):
    if not data:
        return None
    else:
        maxdata = data[0]
        for a in data[1:]:
            if a > maxdata:
                maxdata=a
        return maxdata

data = user()

max_recursive=find_max_recursive(data,len(data))
print(f"재귀 버전 최대값={max_recursive}")
max_iterative=find_max_iterative(data)
print(f"반복 버전 최대값{max_iterative}")