import os
import sys
import openai
from pyparsing import QuotedString
import platform

def get_api_key_path():
    if platform.system() == 'Windows':
        api_key_path = os.path.join(os.getenv('APPDATA'), '.apikey')
    elif platform.system() == 'Darwin':
        api_key_path = os.path.expanduser('~/.apikey')
    else:
        api_key_path = os.path.expanduser('~/.apikey')
    return api_key_path

def load_api_key(api_key_path):
    with open(api_key_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

def save_api_key(api_key, api_key_path):
    with open(api_key_path, 'w') as file:
        file.write(api_key)

def process_lpy_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        
    print("reached")

    csm_snippets = QuotedString('`', multiline=True).setParseAction(lambda t: t[0][1:-1]).searchString(content)

    for snippet in csm_snippets:
        if '[csm]' in snippet:
            code_snippet = snippet.split('[csm]')[1].strip()
            print(f"Processing code snippet: {code_snippet}")
            converted_code = convert_with_chatgpt(code_snippet)
            content = content.replace(f'`{snippet}`', converted_code)

    py_file_path = file_path.replace('.lpy', '.py')
    
    if os.path.exists(py_file_path):
        os.remove(py_file_path)
    
    with open(py_file_path, 'w') as file:
        file.write(content)

    while True:
        try:
            compile(content, py_file_path, 'exec')
            print(f"Successfully compiled: {py_file_path}")
            break
        except SyntaxError as e:
            print(f"Compilation error: {str(e)}")
            corrected_code = correct_with_chatgpt(content, str(e))
            content = corrected_code
            with open(py_file_path, 'w') as file:
                file.write(content)

def convert_with_chatgpt(code_snippet):
    prompt = f"Please convert the following description / pseudo-code into valid Python:\n\n```{code_snippet}```\n\nProvide only the converted Python code in your response, without any explanations. Do not include the original description / pseudo-code in your response. You are being queried by an API to generate code so please make do and write code that compiles and do not respond with words or with markdown."

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    print(response.choices[0].message)

    converted_code = response.choices[0].message.content.strip()
    return converted_code

def correct_with_chatgpt(code, error_message):
    prompt = f"The following Python code has a compilation error:\n\n```{code}```\n\nError message: {error_message}\n\nPlease correct the code and provide only the corrected Python code in your response, without any explanations. You are being queried by an API to generate code so please make do and write code that compiles and do not respond with words or with markdown."

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    corrected_code = response.choices[0].message.content.strip()
    return corrected_code

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the path to the .lpy file as a command-line argument.")
        sys.exit(1)

    lpy_file_path = sys.argv[1]

    api_key_path = get_api_key_path()

    if '-a' in sys.argv:
        api_key_index = sys.argv.index('-a') + 1
        if api_key_index < len(sys.argv):
            api_key = sys.argv[api_key_index]
            save_api_key(api_key, api_key_path)
        else:
            print("Please provide an API key after the -a flag.")
            sys.exit(1)
    else:
        try:
            api_key = load_api_key(api_key_path)
        except FileNotFoundError:
            print(f"API key file not found at {api_key_path}. Please provide an API key using the -a flag.")
            sys.exit(1)

    openai.api_key = api_key

    process_lpy_file(lpy_file_path)