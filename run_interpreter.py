#run_interpreter.py
from interpreter import interpret_file

def main():
    try:
        with open("guess_game.emoji", "r", encoding="utf-8") as file:
            emoji_code = file.read()
            interpret_file(emoji_code)
    except FileNotFoundError:
        print("Error: 'guess_game.emoji' not found in current directory!")
    except Exception as e:
        print(f"Error running program: {e}")

if __name__ == "__main__":
    main()