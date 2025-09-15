# 1. User sends prompt
# 2. LLM turns prompt into json containing a message for the user and an action.
# 3. LLM decides whether it wants to ask the user anything or just get on with running next action, if it asks the user we go back to step one, if it doesnt we go back to step two

def ascii():
    left = [
        " .oooooo..o                    o8o      .   oooo                     ",
        "d8P'    `Y8                    `\"'    .o8   `888                     ",
        "Y88bo.      ooo. .oo.  .oo.   oooo  .o888oo  888 .oo.   oooo    ooo ",
        " `\"Y8888o.  `888P\"Y88bP\"Y88b  `888    888    888P\"Y88b   `88.  .8'  ",
        "     `\"Y88b  888   888   888   888    888    888   888    `88..8'   ",
        "oo     .d8P  888   888   888   888    888 .  888   888     `888'    ",
        "8\"\"88888P'  o888o o888o o888o o888o   \"888\" o888o o888o     .8'     ",
        "                                                        .o..P'        ",
        "                                                        `Y8P'         ",
        "                                                                          "
    ]

    # right letters separated line by line
    P = [
        "           ",
        "::::::::::. ",
        " `;;;```.;;;",
        "  `]]nnn]]' ",
        "   $$$\"\"    ",
        "   888o     ",
        "   YMMMb    "
    ]

    D = [
        "           ",
        ":::::::-.  ",
        " ;;,   `';,",
        " `[[     [[",
        "  $$,    $$",
        "  888_,o8P'",
        "  MMMMP\"`  "
    ]

    A = [
        "           ",
        "  :::.     ",
        "  ;;`;;    ",
        " ,[ [ '[,  ",
        "c$$$cc$$$c ",
        " 888   888,",
        " YMM   \"\"` "
    ]

    right = [P, D, A]

    # ANSI codes for right letters
    red = "\033[91m"
    green = "\033[92m"
    blue = "\033[94m"
    reset = "\033[0m"

    # pad left and right to same number of lines
    max_lines = max(len(left), max(len(r) for r in right))
    for i in range(max_lines):
        l_line = left[i] if i < len(left) else " " * len(left[0])
        r_line = ""
        for j, letter in enumerate(right):
            if i < len(letter):
                if j == 0:
                    r_line += red + letter[i] + reset
                elif j == 1:
                    r_line += green + letter[i] + reset
                else:
                    r_line += blue + letter[i] + reset
            else:
                r_line += " " * len(letter[0])
        print(l_line + " " + r_line)

ascii()

from flask import Flask, request, render_template, jsonify
# import json

app = Flask(__name__)

def smithy(user_input):
    return {
        "message": user_input,
        "command" : {
            "Command": "oneself",
            "Action": "poo",
            "When": "now",
            "Array": "[one, two]",
      }
    }

@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    user_input = data.get('user_input', '').strip()
    output = smithy(user_input)
    return jsonify(output)

@app.route('/confirm', methods=['POST'])
def confirm():
    return {
        "message": "Confirmed Action"
    }

@app.route('/deny', methods=['POST'])
def deny():
    return {
        "message": "Cancelled Action on Users Request"
    }

app.run(port=1234)
