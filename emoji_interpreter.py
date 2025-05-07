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


def main():
    print("Welcome to the Emoji Interpreter! 🚀")
    name = input("Please enter your name: ")
    print(f"\nHello {name_to_emoji(name)}! Your emoji name: {name_to_emoji(name)}")
    

if __name__ == "__main__":
    main()
