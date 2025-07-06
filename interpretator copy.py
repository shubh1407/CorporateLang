import random
import time
import re

variables = {}
manager_mood = "neutral"
block_stack = []

def random_approval():
    print("✅ Approved" if random.choice([True, False]) else "❌ Not Approved")

def random_excuse():
    excuses = [
        "Wifi issue ho gaya tha",
        "Client call chal rha tha",
        "Server down tha",
        "Out of office tha",
        "System hang ho gaya"
    ]
    print(random.choice(excuses))

def should_execute():
    # Execution is allowed only if no false-executing block exists on the stack
    isExecuted = all(b["executing"] for b in block_stack)
    return block_stack[-1]["matched"] and block_stack[-1]["executing"] if block_stack and len(block_stack) > 0 else isExecuted

def run_program(file_path):
    global manager_mood
    with open(file_path) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if lines[0] != "day start":
        raise Exception("☠️ Program bina 'day start' ke chalu kar diya — Manager ne terminate kar diya!")
    if lines[-1] != "day end":
        raise Exception("☠️ 'day end' nahi likha — Client ne scope creep laga diya!")

    i = 0
    while i < len(lines):
        line = lines[i]

        if line == "day start" :
            i += 1
            print("🌅 Day started. Ho gaya siyapa start")
            continue
        if line == "day end":
            i += 1
            print("🌇 Day ended. Ho gaya siyapa khatam")
            continue

        if line.startswith("gupshup") and should_execute():
            start = line.find('"') + 1
            end = line.rfind('"')
            print(line[start:end])

        elif line.startswith("circleBack"):
            parts = line.split()
            if len(parts) != 4 or parts[2] != "=":
                raise Exception("☠️ 'circleBack' ka syntax galat hai!")
            variables[parts[1]] = int(parts[3])

        elif line.startswith("manager ka mood kya he"):
            start = line.find('"') + 1
            end = line.rfind('"')
            manager_mood = line[start:end]

        elif line == "manager ka mood random karo":
            manager_mood = random.choice(["busy", "happy", "angry", "neutral"])

        elif line.startswith("agar"):
            start_idx = line.find("(")
            end_idx = line.rfind(")")
            condition = line[start_idx + 1:end_idx]
            tokens = re.findall(r'\b[a-zA-Z_]\w*\b', condition)
            for token in tokens:
                if token not in variables:
                    raise Exception(f"☠️ Variable '{token}' defined nahi hai!")
                if token in variables:
                    condition = re.sub(rf'\b{token}\b', str(variables[token]), condition)
            result = eval(condition)
            block_stack.append({"type": "if", "executing": True, "matched": result})

        elif line == "nahi":
            if block_stack and block_stack[-1]["type"] == "if":
                current = block_stack.pop()
                block_stack.append({"type": "else", "executing": not current["executing"], "matched": not current["matched"]})
            else:
                raise Exception("☠️ 'nahi' bina 'agar' ke laga diya!")

        elif line == "kaam band":
            block_stack.pop()

        elif line == "switch manager ka mood":
            block_stack.append({"type": "switch", "executing": True, "matched": False})

        elif line.startswith("jab"):
            if not block_stack or all(item["type"] != "switch" for item in block_stack):
                raise Exception("☠️ 'jab' bina 'switch' ke laga diya!")
            start = line.find('"') + 1
            end = line.rfind('"')
            mood_check = line[start:end]
            should_run = (manager_mood == mood_check) and not block_stack[-1]["matched"]
            if should_run:
                block_stack[-1]["matched"] = True
            block_stack.append({"type": "case", "executing": should_run,"matched": should_run})

        elif line == "choro":
            if not block_stack or all(item["type"] != "switch" for item in block_stack):
                raise Exception("☠️ 'warna' bina 'switch' ke laga diya!")
            should_run = not any(item["matched"] for item in block_stack if item["type"] == "case")
            block_stack.append({"type": "case", "executing": should_run,"matched": should_run})
            #block_stack[-1]["matched"] = should_run

        elif line == "mood ka the end":
            while block_stack and block_stack[-1]["type"] in ["case", "switch"]:
                block_stack.pop()

        elif line == "client call lagao":
            block_stack.append({"type": "try", "executing": True, "matched": True})

        elif line == "issue aa gaya":
            if block_stack and any(item["type"] == "try" for item in block_stack):
                print("🔥 issue aa gaya! Exception throw hua.")
                block_stack.pop()
                found = False
                for var in range(i + 1, len(lines)):
                    if lines[var] == "client gussa hua" or lines[var] == "chinta mat kar":
                        i = var
                        type = "catch" if lines[var] == "client gussa hua" else "finally"
                        block_stack.append({"type": type, "executing": True,"matched": True})
                        found = True
                        break 
                if not found:
                    raise Exception("☠️ 'client gussa hua' nahi mila — Exception handle nahi hua!")
                
        elif line == "client gussa hua":
            if block_stack and any(item["type"] == "try" for item in block_stack):
                block_stack.pop()
                block_stack.append({"type": "catch", "executing": True,"matched": True})
            else:
                raise Exception("☠️ 'client gussa hua' bina 'issue aa gaya' ke laga diya!")

        elif line == "chinta mat kar":
            if block_stack and any(item["type"] in ["try","catch"] for item in block_stack):
                block_stack.pop()
                block_stack.append({"type": "finally", "executing": True,"matched": True})

        elif line == "chinta over":
            while block_stack and any(item["type"] in ["try","catch","finally"] for item in block_stack):
                block_stack.pop()

        elif line.startswith("chalo meeting kre"):
            parts = line.split()
            count = int(parts[3])
            loop_lines = []
            i += 1
            while lines[i] != "finally over huyi":
                loop_lines.append(lines[i])
                i += 1
            for _ in range(count):
                run_program_from_lines(loop_lines)
            #i += 1

        elif line.startswith("tea break"):
            parts = line.split()
            sec = int(parts[2])
            print(f"☕ Tea break ...")
            while sec > 0:
                print("abhi bhi tea break chal rha he manager ...")
                time.sleep(10)
                sec -= 10

            print("⏰ Tea break over.")

        elif line == "approval dedo" and should_execute():
            random_approval()

        elif line == "manager ne excuse diya" and should_execute():
            random_excuse()

        i += 1

def run_program_from_lines(lines):
    global manager_mood
    local_variables = variables.copy()
    local_stack = block_stack.copy()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("gupshup") and should_execute():
            start = line.find('"') + 1
            end = line.rfind('"')
            print(line[start:end])
        i += 1

# ✅ Run program:
run_program("program.clang")