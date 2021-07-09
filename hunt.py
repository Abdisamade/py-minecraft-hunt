from random import randint

def read_in_array(file):
    array = []
    with open(file, 'r') as f:
        for line in f:
            array.append(line[0:-1])

    return array

items = read_in_array('./items.txt')
blocks =read_in_array('./blocks.txt')
mobs = read_in_array('./mobs.txt')

random_items_seq = []
random_blocks_seq = []
random_mobs_seq = []

for i in range(5):
    random_items_seq.append(items[randint(0, len(items))])

for i in range(5):
    random_blocks_seq.append(blocks[randint(0, len(blocks))])

for i in range(5):
    random_mobs_seq.append(mobs[randint(0, len(mobs))])

print("To find: ", random_items_seq)
print("To find: ", random_blocks_seq)
print("To kill: ", random_mobs_seq)

input("")