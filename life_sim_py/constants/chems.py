"""
chems have mass, potential and entropy
entropy calculations will consider the amount of these components

"""

chems = {
    # representing "carbon" type chemicals
    'energy': {
        'mass': 0.25,
        'potential': 0.9,
        'entropy': 0.1
    },
    # representing "nitrogen" type chemicals - "building blocks"
    'block': {
        'mass': 0.5,
        'potential': 0.4,
        'entropy': 0.3
    },
    # representing communication chemicals
    'signal': {
        'mass': 0.05,
        'potential': 0.05,
        'entropy': 0.05
    },
    # representing waste chemicals
    'waste': {
        'mass': 0.25,
        'potential': 0.1,
        'entropy': 0.9
    },
    # representing genes the cell has transported in
    'gene': {
        'mass': 0.1,
        'potential': 0.1,
        'entropy': 0.4
    },
}

