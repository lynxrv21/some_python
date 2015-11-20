# http://psung.blogspot.com/2007/12/for-else-in-python.html
# Here's some code written without for...else:

def contains_even_number(l):
    """Prints whether or not the list l contains an even number."""
    has_even_number = False
    for elt in l:
        if elt % 2 == 0:
            has_even_number = True
            break
    if has_even_number:
        print "list contains an even number"
    else:
        print "list does not contain an even number"

# The equivalent code snippet below illustrates how the use of for...else
# lets you remove an extraneous flag variable from that loop:

def contains_even_number(l):
    """Prints whether or not the list l contains an even number."""
    for elt in l:
        if elt % 2 == 0:
            print "list contains an even number"
            break
    else:
        print "list does not contain an even number"
