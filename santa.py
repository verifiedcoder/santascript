#!/usr/bin/env python3
import sys
from santa_lexer import lexer
from santa_parser import parser
from santa_runtime import SantaRuntime


def run_santa_script(code):
    # Initialize runtime
    runtime = SantaRuntime()

    # Parse and execute
    try:
        print("Parsing code...")
        ast = parser.parse(code, lexer=lexer)
        if ast:
            print("Executing code...")
            output = runtime.execute(ast)
            return output
        else:
            print("🎅 Ho ho NO! Parsing failed!")
            return None
    except Exception as e:
        print(f"🎅 Ho ho NO! An error occurred: {str(e)}")
        return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python santa.py <filename.santa>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()

        result = run_santa_script(code)
        if result:
            print("\n🎄 Output:")
            for item in result:
                print(f"🎁 {item}")

    except FileNotFoundError:
        print(f"🎅 Ho ho NO! Could not find file: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"🎅 Ho ho NO! An unexpected error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()