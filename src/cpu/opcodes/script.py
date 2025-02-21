import json
from pprint import pprint

# self, code, mnemonic, length, tcycles, instructions
with open("Opcodes.json") as f:
    opcodes = json.load(f)
    unprefixed = opcodes["unprefixed"]
    count = 0
    for k, v in unprefixed.items():
        count += 1
        print(k)
        m = unprefixed[k]['mnemonic']
        b = unprefixed[k]['bytes']
        c = unprefixed[k]['cycles'][0]
        operands = ''
        if unprefixed[k]["operands"]: 
            for op in unprefixed[k]["operands"]:
                operands += (op['name']) + ' '
        if operands:
            m += ' ' + operands.rstrip()
        print(f'Opcode({k}, {m}, {b}, {c})')
        if count == 2: exit(1)

# with open("dump_opcodes") as f:
#     for k, v in opcodes["unprefixed"]:
#         pass
# with open('example.py', 'w') as f:
#     f.write("def f(x): x + x")