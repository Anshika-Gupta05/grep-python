import sys
class Pattern:
    DIGIT = "\d"
    ALNUM = "\w"
# import pyparsing - available if you need it!
# import lark - available if you need it!
# def combined_patterns(input_line, pattern):


def match_pattern(input_line, pattern):
    # if len(pattern) == 1:
    #     return pattern in input_line
    # elif pattern == "\\d":
    #     return any(c.isdigit() for c in input_line)
    # elif pattern == "\\w":
    #     return any(char.isalnum() for char in input_line)
    if len(input_line) == 0 and len(pattern) == 0:
        return True
    if not pattern:
        return True
    if not input_line:
        return False
    if pattern[0] == input_line[0]:
        return match_pattern(input_line[1:], pattern[1:])
    elif pattern[:2] == Pattern.DIGIT:
        for i in range(len(input_line)):
            if input_line[i].isdigit():
                return match_pattern(input_line[i:], pattern[2:])
        else:
            return False
    elif pattern[:2] == Pattern.ALNUM:
        if input_line[0].isalnum():
            return match_pattern(input_line[1:], pattern[2:])
        else:
            return False
    elif pattern[0] == "[" and pattern[-1] == "]":
        if pattern[1] == "^":
            return not any(char in pattern for char in input_line)
        return any(char in pattern[1:-1] for char in input_line)
    else:
        # raise RuntimeError(f"Unhandled pattern: {pattern}")
        return match_pattern(input_line[1:], pattern)



def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
