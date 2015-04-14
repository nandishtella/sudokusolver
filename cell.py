__author__ = 'nandi_000'

class Cell:
    value = 0 # 0 to represent error value
    possible_values = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    def __init__(self):
        self.value = 0;
        self.possible_values = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9];

    def assign_value(self, value):
        self.value = value;
        if( value != 0 ):
            self.possible_values = [ value ]

    def remove_possible_values(self, value ):
        if value in self.possible_values:
            self.possible_values.remove( value )
        if( len( self.possible_values ) == 1 ):
            self.value = self.possible_values[0]

    def print_cell(self):
        print( self.value, end = "  " )

    def print_possible_values(self):
        print( self.possible_values )