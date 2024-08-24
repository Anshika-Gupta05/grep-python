import sys
import re

def convert_to_list(pattern):
    pattern = pattern.replace("\\d", "[\\d]")
    pattern = pattern.replace("\\w", "[\\w]")
    ignore = False
    new_string = ""
    for i in pattern:
        if ignore:
            if i == "]":
                new_string += i
                ignore = False
            else:
                new_string += i
        elif i == "[":
            new_string += i
            ignore = True
        else:
            new_string += f"[{i}]"
    new_string = new_string.replace("][", ",")
    new_string = new_string.replace("]", "")
    new_string = new_string.replace("[", "")
    return new_string.split(",")

def compare(substring, pattern_list):
    bool_list = []
    for i in range(len(pattern_list)):
        if pattern_list[i] == "\\d":
            bool_list.append(substring[i].isdigit())
        elif pattern_list[i] == substring[i]:
            bool_list.append(True)
        elif pattern_list[i] == "\\w":
            bool_list.append(substring[i].isalpha())
        else:
            bool_list.append(False)
    return all(bool_list)

def optional_qualifier(input_line):
    num = input_line.find("?")
    return [
        f"{input_line[:num]}{input_line[num+1:]}",
        f"{input_line[:num-1]}{input_line[num+1:]}",
    ]

def wildcard(word, c):
    num = word.find(".")
    if word[:num] in c and word[num + 1 :] in c:
        if len(c[c.find(word[:num]) : c.find(word[num + 1 :])]) == len(word[:num]) + 1:
            return True
        else:
            return False
    else:
        return False

def alternation(word, c):
    word = word.replace("(", "")
    word = word.replace(")", "")
    num = word.find("|")
    if word[:num] in c or word[num + 1 :] in c:
        return True
    else:
        return False

def single_backreferrence(word, c):
    word_list = word.split(" ")
    word_list[0] = word_list[0].replace("(", "")
    word_list[0] = word_list[0].replace(")", "")
    num = c.find("and")
    if word_list[0] == "\\w+":
        if {c[: num - 1]} == {c[num + 4 :]}:
            return True
        else:
            return False
    else:
        if f"{word_list[0]} and {word_list[0]}" in c:
            return True
        else:
            return False

def match_pattern(input_line, pattern):
    pattern_types = {
        '[': lambda p: any(char not in p[1:-1] for char in input_line),
        '^': lambda p: input_line.startswith(p[1:]),
        '$': lambda p: input_line.endswith(p[:-1]),
        '+': lambda p: p[:p.find('+')] in input_line,
        '?': lambda p: any(qual in input_line for qual in optional_qualifier(p)),
        '.': lambda p: wildcard(p, input_line),
        '|': lambda p: alternation(p, input_line),
    }

    for pattern_type, matcher in pattern_types.items():
        if pattern_type in pattern:
            return matcher(pattern)

    # Fallback to the custom matching logic
    start = 0
    end = len(convert_to_list(pattern))
    final = []
    if len(input_line) < len(convert_to_list(pattern)):
        return False
    else:
        while end != len(input_line) + 1:
            final.append(compare(input_line[start:end], convert_to_list(pattern)))
            start += 1
            end += 1
        return any(final)

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)
    print("Logs from your program will appear here!")
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()