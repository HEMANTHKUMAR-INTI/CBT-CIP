import random
import time

def show_banner():
    print("\n" + "#" * 60)
    print("WELCOME TO THE ULTIMATE R-P-S SHOWDOWN!".center(60))
    print("#" * 60)
    print("RULEBOOK:")
    print("🪨 Rock beats ✂ Scissors")
    print("📄 Paper beats 🪨 Rock")
    print("✂ Scissors beats 📄 Paper")
    print("#" * 60)

def prompt_choice():
    options = {1: 'rock', 2: 'paper', 3: 'scissors'}
    while True:
        try:
            choice = int(input("Pick your move → 1:Rock | 2:Paper | 3:Scissors: "))
            if choice in options:
                return options[choice]
            else:
                print("⚠ Please enter a valid number (1, 2, or 3).")
        except:
            print("⚠ Numbers only! Try again.")

def computer_strategy(human_move):
    counter_moves = {
        'rock': ['paper', 'scissors'],
        'paper': ['scissors', 'rock'],
        'scissors': ['rock', 'paper']
    }
    if random.random() < 0.3:
        return human_move
    return random.choice(counter_moves[human_move])

def evaluate_result(player, bot):
    win_cases = {
        ('rock', 'scissors'),
        ('paper', 'rock'),
        ('scissors', 'paper')
    }
    if player == bot:
        return 'tie'
    elif (player, bot) in win_cases:
        return 'you'
    else:
        return 'bot'

def run_match():
    user_move = prompt_choice()
    comp_move = computer_strategy(user_move)

    print(f"\n🧍 You played: {user_move.title()}")
    time.sleep(0.6)
    print(f"🤖 Bot played: {comp_move.title()}")
    time.sleep(0.6)

    verdict = evaluate_result(user_move, comp_move)
    if verdict == 'tie':
        print("🔁 It's a tie round!")
    elif verdict == 'you':
        print("🎉 You win this round!")
    else:
        print("😈 Bot takes this round!")
    return verdict

def replay_prompt():
    while True:
        answer = input("Wanna go again? (yes/no): ").lower().strip()
        if answer in ('yes', 'no'):
            return answer == 'yes'
        print("⚠ Only 'yes' or 'no' accepted.")

def begin_game():
    show_banner()
    round_counter = 1
    score_board = {'you': 0, 'bot': 0}

    while True:
        print(f"\n📦 Round {round_counter}")
        outcome = run_match()

        if outcome in score_board:
            score_board[outcome] += 1

        print(f"📊 Score Tracker → You: {score_board['you']} | Bot: {score_board['bot']}")
        round_counter += 1

        if not replay_prompt():
            break

    print("\n" + "=" * 60)
    print("🏁 FINAL GAME REPORT".center(60))
    print("=" * 60)
    print(f"🧍 You: {score_board['you']} | 🤖 Bot: {score_board['bot']}")
    if score_board['you'] > score_board['bot']:
        print("🏆 Victory is yours!")
    elif score_board['you'] < score_board['bot']:
        print("💔 The computer  wins this time.")
    else:
        print("🤝 It's a dead heat!")

if __name__ == "__main__":
    begin_game()