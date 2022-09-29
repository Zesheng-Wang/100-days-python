num_list = list(map(int, input().split(' ')))
sum = 0
print(num_list)
for number in num_list:
    sum += number

avg = sum / len(num_list)
print(f"该序列的平均数是{avg}")
