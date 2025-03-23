import random

# =====================
# 全局配置
# =====================
INITIAL_CHIPS = 1000  # 初始筹码
# 全局常量
SUITS = ["♥", "♦", "♠", "♣"]  # 花色
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]  # 点数
CARD_VALUES = {
    "A": 11,  # 初始按11计算，后续动态调整
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
}


# =====================
# 核心函数
# =====================
def create_deck(num_decks=6):
    """创建多副牌并洗牌"""
    deck = [[suit, rank] for suit in SUITS for rank in RANKS] * num_decks
    random.shuffle(deck)
    return deck


def calculate_score(hand):
    """计算手牌最优点数（自动处理A的1/11值）"""
    score = sum(CARD_VALUES[card[1]] for card in hand)
    aces = sum(1 for card in hand if card[1] == "A")

    # 动态调整A的值
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score


def show_cards(hand, hide_first=False):
    """可视化显示手牌（hide_first用于隐藏庄家首牌）"""
    display = []
    for i, card in enumerate(hand):
        if hide_first and i == 0:
            display.append("[隐藏牌]")
        else:
            display.append(f"{card[0]}{card[1]}")
    return "  ".join(display)


# =====================
# 游戏流程控制
# =====================
def player_turn(deck, player_hand):
    """玩家操作回合"""
    while True:
        current_score = calculate_score(player_hand)
        print(f"\n你的手牌：{show_cards(player_hand)}")
        print(f"当前点数：{current_score}")

        if current_score >= 21:
            break

        choice = input("要牌(h)还是停牌(s)？").lower()
        if choice == "h":
            player_hand.append(deck.pop())
        elif choice == "s":
            break
        else:
            print("无效输入，请输入h或s！")

    return player_hand


def dealer_turn(deck, dealer_hand):
    """庄家自动操作"""
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
    return dealer_hand


def check_winner(player_score, dealer_score):
    """胜负判定"""
    if player_score > 21:
        return "庄家胜！玩家爆牌"
    elif dealer_score > 21:
        return "玩家胜！庄家爆牌"
    elif player_score > dealer_score:
        return "玩家胜！"
    elif dealer_score > player_score:
        return "庄家胜！"
    else:
        return "平局！"


# =====================
# 主游戏逻辑
# =====================
def blackjack_game():
    chips = INITIAL_CHIPS

    while chips > 0:
        print(f"\n=== 当前筹码：{chips} ===")
        bet = int(input("请下注（输入金额）："))

        if bet > chips:
            print("筹码不足！")
            continue

        # 初始化牌局
        deck = create_deck()
        player = [deck.pop(), deck.pop()]
        dealer = [deck.pop(), deck.pop()]

        # 玩家回合
        player = player_turn(deck, player)
        player_score = calculate_score(player)

        # 庄家回合
        if player_score <= 21:
            dealer = dealer_turn(deck, dealer)
        dealer_score = calculate_score(dealer)

        # 显示结果
        print("\n=== 最终结果 ===")
        print(f"庄家手牌：{show_cards(dealer)} → 点数：{dealer_score}")
        print(f"你的手牌：{show_cards(player)} → 点数：{player_score}")

        # 结算
        result = check_winner(player_score, dealer_score)
        print(f"\n结果：{result}")

        if "玩家胜" in result:
            chips += bet
        elif "庄家胜" in result:
            chips -= bet

        # 继续游戏判断
        if input("\n继续游戏？(y/n)").lower() != "y":
            break

    print(f"\n游戏结束，最终筹码：{chips}")


# =====================
# 启动游戏
# =====================
if __name__ == "__main__":
    print("=== 欢迎来到二十一点赌场 ===")
    blackjack_game()
