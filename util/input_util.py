import sys
from pathlib import Path


def get_input() -> str:
    """Parse the day from the script name, open the corresponding input file."""
    script_file_name = Path(sys.argv[0]).name

    try:
        # Only look at the digits in the file name, combine those
        day_number = int(''.join(c for c in script_file_name if c.isdigit()))
    except ValueError:
        raise ValueError(f'Unexpected script name: {script_file_name}')

    input_file = Path(__file__).parent.parent / 'input' / f'{day_number:02d}.txt'
    return input_file.read_text().strip('\n')
