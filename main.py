import re,sys

def find_placeholders(search_string: str, pattern: str) -> list[str]:
    parts = pattern.split('%s')
    regex = ''
    num_parts = len(parts)
    for i, part in enumerate(parts):
        regex += re.escape(part)
        if i < num_parts - 1:
            # Use greedy capture if this is the last placeholder and the pattern ends with it.
            if i == num_parts - 2 and parts[-1] == '':
                regex += '(.+)'  
            else:
                regex += '(.+?)'
    match = re.search(regex, search_string)
    return list(match.groups()) if match else []

def find_matching_pattern(search_string: str, patterns: list[str]) -> tuple[int, str, list[str]] | None:
    """
    Tries each pattern in the list against search_string.
    Returns a tuple (pattern_index, pattern, captured_list) for the first matching pattern.
    If no pattern matches, returns None.
    """
    for idx, pattern in enumerate(patterns):
        captured = find_placeholders(search_string, pattern)
        if captured:
            return idx, pattern, captured
    return None

def cut_line(s):
    from copy import deepcopy
    stack.append(deepcopy(stack)[-(s+1)])
    del stack[-(s+1)]
def charify(s):
    stack[-(int(s)+1)] = chr(stack[-(int(s)+1)])
def print_stack(s):
    print(stack[-(int(s)+1)])
def asciify(s):
    stack[-(int(s)+1)] = ord(stack[-(int(s)+1)])
stack = []

def parse_range(range_str):
    """
    Parses a string that is either a single number or in the format "l-h".
    If a single number is provided, it returns a list with that number.
    If "l-h" is provided, it returns a list of integers from l to h (inclusive).
    """
    if '-' in range_str:
        low, high = map(int, range_str.split('-'))
        return list(range(low, high + 1))
    elif "x" in range_str:
        n, times = map(int, range_str.split('x'))
        return [int(n)]*times
    elif "," in range_str:
        return list(map(int, range_str.split(',')))
    else:
        # Only a single number is provided.
        return [range_str]

def run_func_on_ranges(func, *range_strs):
    """
    Takes a function and an arbitrary number of range strings.
    Each range string is parsed into a list of integers.
    The function is then called with one element from each range at a time,
    using zip which stops at the shortest list.
    """
    # Parse each range string into a list
    range_lists = [parse_range(rs) for rs in range_strs]
     
    # Iterate over the corresponding elements of each list
    for args in zip(*range_lists):
        func(*args)

def repeat(num:str):
    if num == "infinite" or num == "inf":
        result = find_matching_pattern(code[idx-1].split("#")[0].strip(),list(instructionmap.keys()))
        while True:
            run_func_on_ranges(list(instructionmap.values())[result[0]], *result[2])
    else:
        result = find_matching_pattern(code[idx-1].split("#")[0].strip(),list(instructionmap.keys()))
        for _ in range(int(num)):
            run_func_on_ranges(list(instructionmap.values())[result[0]], *result[2])

def if_func(s):
    if stack[-(int(s)+1)] <= 0:
        result = find_matching_pattern(i.split("#")[1].strip(),list(instructionmap.keys()))
        run_func_on_ranges(list(instructionmap.values())[result[0]], *result[2])
    else:
        if len(i.split("#")) == 3:
            result = find_matching_pattern(i.split("#")[2].strip(),list(instructionmap.keys()))
            run_func_on_ranges(list(instructionmap.values())[result[0]], *result[2])

def numify(s):
    stack[-(int(s)+1)] = int(stack[-(int(s)+1)])
def strify(s):
    stack[-(int(s)+1)] = str(stack[-(int(s)+1)])

instructionmap = {
    "%s my ass": lambda v:stack.append(int(v)),
    "%s go touch grass": print_stack,
    "make %s fuck %s": lambda p1,p2: stack.append(stack[-(int(p1)+1)] + stack[-(int(p2)+1)]),
    "%s and %s had a miscarriage": lambda p1,p2: stack.append(stack[-(int(p1)+1)] - stack[-(int(p2)+1)]),
    "make %s get %s pregnant": lambda p1,p2: stack.append(stack[-(int(p1)+1)] * stack[-(int(p2)+1)]),
    "make %s preform lobotomy on %s": lambda p1,p2: stack.append(stack[-(int(p1)+1)] / stack[-(int(p2)+1)]),
    "let %s cut the line": cut_line,
    "%s get out":lambda s:stack.pop(-(int(s)+1)),
    "%s present to the class":lambda s:stack.append(input(stack[-(int(s)+1)])),
    "what was the %s thing you said %s":lambda s: stack.append(str(stack[-(int(s)+1)])[int(s)]),
    "%s needs more character development":charify,
    "%s said he has a lot of girls if he is lying i would":if_func,
    "%s said he has a lot of guys if he is lying i would":if_func,
    "%s has too much main character energy":asciify,
    "decapitate %s":numify,
    "recapitate %s":strify,
    "repeat that %s more times":repeat,
    "commit mass murder but leave a note %s":lambda s: exit(int(s))
}
try:
    code = open(sys.argv[1],"r").read().lower().split("\n")
except:
    exit("Please provide a script file")
debug = "debug" in sys.argv
try:
    for idx,i in enumerate(code):
        result = find_matching_pattern(i.split("#")[0].strip(),list(instructionmap.keys()))
        if result:
            if debug:print(result[1]);print(result[2])
            run_func_on_ranges(list(instructionmap.values())[result[0]], *result[2])
except BaseException as e:
    import os
    e.add_note(f"File {os.path.abspath(sys.argv[1])}, line {idx+1}\n    {i}")
    raise e
if debug:stack.reverse();print(stack)
