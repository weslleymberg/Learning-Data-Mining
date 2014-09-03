from datetime import datetime
from collections import Counter
from itertools import chain, combinations

#Initial config
INPUT_FILE = './accidents_sample.dat'
OUTPUT_FILE = './rules.dat'
MIN_SUPPORT = 0.80
MIN_CONFIDENCE = 0.50

#Global variables
FILE_BUFFER = list()

def load_from_file():
    itemSet = set()
    with open(INPUT_FILE) as f:
        for record in f:
            transaction = record.split()
            FILE_BUFFER.append(frozenset(transaction))
            for item in transaction:
                itemSet.add(frozenset([item]))
    return itemSet

def filter_by_minimum_support(itemSet, freqSet):
    _dict = Counter()
    _itemSet = set()
    for item in itemSet:
        for transaction in FILE_BUFFER:
            if item.issubset(transaction):
                _dict[item] += 1

    for item, count in _dict.iteritems():
        if float(count) / len(FILE_BUFFER) >= MIN_SUPPORT:
            _itemSet.add(item)
            freqSet[item] = _dict[item]
    return _itemSet

def generate_k_itemset(source, lenght):
    return set((i.union(j) for i in source for j in source if len(i.union(j)) == lenght))

def generate_output(freqSet):
    lines = list()

    def get_support(item):
        return float(freqSet[item])/len(FILE_BUFFER)

    def get_confidence(xy, x):
        return get_support(xy) / get_support(x)

    def subsets(item):
        return chain(*(combinations(item, i+1) for i in xrange(len(item))))

    mask = "{} ==> {} = suppxy({:.2%}), suppx({:.2%}), conf({:.2%})\n"

    _freqSet = filter(lambda x: len(x)>1, freqSet)
    for item in _freqSet:
        _subset = map(frozenset, (x for x in subsets(item)))
        for element in _subset:
            remain = item.difference(element)
            if len(remain) > 0:
                confidence = get_confidence(item, element)
                if confidence >= MIN_CONFIDENCE:
                    lines.append(mask.format(element, remain, \
                                 get_support(element), get_support(remain),\
                                 confidence))
    with open(OUTPUT_FILE, 'w') as f:
        f.write("".join(lines))


if __name__ == '__main__':
    startTime = datetime.now()

    freqSet = dict()

    Ck = load_from_file()
    Lk = filter_by_minimum_support(Ck, freqSet)
    k = 2
    while True:
        print k-1, len(Lk)
        Ck = generate_k_itemset(Lk, k)
        new_Lk = filter_by_minimum_support(Ck, freqSet)
        if new_Lk == set([]):
            break
        Lk = new_Lk
        k += 1
        print '--'

    generate_output(freqSet)
    print 'It took', datetime.now()-startTime
