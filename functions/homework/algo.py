#do crud functions in other file i'll write the actual algo
import functools
def organizationthing(a, b):
    if (2 * a[0] + a[1] + a[2] >= 2 * b[0] + b[1] + b[2]):
        return -1
    else:
        return 1

def returnorder(a):
    #a should be the weights as follows:
    #each sublist contains numbers, 1, 2, or 3 that say the magnitude, the first is priority
    #the second is how hard the work is and the third is the time
    r = sorted(a, key=functools.cmp_to_key(organizationthing))
    return r
