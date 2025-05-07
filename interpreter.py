import random

variables = {}
loop_stack = []
conditional_stack = []

def execute_emoji(line):
    """Handle special emoji commands"""
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

def interpret_line(line, line_num):
    """Interpret a single line of emoji code"""
    global variables, loop_stack, conditional_stack
    
    try:
        line = line.strip()
        if not line:
            return None

        # Handle control flow first
        if line == "🔄":
            loop_stack.append({"start": line_num, "active": True})
            return
        elif line == "🛑":
            if loop_stack:
                loop = loop_stack[-1]
                if loop["active"]:
                    return {"jump": loop["start"]}
                loop_stack.pop()
            return
        elif line == "⏹":
            if loop_stack:
                loop_stack[-1]["active"] = False
            return {"break": True}
        
        # Handle conditionals
        if line.startswith("🚀"):
            parts = line[2:].split("📌")
            condition = parts[0].strip()
            left, op, right = parse_condition(condition)
            result = evaluate_condition(left, op, right)
            conditional_stack.append(result)
            if not result:
                return {"skip_until": "🚁"}
            return
        elif line == "🚁":
            if conditional_stack:
                conditional_stack.pop()
            return

        # Skip execution if we're in a false conditional block
        if conditional_stack and not conditional_stack[-1]:
            return

        # Print statements
        if line.startswith("🗣️"):
            output = line[2:].strip().strip('"')
            for var in sorted(variables.keys(), key=len, reverse=True):
                output = output.replace(f"🔢{var}", str(variables[var]))
            print(output)
            return

        # Variable assignments
        if "👉" in line:
            parts = line.split("👉", 1)
            var_name = parts[0].replace("🔢", "").strip()
            value_expr = parts[1].strip()

            # Handle special emoji commands
            if "🎲" in value_expr or "📥" in value_expr:
                variables[var_name] = execute_emoji(value_expr)
                print(f"Assigned {var_name} = {variables[var_name]}")
                return

            # Handle regular expressions
            expr = value_expr
            for var in sorted(variables.keys(), key=len, reverse=True):
                expr = expr.replace(f"🔢{var}", str(variables[var]))
            
            expr = (expr.replace("➕", "+")
                     .replace("➖", "-")
                     .replace("✖️", "*")
                     .replace("➗", "/")
                     .replace("🧮", "%")
                     .replace("🔢", ""))
            
            if expr.strip():
                try:
                    variables[var_name] = eval(expr, {"__builtins__": None}, {})
                    print(f"Assigned {var_name} = {variables[var_name]}")
                except Exception as e:
                    print(f"Line {line_num}: Error in expression: {e}")
            return

        print(f"Line {line_num}: Unknown command: {line}")

    except Exception as e:
        print(f"Line {line_num}: Unexpected error: {e}")

def parse_condition(condition):
    """Parse comparison condition like 'a ➡ b'"""
    if "➡" in condition:
        left, right = condition.split("➡")
        return left.strip(), ">", right.strip()
    elif "⬅" in condition:
        left, right = condition.split("⬅")
        return left.strip(), "<", right.strip()
    return None, None, None

def evaluate_condition(left, op, right):
    """Evaluate comparison condition"""
    left_val = variables.get(left.replace("🔢", ""), 0)
    right_val = variables.get(right.replace("🔢", ""), 0)
    
    if op == ">":
        return left_val > right_val
    elif op == "<":
        return left_val < right_val
    return False

def interpret_file(content):
    """Interpret a complete emoji program"""
    global variables, loop_stack, conditional_stack
    variables = {}
    loop_stack = []
    conditional_stack = []
    
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    i = 0
    
    while i < len(lines):
        line = lines[i]
        result = interpret_line(line, i+1)
        
        if isinstance(result, dict):
            if "jump" in result:
                i = result["jump"] - 1
            elif "break" in result:
                break
            elif "skip_until" in result:
                while i < len(lines) and not lines[i].startswith(result["skip_until"]):
                    i += 1
        
        i += 1