with open('tasks/day1/input.txt') as f:
    lines = f.read().strip().split('\n')

pos = 50
count = 0
for line in lines:
    direction = line[0]
    amount = int(line[1:])
    if direction == 'L':
        pos = (pos - amount) % 100
    else:
        pos = (pos + amount) % 100
    if pos == 0:
        count += 1

print(count)