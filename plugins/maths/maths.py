import sys
import json

def main():
    if len(sys.argv) < 2:
        print("No input provided")
        return

    try:
        action = json.loads(sys.argv[1])
    except Exception as e:
        print(f"Invalid JSON: {e}")
        return

    op = action.get("operation")
    a = action.get("a")
    b = action.get("b")

    try:
        if op == "addition":
            result = a + b
        elif op == "subtraction":
            result = a - b
        elif op == "multiplication":
            result = a * b
        elif op == "division":
            if b == 0:
                result = "Error: division by zero"
            else:
                result = a / b
        else:
            result = f"Unknown operation: {op}"
    except Exception as e:
        result = f"Error: {e}"

    print(result)

main()
