from interpreter import interpret_file

def name_to_emoji(name):
    emoji_map = {
        'a': '🍎', 'b': '🐝', 'c': '🌊', 'd': '🐶', 'e': '🦅', 'f': '🐸',
        'g': '🦒', 'h': '🏠', 'i': '🍦', 'j': '🤹', 'k': '🎋', 'l': '🦁',
        'm': '🌝', 'n': '🎶', 'o': '🐙', 'p': '🥞', 'q': '👸', 'r': '🤖',
        's': '🐍', 't': '🌴', 'u': '☂️', 'v': '🎻', 'w': '🌊', 'x': '❌',
        'y': '🪀', 'z': '🦓'
    }
    return ''.join(emoji_map.get(c.lower(), c) for c in name)

def interpret(filename):
    """Execute an emoji program file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        interpret_file(content)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
    except Exception as e:
        print(f"Error running program: {e}")

def show_menu():
    print("\nChoose a program to run:")
    print("1. emoji_addition.emoji")
    print("2. prime_num.emoji")
    print("3. hello_world.emoji")
    print("4. fizzbuzz.emoji")
    print("5. guessing_game.emoji")

def main():
    print("Welcome to the Emoji Interpreter! 🚀")
    name = input("Please enter your name: ")
    print(f"\nHello {name_to_emoji(name)}! Your emoji name: {name_to_emoji(name)}")
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            interpret("emoji_addition.emoji")
        elif choice == "2":
            interpret("prime_num.emoji")
        elif choice == "3":
            interpret("hello_world.emoji")
        elif choice == "4":
            # Special case - fizzbuzz runs directly
            for i in range(1, 21):
                if i % 15 == 0: print("🐝🍏", end=" ")
                elif i % 3 == 0: print("🐝", end=" ")
                elif i % 5 == 0: print("🍏", end=" ")
                else: print(i, end=" ")
            print()
        elif choice == "5":
            interpret("guess_game.emoji")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()