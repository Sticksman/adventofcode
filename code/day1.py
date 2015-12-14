counter = 0
with open('adventofcode/inputs/day1', 'r') as f:
    instructions = f.read()
    for i, instruction in enumerate(instructions):
        if instruction == '(':
            counter += 1
        elif instruction == ')':
            counter -= 1

        if counter == -1:
            break

print counter
print i + 1
