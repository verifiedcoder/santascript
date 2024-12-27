import os
from santa_lexer import lexer
from santa_parser import parser
from santa_runtime import SantaRuntime


def run_example():
    print("🎄 North Pole Gift Management System 🎄")
    print("=======================================")

    try:
        print("📜 Checking for example.santa...")
        if not os.path.exists('example.santa'):
            raise FileNotFoundError("example.santa not found")

        # Read the example file
        with open('example.santa', 'r', encoding='utf-8') as f:
            code = f.read()

        print(f"📜 File length: {len(code)} characters")
        print("📜 File contents:")
        print("---------------------------------------")
        print(repr(code))
        print("---------------------------------------")

        print("🎅 Initializing runtime...")
        runtime = SantaRuntime()
        print("✓ Runtime initialized")

        print("🎅 Tokenizing code...")
        lexer.input(code)
        tokens = list(lexer)
        print("Tokens found:")
        for tok in tokens:
            print(f"    {tok.type}: {repr(tok.value)}")

        print("🎅 Parsing code...")
        lexer.input(code)  # Reset lexer
        ast = parser.parse(code, lexer=lexer)

        if ast:
            print("✓ AST generated:")
            print(ast)

            print("🎁 Executing North Pole operations...")
            print("---------------------------------------")

            output = runtime.execute(ast)
            print(f"✓ Execution complete, output length: {len(output)}")

            print("\n✨ Program Output:")
            print("---------------------------------------")
            for item in output:
                print(f"🎄 {item}")

        else:
            print("❌ Ho ho NO! Parsing failed!")

    except ImportError as e:
        print(f"❌ Ho ho NO! Missing module: {str(e)}")
        print("Make sure santa_runtime.py is in the same directory")
    except FileNotFoundError as e:
        print(f"❌ Ho ho NO! {str(e)}")
    except Exception as e:
        print(f"❌ Ho ho NO! An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n=======================================")
        print("🎅 Santa's Workshop closing for the day!")


if __name__ == "__main__":
    run_example()