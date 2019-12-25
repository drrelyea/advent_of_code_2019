import numpy as np
with open('/Users/relyea/data/day22input.txt') as input_file:
    inpstring = input_file.readlines()

newlist = [aa.strip('\n') for aa in inpstring]

N = 10007
N = 101
deck = np.arange(N)



def deal_into_new_stack(deck):
    return deck[::-1]

def cut_k_cards(deck, k):
    listdeck = list(deck)
    return np.array(listdeck[k:] + listdeck[:k])

def phase_shuffle(deck, k):
    the_indices = np.argsort(np.arange(N)*k % N)
    return deck[the_indices]

for line in newlist:
    if "cut" in line:
        deck = cut_k_cards(deck, int(line[4:]))
    elif "deal into" in line:
        deck = deal_into_new_stack(deck)
    elif "deal with" in line:
        deck = phase_shuffle(deck, int(line[20:]))

# print(deck)


two phases in a row are a phase of the product of the two numbers
a phase A followed by a cut B is a cut of  followed by a phase A

so this is mod arithmetic

if I had to cut 1e13 times, I could track a card due to mod
if I had to reverse and cut 1e13 times, it would be easier because it would just be levels of undo

if I had to undo an argsort applied 1e13 times, the card still only travels due to a mod, so undoing it is not hard
and ditto with the cut or the reverse

new stack is a reverse of all actions
deal with increment 5 means 

thecardposition * 5 mod N = newposition

bignum * 5 = somenumber*N + remainder newposition