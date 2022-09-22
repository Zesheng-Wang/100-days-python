# rock-paper-scissors
import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

game_images = [rock, paper, scissors]

user_choice = int(
    input("请输入你的选择? 输入0表示石头, 输入1示布 或 输入2表示剪刀.\n"))
print(game_images[user_choice])

computer_choice = random.randint(0, 2)
print("AI的选择:")
print(game_images[computer_choice])

if user_choice >= 3 or user_choice < 0:
    print("您输入的数字不合法，你输了!")
elif user_choice == 0 and computer_choice == 2:
    print("You win!")
elif computer_choice == 0 and user_choice == 2:
    print("You lose")
elif computer_choice > user_choice:
    print("You lose")
elif user_choice > computer_choice:
    print("You win!")
elif computer_choice == user_choice:
    print("平局")
