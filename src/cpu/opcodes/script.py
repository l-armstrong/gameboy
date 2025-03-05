import json
from pprint import pprint

# self, code, mnemonic, length, tcycles, instructions
with open("Opcodes.json") as f:
    opcodes = json.load(f)
    # unprefixed = opcodes["unprefixed"]
    # count = 0
    # for k, v in unprefixed.items():
    #     count += 1
    #     m = unprefixed[k]['mnemonic']
    #     b = unprefixed[k]['bytes']
    #     c = unprefixed[k]['cycles'][0]
    #     operands = ''
    #     if unprefixed[k]["operands"]: 
    #         for op in unprefixed[k]["operands"]:
    #             operands += (op['name']) + ' '
    #     if operands:
    #         m += ' ' + operands.rstrip()
    #     print(f'{k}: Opcode({k}, {m}, {b}, {c}),')
    #     if count == 4: exit(1)

with open("cb_dump_opcodes", "w") as f:
    unprefixed = opcodes["cbprefixed"]
    f.write("{")
    for k, v in unprefixed.items():
        m = unprefixed[k]['mnemonic']
        b = unprefixed[k]['bytes']
        c = unprefixed[k]['cycles'][0]
        operands = ''
        if unprefixed[k]["operands"]: 
            for op in unprefixed[k]["operands"]:
                operands += (op['name']) + ' '
        if operands:
            m += ' ' + operands.rstrip()
        f.write(f'    {k}: Opcode({k}, "{m}", {b}, {c}),\n')
    f.write("}")

# with open("dump_opcodes") as f:
#     for k, v in opcodes["unprefixed"]:
#         pass
# with open('example.py', 'w') as f:
#     f.write("def f(x): x + x")