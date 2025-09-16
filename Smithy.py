import os
from dotenv import load_dotenv
import openai
import subprocess
from pathlib import Path
import sys
import json
from datetime import datetime
import socket
import colorama


red = "\033[91m"
green = "\033[92m"
blue = "\033[94m"
magenta = "\033[95m"

reset = "\033[0m"


def ascii():
    print("\n")
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

version = "2.4"

try:
    socket.create_connection(("8.8.8.8", 53), timeout=5)
except OSError:
    print("Your offline, exiting program.")
    sys.exit()

time = datetime.today().strftime('%Y%m%d%H%M%S')

# set config path, plugin dir and load .env
home_dir = Path.home()
config_path = 'config'
print(f"Config path: {config_path}/main.env")
load_dotenv(f'{config_path}/main.env')
plugin_dir = os.getenv("PLUGINS")

# tell the user the plugin dir, unless it is none, then scare them
if(plugin_dir) == None:
    print(f"Key PLUGINS does not exist in {config_path}/main.env")
    sys.exit()
else:
    print(f"Loading plugins from {plugin_dir}")

NAME = os.getenv("NAME")
print(f"Got user name: {NAME}")
# set up conversation messages
conversation_messages = []

# load openAI client
print("Loading OpenAI client.")

OPENAI_KEY = os.getenv("OPENAI_KEY")
if not OPENAI_KEY:
    raise ValueError(f"Key OPENAI_KEY does not exist in {config_path}/main.env")
client = openai.OpenAI(api_key=OPENAI_KEY)
MODEL_NAME = os.getenv("MODEL")
if MODEL_NAME == None:
    MODEL_NAME = "gpt-4.1"


addons = []

def load_addons():
    global addons
    addons = []
    if plugin_dir == None:
        print("No plugin directory set")
        sys.exit()
    root_path = Path(plugin_dir)

    for subdir in root_path.iterdir():
        if subdir.is_dir():
            commands_file = subdir / "commands.md"

            if commands_file.exists():
                try:
                    with open(commands_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    addons.append(content)

                except Exception as e:
                    print(f"Error reading {commands_file}: {e}")

load_addons()
print("Loaded addons")
print(addons)

ascii()
print(f"Chatting with Smithy v{version}")
def llm(prompt):
    if not os.path.exists(f"{config_path}/sys_prompt.md"):
        with open(f"{config_path}/sys_prompt.md", "w") as f:
            pass
        print(f"created sys_prompt.md at {config_path}")

    with open(f"{config_path}/sys_prompt.md") as f:
        content = f.read()
        content = content.format(actions=addons, time=time, user=NAME)

    messages = {}

    messages["smithy"] = [
        {
            "role": "assistant",
            "content": content
        }
    ]

    if len(conversation_messages) > 0:
        recent_messages = conversation_messages[-10:]
        for msg in recent_messages:
            messages["smithy"].append(msg)

    messages["smithy"].append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages["smithy"],
        temperature=0.7,
        max_tokens=400,
        stream=False,
    )
    return response.choices[0].message.content

def run_action(action):
    print(magenta)
    print("Smithy is attempting to run an action:")
    print(action)
    confirmation = input("Allow action Y/n? ")
    if confirmation == "n":
        print(f"Action cancelled on user's request{reset}")
        conversation_messages.append({"role": "user", "content": "Cancel action"})
        conversation_messages.append({"role": "system", "content": "Action cancelled"})
    else:
        cmd = ["python", f"Plugins/{action["Action"]}/{action["Action"]}.py", str(action)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout.strip()+reset)
        conversation_messages.append({"role": "system", "content": result.stdout.strip()})

def smithy(user_input):
    while True:
        # ask smithy
        smithy = llm(user_input)
        # log to conversation messages
        conversation_messages.append({"role": "assistant", "content": smithy})
        # load json
        try:
            smithy = json.loads(smithy)
        except Exception as e:
            print(f"{red}Did smithy output invalid json?")
            print(e)
            print(smithy)
            print(reset)
            return

        global smithy_message
        global smithy_action
        # extract values to individual variables
        smithy_message = smithy["Message"]
        print(f"{blue}Smithy: {smithy_message}{reset}")
        smithy_action = smithy["Action"]
        smithy_continue = smithy["Continue"]

        # run action
        if smithy_action != {}:
            run_action(smithy_action)

        if smithy_continue != "True":
            break

def main(user_input):
    conversation_messages.append({"role": "user", "content": user_input})
    smithy(user_input)

if __name__ == "__main__":
    while True:
        user_input = input(f"{green}{NAME}: {reset}")
        main(user_input)
