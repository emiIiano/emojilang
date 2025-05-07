import random
import re

variables = {}
loop_stack = []
conditional_stack = []
current_if_group = []

def name_to_emoji(name):
    return ''.join(f":{char}:" if char.isalpha() else char for char in name.lower())

def execute_emoji(line):
    try:
        if "🎲" in line:
            start = line.find("(") + 1
            end = line.find(")")
            range_parts = line[start:end].split("➖")
            return random.randint(int(range_parts[0]), int(range_parts[1]))
        elif "📥" in line:
            return int(input("Enter your guess: "))
    except Exception as e:
        print(f"Error executing emoji command: {e}")
        return None

def evaluate_expr(expr):
    expr = expr.replace("🔢", "")
    for var in variables:
        expr = expr.replace(var, str(variables[var]))
    expr = (expr.replace("➕", "+")
                 .replace("➖", "-")
                 .replace("✖️", "*")
                 .replace("➗", "/")
                 .replace("🧮", "%")
                 .replace("✅", "True")
                 .replace("🚫", "False"))
    return expr

def evaluate_condition_expr(expr):
    try:
        return eval(evaluate_expr(expr), {"__builtins__": None}, {})
    except:
        return False

def parse_literal(value_expr):
    if value_expr == "✅": return True
    if value_expr == "🚫": return False
    return None

def interpret_line(line, line_num):
    global variables, loop_stack, conditional_stack, current_if_group

    try:
        line = line.strip()
        if not line:
            return None

        if line.startswith("🔁"):
            match = re.match(r"🔁 🔢(\w+) from (.+?) to (.+)", line)
            if match:
                var, start_expr, end_expr = match.groups()
                start = int(eval(evaluate_expr(start_expr), {"__builtins__": None}, {}))
                end = int(eval(evaluate_expr(end_expr), {"__builtins__": None}, {}))
                loop_stack.append({"var": var, "start_line": line_num, "end": end, "index": start, "broken": False})
                variables[var] = start
                return

        elif line == "🔄":
            if loop_stack:
                loop = loop_stack[-1]
                if loop.get("broken"):
                    loop_stack.pop()
                else:
                    loop_var = loop["var"]
                    variables[loop_var] += 1
                    if variables[loop_var] > loop["end"]:
                        loop_stack.pop()
                    else:
                        return {"jump": loop["start_line"]}
            return

        elif line == "🔚 loop":
            if loop_stack:
                loop_stack[-1]["broken"] = True
            return

        elif line == "🛑":
            if conditional_stack:
                conditional_stack.pop()
            current_if_group.clear()
            return

        if line.startswith("🤔") or line.startswith("🚫"):
            if "if" in line:
                condition = line.split("if", 1)[-1].strip()
                result = evaluate_condition_expr(condition)
                conditional_stack.append(result)
                current_if_group.append(result)
                if not result:
                    return {"skip_until": None}
                return
            elif line.strip() == "🚫 else":
                if not any(current_if_group):
                    return
                else:
                    return {"skip_until": "🛑"}

        if not line.startswith(("🤔", "🚫")):
            current_if_group.clear()

        if conditional_stack and not conditional_stack[-1]:
            return

        if line.startswith("🗣️"):
            output = line[2:].strip().strip('"')
            for var in variables:
                output = output.replace(f"🔢{var}", str(variables[var]))
            print(output)
            return

        if "👉" in line or "=" in line:
            line = line.replace("📦", "").strip()
            if "👉" in line:
                parts = line.split("👉", 1)
            else:
                parts = line.split("=", 1)

            var_name = parts[0].replace("🔢", "").strip()
            value_expr = parts[1].strip()

            literal = parse_literal(value_expr)
            if literal is not None:
                variables[var_name] = literal
                return

            if "🎲" in value_expr or "📥" in value_expr:
                variables[var_name] = execute_emoji(value_expr)
                return

            expr = evaluate_expr(value_expr)
            if expr.strip():
                variables[var_name] = eval(expr, {"__builtins__": None}, {})
            return

        print(f"Line {line_num}: Unknown command: {line}")

    except Exception as e:
        print(f"Line {line_num}: Unexpected error: {e}")

def interpret_file(content):
    global variables, loop_stack, conditional_stack, current_if_group
    variables = {}
    loop_stack = []
    conditional_stack = []
    current_if_group = []

    lines = [line.strip() for line in content.split('\n') if line.strip()]
    i = 0

    while i < len(lines):
        line = lines[i]
        result = interpret_line(line, i+1)

        if isinstance(result, dict):
            if "jump" in result:
                i = result["jump"] - 1
            elif "skip_until" in result and result["skip_until"]:
                while i < len(lines) and not lines[i].startswith(result["skip_until"]):
                    i += 1
        i += 1

def interpret(filename):
    with open(filename, 'r') as f:
        content = f.read()
    interpret_file(content)
