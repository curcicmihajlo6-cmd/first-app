import random
import time
import os

WORDS = ["python", "hangman", "dinosaur", "programming", "computer", "keyboard", "monitor", "algorithm"]

HANGMAN_STAGES = [
    """
       ------
       |    |
       |
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   \\|
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   \\|/
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   \\|/
       |    |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   \\|/
       |    |
       |   / \\
    --------
    """
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_text(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def main():
    clear_screen()
    animate_text("=" * 50)
    animate_text("🎮 WELCOME TO HANGMAN! 🎮", delay=0.02)
    animate_text("=" * 50)
    time.sleep(1)
    
    word = random.choice(WORDS).upper()
    guessed = set()
    wrong = set()
    max_wrong = len(HANGMAN_STAGES) - 1
    
    while True:
        clear_screen()
        print(HANGMAN_STAGES[len(wrong)])
        
        display = "".join([letter if letter in guessed else "_" for letter in word])
        print(f"\nWord: {' '.join(display)}")
        print(f"Wrong guesses: {', '.join(sorted(wrong)) if wrong else 'None'}")
        print(f"Remaining: {max_wrong - len(wrong)}")
        
        if "_" not in display:
            animate_text(f"\n🎉 YOU WIN! The word was: {word}", delay=0.05)
            break
        
        if len(wrong) >= max_wrong:
            print(HANGMAN_STAGES[len(wrong)])
            animate_text(f"\n💀 GAME OVER! The word was: {word}", delay=0.05)
            break
        
        guess = input("\nGuess a letter: ").upper().strip()
        
        if len(guess) != 1 or not guess.isalpha():
            print("❌ Please enter a single letter!")
            time.sleep(1)
            continue
        
        if guess in guessed or guess in wrong:
            print("❌ You already guessed that!")
            time.sleep(1)
            continue
        
        if guess in word:
            guessed.add(guess)
            animate_text(f"✓ Good guess! '{guess}' is in the word!", delay=0.03)
        else:
            wrong.add(guess)
            animate_text(f"✗ Wrong guess! '{guess}' is not in the word!", delay=0.03)
        
        time.sleep(1)

if __name__ == "__main__":
    main()