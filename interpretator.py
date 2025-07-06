import random
import time
import re

variables = {}
manager_mood = "neutral"
block_stack = []

def random_approval():
    yield ("\n✅ Approved" if random.choice([True, False]) else "❌ Not Approved")

def random_excuse():
    excuses = [
        "Wifi issue ho gaya tha",
        "Client call chal rha tha",
        "Server down tha",
        "Out of office tha",
        "System hang ho gaya"
    ]
    yield ("\n" +random.choice(excuses))

def should_execute():
    # Execution is allowed only if no false-executing block exists on the stack
    isExecuted = all(b["executing"] for b in block_stack)
    return block_stack[-1]["matched"] and block_stack[-1]["executing"] if block_stack and len(block_stack) > 0 else isExecuted

def run_program(lines):
    try:
        global manager_mood
    # with open(file_path) as f:
        #    lines = [line.strip() for line in f.readlines() if line.strip()]
        if not lines or len(lines) < 1:
            raise Exception("☠️ kya kar rha he bhai tu Program mein kuch nahi hai")
        if lines[0] != "day start":
            raise Exception("☠️ Program bina 'day start' ke chalu kar diya")
        if lines[-1] != "day end":
            raise Exception("☠️ Bina 'day end' ke program khatam kar diya")

        i = 0
        while i < len(lines):
            code = lines[i]
            line = code.strip()
            if line == "day start" :
                i += 1
                yield ("\n🌅 Day started. Ho gaya siyapa start")
                continue
            if line == "day end":
                i += 1
                yield ("\n🌇 Day ended. Ho gaya siyapa khatam")
                continue

            if line.startswith("reportKaro") and should_execute():
                expr = line[10:].strip()
                if expr.startswith('"') and expr.endswith('"'):
                    # It's a string literal
                    yield "\n" + expr[1:-1]
                else:
                    # It's a variable or expression, so replace variables and evaluate
                    print("Processing expression:", variables)
                    tokens = re.findall(r'\b[a-zA-Z_]\w*\b', expr)
                    print("Tokens found:", tokens)
                    for token in tokens:
                        if token not in variables:
                            raise Exception(f"☠️ Variable '{token}' defined nahi hai!")
                        expr = re.sub(rf'\b{token}\b', str(variables[token]), expr)
                    try:
                        print("Evaluating expression:", expr)
                        result = eval(expr)
                        yield "\n" + str(result)
                    except Exception as e:
                        yield f"\n⚠️ Error: {e}"

            elif line.startswith("assignTask"):
                parts = line.split()
                if len(parts) != 4 or parts[2] != "=":
                    raise Exception("☠️ 'assignTask' ka syntax galat hai!")
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
                print("Evaluating condition:", condition)
                result = eval(condition)
                print("Condition result:", result)
                block_stack.append({"type": "if", "executing": True, "matched": result})

            elif line == "nahi":
                if block_stack and block_stack[-1]["type"] == "if":
                    current = block_stack.pop() 
                    block_stack.append({"type": "else", "executing": current["executing"], "matched":not current["matched"]})
                else:
                    raise Exception("☠️ 'nahi' bina 'agar' ke laga diya!")

            elif line == "kaam band":
                block_stack.pop()

            elif line == "manager ka mood":
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
                    yield ("\n🔥 issue aa gaya! Exception throw hua.")
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
                    #run_program_from_lines(loop_lines)
                    iloop = 0
                    while iloop < len(loop_lines):
                        loop_line = loop_lines[iloop]
                        if loop_line.startswith("reportKaro") and should_execute():
                            start = loop_line.find('"') + 1
                            end = loop_line.rfind('"')
                            yield ("\n" +loop_line[start:end])
                        iloop += 1
                #i += 1

            elif line.startswith("tea break"):
                parts = line.split()
                sec = int(parts[2])
                yield ("\n" +f"☕ Tea break ...")
                while sec > 0:
                    yield ("\nabhi bhi tea break chal rha he manager ...")
                    time.sleep(10)
                    sec -= 10

                yield ("\n⏰ Tea break over.")

            elif line == "approval dedo" and should_execute():
                random_approval()

            elif line == "manager ne excuse diya" and should_execute():
                random_excuse()

            i += 1
        yield ("\n\n🌟 Program execution complete. Tera promotion pakka")
    except Exception as e:
        yield ("<b>"+str(e)+ "\nManager dekhe usse pehle fix kr!</b>")

def run_program_from_lines(lines):
    global manager_mood
    local_variables = variables.copy()
    local_stack = block_stack.copy()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("reportKaro") and should_execute():
            start = line.find('"') + 1
            end = line.rfind('"')
            yield ("\n" +line[start:end])
        i += 1

# ✅ Run program:
#run_program("program.clang")