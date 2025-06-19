import ollama
import webbrowser
import tempfile
import os
import html
import sys


# --- Configuration ---
# You can change this to any model you have downloaded via Ollama
# e.g., "llama2", "mistral", "codellama", "llama3:8b", "llama3:70b"
DEFAULT_MODEL = "llama3"
# --- End Configuration ---     

#Prototypes
def check_ollama_connection_and_model(model_name):
    """Checks if Ollama is running and if the specified model is available."""
    pass
def generate_llm_response(client, model_name, prompt_text):
    """
    Sends the prompt to the Llama LLM via Ollama and gets the response.
    """
    pass
def display_in_browser(natural_input, llm_output):
    """
    Creates an HTML file with the input and output and displays it in the browser.
    """
    pass

def check_ollama_connection_and_model(model_name):
    """Checks if Ollama is running and if the specified model is available."""
    try:
        client = ollama.Client()
        client.list() # Simple check to see if the server is responsive
        print("Successfully connected to Ollama.")

        available_models = [m['name'].split(':')[0] for m in client.list()['models']]
        available_model_versions = [m['name'] for m in client.list()['models']]

        if model_name in available_model_versions or model_name.split(':')[0] in available_models:
            print(f"Model '{model_name}' or a version of it appears to be available.")
            return client
        else:
            print(f"Error: Model '{model_name}' not found in Ollama.")
            print("Available models:")
            if available_model_versions:
                for m in available_model_versions:
                    print(f"  - {m}")
            else:
                print("  No models found. Please pull a model using 'ollama pull <modelname>'.")
            print(f"You can try: 'ollama pull {model_name}' or choose from the list above.")
            return None

    except Exception as e:
        print(f"Error connecting to Ollama or listing models: {e}")
        print("Please ensure Ollama is running. You can start it by typing 'ollama serve' in your terminal (if installed as CLI) or by running the Ollama application.")
        return None

def generate_llm_response(client, model_name, prompt_text):
    """
    Sends the prompt to the Llama LLM via Ollama and gets the response.
    """
    print(f"\nSending prompt to Llama model '{model_name}':\n'{prompt_text}'")
    print("Waiting for response...")
    try:
        response = client.chat(
            model=model_name,
            messages=[
                {
                    'role': 'user',
                    'content': prompt_text,
                },
            ]
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error during LLM generation: {e}")
        return f"Error: Could not get a response from the LLM. Details: {str(e)}"

def display_in_browser(natural_input, llm_output):
    """
    Creates an HTML file with the input and output and displays it in the browser.
    """
    # Escape HTML special characters in the input and output
    safe_input = html.escape(natural_input)
    # For LLM output, we often want to preserve newlines and spaces,
    # so we'll wrap it in <pre> and escape.
    safe_output_html = html.escape(llm_output).replace('\n', '<br>')


    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LLM Response</title>
        <style>
            body {{ font-family: sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }}
            .container {{ background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #5a5a5a; }}
            h2 {{ color: #333; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
            .prompt, .response {{
                margin-bottom: 20px;
                padding: 15px;
                border-radius: 5px;
                border: 1px solid #ddd;
            }}
            .prompt {{ background-color: #e9efff; }}
            .response {{ background-color: #e9f9e9; }}
            pre {{
                white-space: pre-wrap;       /* CSS3 */
                white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
                white-space: -pre-wrap;      /* Opera 4-6 */
                white-space: -o-pre-wrap;    /* Opera 7 */
                word-wrap: break-word;       /* Internet Explorer 5.5+ */
                font-family: monospace;
                font-size: 0.95em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Llama LLM Interaction</h1>
            
            <div class="prompt">
                <h2>Your Input (Prompt):</h2>
                <p>{safe_input}</p>
            </div>
            
            <div class="response">
                <h2>LLM Response:</h2>
                <pre>{safe_output_html}</pre>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        # Create a temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as tmp_file:
            tmp_file.write(html_content)
            tmp_file_path = tmp_file.name
        
        print(f"Displaying output in browser: {tmp_file_path}")
        webbrowser.open('file://' + os.path.realpath(tmp_file_path))
        
        # Keep the script alive for a bit so the browser has time to open the file
        # On some systems, if the script exits too fast, the temp file might be cleaned up
        # before the browser fully loads it if delete=True was used.
        # With delete=False, we'd normally clean it up manually after a delay or user action.
        # For simplicity, let's prompt the user before cleaning up.
        input("Press Enter to close this script and delete the temporary HTML file...")
        os.unlink(tmp_file_path)
        print(f"Temporary file {tmp_file_path} deleted.")

    except Exception as e:
        print(f"Error displaying in browser: {e}")
        print("--- LLM Output (Console Fallback) ---")
        print(llm_output)
        print("------------------------------------")

def main():
    """Main function to run the script."""
    model_to_use = DEFAULT_MODEL
    
    # Allow overriding model from command line argument
    if len(sys.argv) > 1:
        model_to_use = sys.argv[1]
        print(f"Using model specified from command line: {model_to_use}")
    else:
        print(f"Using default model: {model_to_use}")

    ollama_client = check_ollama_connection_and_model(model_to_use)
    if not ollama_client:
        return

    print("\nEnter your natural language query for the Llama LLM.")
    print("Type 'exit' or 'quit' to end.")

    while True:
        natural_input = input("\nYour query: ")
        if natural_input.lower() in ['exit', 'quit']:
            print("Exiting...")
            break
        if not natural_input.strip():
            print("Please enter some text.")
            continue

        # In this case, the "natural English language" IS the prompt.
        # No special conversion is needed for basic interaction.
        # For more complex scenarios, you might add system prompts or formatting here.
        prompt = natural_input 

        llm_response_text = generate_llm_response(ollama_client, model_to_use, prompt)

        if llm_response_text:
            display_in_browser(natural_input, llm_response_text)

if __name__ == "__main__":
    main()