import csv
from collections import Counter

blacklist = ['TON', ' CITY', 'SVILLE', 'VILLE', 'LAND', 'FIELD']

def extend_suffix(cities, base):
    cities = [city for city in cities if city.endswith(base)]
    base_matches = len(cities)
    l = len(base) + 1
    suffixes = Counter(city[-l:] for city in cities if len(city) >= l)
    return [s for s in suffixes if suffixes[s] > base_matches ** .75]

def get_suffixes(cities):
    suffixes = [x for x,y in Counter(s[-1] for s in cities).items() if y > 0.05 * len(cities)]

    final_suffixes = []
    while len(suffixes):
        new_suffixes = []
        for b in suffixes:
            s = extend_suffix(cities, b)
            if not len(s) and len(b) > 2:
                final_suffixes.append(b)
            else:
                new_suffixes += s
        suffixes = new_suffixes
    return Counter({x: sum(1 for c in cities if c.endswith(x)) for x in final_suffixes if x not in blacklist})

def get_prefixes(cities):
    cities = [x[::-1] for x in cities]
    return Counter({x[::-1]: y for x,y in get_suffixes(cities).items()})

reader = csv.reader(open('Govt_Units_2017_Final.csv'))
rows = [line for line in reader][1:]
by_state = {k: [row[1].split(' OF ', maxsplit=1)[1] for row in rows if row[6] == k] for k in set(row[6] for row in rows)}
endings_by_state = {st: Counter(x[-1:] for x in by_state[st]) for st in by_state}

unique_endings_by_state = {st: Counter(x[-3:] for x in set(by_state[st])) for st in by_state}

# print(get_suffixes(set(sum(by_state.values(), []))))

for state in sorted(by_state.keys()):
    cities = set(by_state[state])
    prefixes, suffixes = get_prefixes(cities), get_suffixes(cities)
    if len(prefixes) + len(suffixes):
        print(state, prefixes, suffixes)

    
