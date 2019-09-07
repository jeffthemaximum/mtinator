DATA = [
    {
        'lines': ['1', '2', '3', '4', '5', '6', 'S'],
        'feed_id': 1
    },
    {
        'lines': ['A', 'C', 'E', 'H'],
        'feed_id': 26
    },
    {
        'lines': ['N', 'Q', 'R', 'W'],
        'feed_id': 16
    },
    {
        'lines': ['B', 'D', 'F', 'M'],
        'feed_id': 21
    },
    {
        'lines': ['L'],
        'feed_id': 2
    },
    {
        'lines': ['G'],
        'feed_id': 31
    },
    {
        'lines': ['J', 'Z'],
        'feed_id': 36
    },
    {
        'lines': ['7'],
        'feed_id': 51
    },
]


def flatten(l):
    return [item for sublist in l for item in sublist]


def line_to_feed_id(line):
    return next((x['feed_id'] for x in DATA if line in x['lines']), None)


def all_lines():
    return flatten([datum['lines'] for datum in DATA])
