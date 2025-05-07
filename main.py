from emoji_interpreter import name_to_emoji, interpret

def main():
    print("Welcome to the Emoji Interpreter! 🚀")
    name = input("Please type your name: ")
    emoji_name = name_to_emoji(name)
    print(f"\nHere is your name in emoji language: {emoji_name}")

    print("\nNow, let's choose what you'd like to do next:")
    print("1. Run emoji_addition.emoji")
    print("2. Run prime_num.emoji")
    print("3. Run hello_world.emoji")
    print("4. Run fizzbuzz.emoji")

    choice = input("Enter the number of your choice: ")

    program_map = {
        "1": "emoji_addition.emoji",
        "2": "prime_num.emoji",
        "3": "hello_world.emoji",
        "4": "fizzbuzz.emoji"
    }

    if choice in program_map:
        interpret(program_map[choice])
        print()  # Ensure newline after execution
    else:
        print("Invalid choice. Please select a valid number (1-4).")

if __name__ == "__main__":
    main()
