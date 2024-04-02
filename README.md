


# LPy to Python Compiler

This project provides a Python script that compiles an LPy file into a Python file. The LPy file allows you to write pseudo-code snippets wrapped in backticks and tagged with `[csm]` (ChatGPT Save Me!). The script uses the OpenAI ChatGPT model to convert these pseudo-code snippets into valid Python code.

## Requirements

- Python 3.x
- OpenAI Python library (`openai`)
- pyparsing library (`pyparsing`)

You can install the required libraries using the following command:

``pip install openai pyparsing``

## Setup

1. Obtain an API key from OpenAI by signing up for an account at [https://openai.com](https://openai.com).
2. Save your API key in a file named `.apikey` in one of the following locations:

   - On Windows: `%APPDATA%\.apikey`
   - On macOS: `~/.apikey`
   - On Linux: `~/.apikey`

   Alternatively, you can provide the API key using the `-a` flag when running the script (see Usage section).

## Usage

To compile an LPy file into a Python file, run the following command:

``python lpy.py (name of file I want to compile from lpy to py)``


Replace `(name of file I want to compile from lpy to py)` with the path to your LPy file.

If you haven't saved your API key in the `.apikey` file, you can provide it using the `-a` flag followed by the key:

``python lpy.py (name of file I want to compile from lpy to py) -a your_api_key``

The script will process the LPy file, convert the pseudo-code snippets tagged with `[csm]` into valid Python code using ChatGPT, and generate a corresponding Python file with the same name but with a `.py` extension.

## Example

Here's an example of an LPy file (`example.lpy`):

```python
def greet(name):
    `[csm]
    print a greeting message that says "Hello, (name)!"
    `

greet("Alice")
```

After running the compiler script:

```
python lpy.py example.lpy
```

The generated Python file (`example.py`) will look like this:

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
```

## Notes

- The script uses the `gpt-4` model by default for code conversion and error correction. Make sure you have access to this model through your OpenAI API key.
- Be mindful of the OpenAI API usage limits and associated costs. Each pseudo-code snippet conversion and error correction counts as an API request.
- The script attempts to compile the generated Python file and iteratively corrects any compilation errors using ChatGPT until the file successfully compiles.

## License

This project is licensed under the [MIT License](LICENSE).
