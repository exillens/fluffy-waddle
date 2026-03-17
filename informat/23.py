from itertools import count

f = open('26_7626.txt')
k = int(f.readline())
n = int(f.readline())
people = []
for i in range(n):
    p1, p2 = [int(x) for x in f.readline().split()]
    people.append((p1, p2))
people.sort()

cells = [0] * k
count = 0
last = []

for i in range(len(people)):
    p1, p2 = people[i]
    for j in range(len(cells)):
        if p1 > cells[j]:
            count += 1
            cells[j] = p2
            last.append([p1, j+1])
            break

print(count)
print(last)