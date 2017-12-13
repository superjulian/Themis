import sys

def main(): 
    was_black = False
    for item in sys.argv:
        if item == 'Black': 
            was_black = True
    
    if was_black: 
        print "0"
    else: 
        print "1"
main()
