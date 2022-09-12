height = float(input("请输入您的身高(m): "))
weight = float(input("请输入您的体重(kg):"))
bmi = weight / height ** 2
if bmi <= 18.4:
    print(f"你的 BMI 值: {bmi:.1f}，身体状态：偏瘦")
elif bmi <= 23.9:
    print(f"你的 BMI 值: {bmi:.1f}，身体状态：正常")
elif bmi <= 27.9:
    print(f"你的 BMI 值: {bmi:.1f}，身体状态：过重")
else:
    print(f"你的 BMI 值: {bmi:.1f}，身体状态：肥胖")
