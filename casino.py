# ...existing code...
import random
import time
import sys

WHEEL = [
    ("Lose", 0.40, 0.0),      # 40% -> lose bet
    ("Double", 0.30, 2.0),    # 30% -> 2x
    ("Triple", 0.15, 3.0),    # 15% -> 3x
    ("FiveX", 0.10, 5.0),     # 10% -> 5x
    ("Jackpot", 0.05, 10.0),  # 5%  -> 10x
]

SPIN_CHARS = ["|", "/", "-", "\\"]

def choose_sector():
    labels = [s[0] for s in WHEEL]
    weights = [s[1] for s in WHEEL]
    return random.choices(list(range(len(WHEEL))), weights=weights, k=1)[0]

def animate_spin(final_index, rounds=20, delay=0.04):
    length = len(WHEEL)
    pos = random.randrange(length)
    for i in range(rounds):
        pos = (pos + 1) % length
        label = WHEEL[pos][0]
        sys.stdout.write(f"\rSpinning... {SPIN_CHARS[i % len(SPIN_CHARS)]}  [{label}] ")
        sys.stdout.flush()
        time.sleep(delay)
    # slow to final
    while pos != final_index:
        pos = (pos + 1) % length
        label = WHEEL[pos][0]
        sys.stdout.write(f"\rSpinning... {SPIN_CHARS[pos % len(SPIN_CHARS)]}  [{label}] ")
        sys.stdout.flush()
        time.sleep(delay * 1.8)
    print()

def play_round(balance):
    print(f"\nBalance: ${balance:.2f}")
    while True:
        try:
            bet = float(input("Place your bet (or 0 to cancel): ").strip())
            if bet < 0:
                print("Bet must be non-negative.")
                continue
            if bet == 0:
                return balance
            if bet > balance:
                print("Insufficient balance.")
                continue
            break
        except ValueError:
            print("Enter a numeric bet amount.")
    print("Spinning the wheel...")
    idx = choose_sector()
    animate_spin(idx)
    label, _, mult = WHEEL[idx]
    if mult <= 0:
        winnings = 0.0
        balance -= bet
        print(f"Result: {label} — you lost ${bet:.2f}.")
    else:
        winnings = bet * mult
        balance += (winnings - bet)  # net gain: winnings minus original bet
        print(f"Result: {label} — you win ${winnings:.2f} (multiplier {mult}x).")
    print(f"New balance: ${balance:.2f}")
    return balance

def print_help():
    print("\nCommands:")
    print("  spin   - place a bet and spin")
    print("  bal    - show balance")
    print("  help   - show commands")
    print("  quit   - exit game\n")

def main():
    print("Welcome to Lucky Spin Casino (demo).")
    balance = 100.0
    print("Starting balance: $100.00")
    print_help()
    while True:
        cmd = input("> ").strip().lower()
        if cmd in ("quit", "q", "exit"):
            print(f"Leaving casino. Final balance: ${balance:.2f}")
            break
        if cmd in ("help", "h"):
            print_help()
            continue
        if cmd in ("bal", "balance"):
            print(f"Balance: ${balance:.2f}")
            continue
        if cmd in ("spin", "s"):
            balance = play_round(balance)
            if balance <= 0:
                print("You've run out of money. Game over.")
                break
            continue
        print("Unknown command. Type 'help' for options.")

if __name__ == "__main__":
    main()
# ...existing code...