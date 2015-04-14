__author__ = 'nandi_000'

import cell
import copy

class Grid:
    matrix = [[]]

    def __init__(self):
        self.matrix = [ [ cell.Cell() for j in range( 0, 9 ) ] for i in range( 0, 9 ) ]
#        for i in range( 0, 9 ):
#            for j in range( 0, 9 ):
#                self.matrix[i][j] = cell.Cell()

    def print_grid(self):
        for i in range( 0, 9 ):
            for j in range( 0, 9 ):
                self.matrix[i][j].print_cell()
            print( "\n" )

    def grid_initialize(self, matrix ):
        for i in range( 0, 9 ):
            for j in range( 0, 9 ):
                self.matrix[i][j].assign_value( matrix[i][j]);

    def has_state_changed(self, matrix ):
        for i in range( 0, 9 ):
            for j in range( 0, 9 ):
                diff = set( matrix[i][j].possible_values ) - set( self.matrix[i][j].possible_values )
                #print( i, j, diff, set( matrix[i][j].possible_values ), set( self.matrix[i][j].possible_values ) )
                if( len( diff ) ):
                    return( True )
        return( False )

    def run_next_round(self):
        for i in range( 0, 9 ):
            for j in range( 0, 9 ):
                cell = self.matrix[i][j];
                # remove everything in the same row
                row_list = [1,2,3,4,5,6,7,8,9]
                for k in range( 0, 9 ):
                    if( k != j ):
                        cell.remove_possible_values( self.matrix[i][k].value)
                        row_list = set( row_list ) - set( self.matrix[i][k].possible_values )

                #remove everything in the same column
                column_list = [1,2,3,4,5,6,7,8,9]
                for k in range( 0, 9 ):
                    if( k != i ):
                        cell.remove_possible_values( self.matrix[k][j].value )
                        column_list = set( column_list ) - set( self.matrix[k][j].possible_values )

                #remove everything in the same 3X3
                row = 3 * int( i/3 );
                column = 3 * int( j/3 );
                box_list = [1,2,3,4,5,6,7,8,9]
                for row_i in range( row, row + 3 ):
                    for column_j in range( column, column + 3 ):
                        if( row_i != i or column_j != j ):
                            cell.remove_possible_values( self.matrix[row_i][column_j].value)
                            box_list = set( box_list ) - set( self.matrix[row_i][column_j].possible_values )

                missing_elements = list( row_list ) + list( column_list ) + list( box_list )
                #print( missing_elements )
                if( len( missing_elements ) > 0):
                    cell.assign_value( missing_elements[0] )
                # Do the above steps for elements missing from union of row and intersection with possible values
                self.matrix[i][j] = cell

    def solve(self):
        i = 0;
        while( True ):
            i += 1;
            matrix = copy.deepcopy( self.matrix )
            self.run_next_round()
            state_change = self.has_state_changed( matrix )
            if( state_change == False ):
                print( "Solved in ", i, " iterations" )
                break
        return( self.state() )

    # call this once we reach a steady state
    # 0 for failed state, 1 is for solved state, 2 is for intermediate
    def state(self):
        row_stats = [];
        column_stats = [];
        box_stats = [];

        # first check for state 0
        for i in range( 0, 9 ):
            for j in range( 0, 9 ):
                if( len( self.matrix[i][j].possible_values ) == 0 ):
                    return( 0 );

        # populate row stats, column stats and box stats as a dictionary in list
        for i in range( 0, 9 ):
            stats = dict( zip( [ 0,1,2,3,4,5,6,7,8,9 ], [ 0,0,0,0,0,0,0,0,0,0 ] ) )
            for j in range( 0, 9 ):
                stats[ self.matrix[i][j].value ] += 1
            for key in stats:
                if( key != 0 and stats[ key ] > 1 ):
                    return( 0 )

        for j in range( 0, 9 ):
            stats = dict( zip( [ 0,1,2,3,4,5,6,7,8,9 ], [ 0,0,0,0,0,0,0,0,0,0 ] ) )
            for i in range( 0, 9 ):
                stats[ self.matrix[i][j].value ] += 1
            for key in stats:
                if( key != 0 and stats[ key ] > 1 ):
                    return( 0 )

        for row in range( 0, 3 ):
            for column in range( 0, 3 ):
                stats = dict( zip( [ 0,1,2,3,4,5,6,7,8,9 ], [ 0,0,0,0,0,0,0,0,0,0 ] ) )
                for row_i in range( 3 * row, 3 * row + 3 ):
                    for column_j in range( 3 * column, 3 * column + 3 ):
                        stats[ self.matrix[row_i][column_j].value ] += 1

                for key in stats:
                    if( key != 0 and stats[ key ] > 1 ):
                        return( 0 )

        #checking for state 1 and 2 is trivial. 1 is the state where there is atleast a zero while 2 is no zeros

        for i in range( 0, 9 ):
            for j in range( 0, 9 ):
                if( self.matrix[i][j].value == 0 ):
                    return( 1 )

        return( 2 )
            #verify the stats

    # This returns 0 for a failed solution and 2 for a successful solution
    def solve_recursive(self):
        state = self.solve()

        #check the state and if state is 2, return the result = 2
        if( state == 2 ):
            return( 2 )

        if( state == 0 ):
            return( 0 ) #No solution found and this will not happen in base state

        #make a copy of the solution if state is 1
        board = copy.deepcopy( self.matrix )


        #if state is 1, choose an element with least possible values and for all possible values
        #while all values, check substitute each possible value unless we get a 2 from child call
        for i in range( 0,9 ):
            for j in range( 0, 9 ):
                if( len( self.matrix[i][j].possible_values ) > 1 ):
                    break;

        for value in self.matrix[i][j].possible_values:
            self.matrix[i][j].assign_value( value )
            print( "Going a level deeper" )
            state = self.solve_recursive()
            if( state == 2 ):
                return( state )
            if( state == 0 ):
                print( "backtracking" )
                self.matrix = copy.deepcopy( board )
