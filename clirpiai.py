#!/usr/bin/env python3
from openai import OpenAI

client = OpenAI()
import os
import sys
import logging
from colorama import Fore, Back, Style
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Models
model_in_use = "gpt-3.5-turbo"

# Initialize message history
messages = [{"role": "system", "content": "You are a helpful assistant"}]

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def check_api_key():
    """Check if the OpenAI API key is set."""
    if not os.getenv('OPENAI_API_KEY'):
        logging.error("OpenAI API key is not set. Please set it in environment variables.")
        sys.exit(1)

def openai_response(message):
    """Get a response from OpenAI."""
    global messages
    messages.append({"role": "user", "content": message})
    try:
        chat = client.chat.completions.create(model=model_in_use,
        messages=messages)
        reply = chat.choices[0].message.content
        print(Fore.CYAN + Style.BRIGHT + Back.BLACK + "Assistant: >>> " + Style.RESET_ALL, reply)
        messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        logging.error(f"Error getting response from OpenAI: {e}")

def interactive_mode():
    """Run the interactive mode."""
    clear_screen()
    print(Style.BRIGHT + Back.RED + Fore.WHITE + "Interactive Assistant Mode. Type 'exit' to quit or 'help' for commands." + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.GREEN + f"Model in use: {model_in_use}" + Style.RESET_ALL)

    while True:
        message = input(Style.BRIGHT + Fore.YELLOW + Back.BLACK + "Prompt: >>> " + Style.RESET_ALL).strip()
        if message.lower() == 'exit':
            print("Bye!")
            break
        elif message.lower().startswith('model'):
            change_model(message)
        elif message.lower() == 'list':
            list_models()
        elif message.lower() == 'help':
            print_help()
        else:
            openai_response(message)

def change_model(command):
    """Change the current OpenAI model."""
    global model_in_use
    try:
        new_model = command.split()[1]
        # Check if the new model is valid (optional enhancement)
        list_of_models = [model['id'] for model in client.models.list()['data']]
        if new_model in list_of_models:
            model_in_use = new_model
            print(f"Model successfully changed to: {model_in_use}")
        else:
            print("Model not found. Reverting to the previous model.")
    except IndexError:
        print("Invalid command. Usage: model MODEL_NAME")

def list_models():
    """List available OpenAI models."""
    try:
        models = client.models.list()
        print(f"Current OpenAI model: {model_in_use}")
        for model in models.data:
            print(model['id'])
    except Exception as e:
        logging.error(f"Error listing models: {e}")

def print_help():
    """Print help information."""
    print("Commands:")
    print("  list                  List available models")
    print("  model MODEL_NAME      Change the current model")
    print("  exit                  Exit interactive mode")

def read_from_stdin():
    """Read input from stdin and process it."""
    print("Reading input from standard input. Press Ctrl+D (or Ctrl+Z on Windows) to end input.")
    input_data = sys.stdin.read().strip()
    if input_data:
        openai_response(input_data)

def main():
    """Main function to run the script."""
    check_api_key()

    if len(sys.argv) < 2:
        print("Error: Please provide at least one parameter. Use '-h' to see the usage.")
        sys.exit(1)

    mode = sys.argv[1]
    global model_in_use

    # Handle optional model argument
    if len(sys.argv) > 3 and sys.argv[2] == '--model':
        model_in_use = sys.argv[3]
        args_start_index = 4
    else:
        args_start_index = 2

    if mode == "-i":
        interactive_mode()
    elif mode == "-t" and len(sys.argv) > args_start_index:
        message = ' '.join(sys.argv[args_start_index:])
        openai_response(message)
    elif mode == "-s":
        read_from_stdin()
    elif mode == "-h":
        print("Usage:")
        print("  clirpiai -i [--model MODEL_NAME]     : for interactive mode")
        print("  clirpiai -t [--model MODEL_NAME] TEXT: to respond to the text")
        print("  clirpiai -s [--model MODEL_NAME]     : to read input from standard input")
    else:
        print("Error: Invalid parameter or missing query. Use '-h' to see the usage.")

if __name__ == "__main__":
    main()