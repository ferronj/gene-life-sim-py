SENSORS = [
    #'POSITION',
    'POSITION_VECTOR',
    'MASS',
    'POTENTIAL',
    'ENTROPY',
    'GENE',
    'GENOME_LENGTH',
    'DETECT_ENERGY',
    'DETECT_BLOCK',
    'DETECT_SIGNAL',
    'DETECT_WASTE',
    'DETECT_GENE',
    'DETECT_CELL',
    'DETECT_PHOTO'
]

ACTIONS = [
    'MOVE',  # movement will be f(mass)
    'TURN',  # movement will be f(mass)
    'GROW',  # POTENTIAL_TO_MASS
    'REPRODUCE',  # BIT-FLIP MUTATION
    'DIE',
    'ATTACK',
    'ADD_GENE',
    'CUT_GENE',
    # Transports will affect the resource balance
    'TRANSPORT_IN_ENERGY',
    'TRANSPORT_IN_BLOCK',
    'TRANSPORT_IN_SIGNAL',
    'TRANSPORT_IN_WASTE',
    'TRANSPORT_IN_GENE',
    'TRANSPORT_OUT_ENERGY',
    'TRANSPORT_OUT_BLOCK',
    'TRANSPORT_OUT_SIGNAL',
    'TRANSPORT_OUT_WASTE',
    'TRANSPORT_OUT_GENE',
    # Not sure if this makes sense yet...
    # Trying to solve the cell resource problem
    'MASS_TO_POTENTIAL',
    'MASS_TO_ENTROPY',
    'POTENTIAL_TO_MASS',
    'POTENTIAL_TO_ENTROPY',
    'ENTROPY_TO_MASS',
    'ENTROPY_TO_POTENTIAL',
    'PHOTO_TO_POTENTIAL',
    'POTENTIAL_TO_PHOTO'
]