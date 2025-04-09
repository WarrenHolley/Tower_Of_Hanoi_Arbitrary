# A Tower of Hanoi implementation.
# Thrown together after I nerd-sniped myself asking
#  'What if the Tower of Hanoi had more than 3 pegs?'
#######
# Written 2021-11 - Warren Holley
#######
# Potential Upgrades:
## More setup conditions
## - Arbitrary Source/Target pegs
## Variant Rules?
## Derive the formula. Wikipedia's got a whole section on theory, but it's limited to 3-peg TOH.
## Improve the debug output.

import argparse

MOVE_COUNTER = 0 
TOWER_STRUCT = None
DEBUG_PRINT  = False


def Setup_Tower( Peg_Count, Stack_Size ):
  global TOWER_STRUCT
  TOWER_STRUCT    = [[] for i in range( Peg_Count ) ]
  TOWER_STRUCT[0] = list(range(1, Stack_Size+1))[::-1]


def Move_Block( from_peg, to_peg ):
  # Manipulates TOWER_STRUCT as well, do not need to set.
  global MOVE_COUNTER

  #Sanity check: Make sure that the block to move is moving onto a peg with a larger block below it.
  This_Block = TOWER_STRUCT[from_peg][-1]
  if TOWER_STRUCT[to_peg] != []:
    Target_Block = TOWER_STRUCT[to_peg][-1]
    if This_Block > Target_Block:
      print("Exception! Tower status pre-exception:")
      Print_Tower( True ) # Overrride debugging.
      _errstr = "Moving block {:d} from peg {:d} to peg {:d} puts it on top of block {:d}".format( This_Block, from_peg, to_peg, Target_Block )
      raise ValueError( _errstr )

  TOWER_STRUCT[ to_peg  ].append( This_Block )
  TOWER_STRUCT[ from_peg].pop() # Remove last (smallest) element "This_Block"
  MOVE_COUNTER += 1
  
  # And if requested, print the tower status.
  Print_Tower()
  

def Print_Tower( override_debug = False ):
  if DEBUG_PRINT or override_debug:
    for Peg in TOWER_STRUCT:
      print( Peg )
    print()


def Cache( New_Start, New_End, All_Pegs ):
  New_Cache = [ Peg for Peg in All_Pegs if Peg not in [ New_Start, New_End ] ]
  return New_Cache

def Arb_TOH( Source_Peg, Target_Peg, Num_Blocks_To_Move ):
  # Determine the 'cache' pegs, the ones not included in the source/targets.
  # These are used to cache the larger blocks to reduce total movement.
  Cache_Pegs = [ Peg_ID for Peg_ID in range(len( TOWER_STRUCT )) if Peg_ID not in [Source_Peg, Target_Peg]]
  
  # To limit edge case: If cache larger than needed, reduce size of Cache array.
  # Simplifies following movement.
  if Num_Blocks_To_Move <= len(Cache_Pegs): 
    Cache_Pegs = Cache_Pegs[:Num_Blocks_To_Move-1]

  # IFF everything fits in the cache: (Minus the largest block)
  if Num_Blocks_To_Move-1 == len(Cache_Pegs):
    # Move everything into the cahce pegs
    for Peg in Cache_Pegs:
      Move_Block( Source_Peg, Peg )
    # Move the largest peg to the target
    Move_Block( Source_Peg, Target_Peg )
    # And then move everything off of the cache
    for Peg in Cache_Pegs[::-1]:
      Move_Block( Peg, Target_Peg )
    # And return, as everything is now on the target peg.
    return

  # If got here, then won't all fit in the cache.
  # TOW enough of the top of the Source Peg somewhere into the cache 
  #  as to allow the larger blocks to be distrubuted amonst the cache,
  #  to allow for the largest block to be moved onto the Target peg
  # Then empty the cache, and move the recursed tower onto the target peg.
 
  All_Pegs = list(range(len( TOWER_STRUCT ))) # Get list of all peg IDs
  # Get the minimum size of the substack required to distribute the remainder amongst the cache
  Substack_Size   = Num_Blocks_To_Move - len(Cache_Pegs)
  Substack_Target = Cache_Pegs[0] # Just move onto the first Cache block.

  Arb_TOH( Source_Peg, Substack_Target, Substack_Size )
  
  for Peg in Cache_Pegs[1:]: # Then move the remainder from the Source into the cache,
    Move_Block( Source_Peg, Peg )
  Move_Block( Source_Peg, Target_Peg ) # Move the largest block
  for Peg in Cache_Pegs[1:][::-1]: # Move the remainder of the cache into the Target Peg.
    Move_Block( Peg, Target_Peg )

  # And then move the substack tower onto the target stack.
  Arb_TOH( Substack_Target, Target_Peg, Substack_Size)



def main( Num_Pegs = 3, Num_Blocks = 5, Debug = False ):
  global DEBUG_PRINT
  DEBUG_PRINT = Debug
  
  # Should get the setup, source, & target pegs set as arbitrary.
  # For now just push them from the first tower to the last tower.
  Source_Tower = 0
  Target_Tower = Num_Pegs - 1
  
  print("Starting Setup:")
  Setup_Tower( Num_Pegs, Num_Blocks )
  Print_Tower( True )  
  
  Arb_TOH ( Source_Tower, Target_Tower, Num_Blocks )
  
  print("End Result:")
  Print_Tower( True )
  
  print("Total Moves:", MOVE_COUNTER)
  return MOVE_COUNTER
	


if __name__ == '__main__':
  _parser = argparse.ArgumentParser(description='Tower Of Hanoi, using arbitrary pegs')
  _parser.add_argument('Peg_Count',   type=int, help='Number of pegs in the tower.')
  _parser.add_argument('Block_Count', type=int, help='Number of blocks on the source peg.')
  _parser.add_argument('--debug', '--verbose',  help='Prints each move in the game.', action='store_true' )
  _args = _parser.parse_args()
  
  num_pegs   = _args.Peg_Count
  num_blocks = _args.Block_Count
  bool_debug = _args.debug
  
  main( num_pegs, num_blocks, bool_debug )

  
