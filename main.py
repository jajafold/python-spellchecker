from GUI import MainWindow, HandlerModes
import sys

# hello my freinds, im froum rusia, pleaze give me beer from kabinet.
# my freind is rusian kyborg.


def convert_to_mode(mode_str: str) -> HandlerModes:
    converter = {
        '--auto': HandlerModes.Autocorrect,
        '-a': HandlerModes.Autocorrect,

        '--light': HandlerModes.Highlight,
        '-l': HandlerModes.Highlight
    }

    return converter[mode_str]


if __name__ == "__main__":
    args = None
    if len(sys.argv) >= 2:
        args = sys.argv[1:]

    if args[0] in ['help', '-help', '--help', '-h']:
        print('''
    Welcome to Spellchecker v1.1
        
        
    Usage: main.py [option]
     -l,  --light        Spellchecker will only highlight misspelled words
     -a,  --auto             Spellchecker will automatically replace misspelled words
        ''')

        sys.exit()

    mode = None
    try:
        mode = convert_to_mode(args[0])
    except KeyError as e:
        print("First argument is invalid. Try --help to view valid startup arguments")
        sys.exit()

    if not mode:
        window = MainWindow()
    else:
        window = MainWindow(mode)



