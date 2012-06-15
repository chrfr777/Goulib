#functional toolset from http://pyeuler.wikidot.com/toolset
#tools from http://docs.python.org/dev/py3k/library/itertools.html

#!/usr/bin/python
from itertools import *

def any(seq, pred=bool):
    "Return True if pred(x) is True for at least one element in the iterable"
    return (True in imap(pred, seq))

def all(seq, pred=bool):
    "Return True if pred(x) is True for all elements in the iterable"
    return (False not in imap(pred, seq))

def no(seq, pred=bool):
    "Returns True if pred(x) is False for every element in the iterable"
    return (True not in imap(pred, seq))

def take(n, iterable):
    """Take first n elements from iterable"""
    return islice(iterable, n)

def takenth(n, iterable):
    "Returns the nth item"
    return islice(iterable, n, n+1).next()

def first(iterable):
    """Take first element in the iterable"""
    return iterable.next()

def last(iterable):
    """Take last element in the iterable"""
    return reduce(lambda _, y: y, iterable)

def takeevery(n, iterable):
    """Take an element from iterator every n elements"""
    return islice(iterable, 0, None, n)

def drop(n, iterable):
    """Drop n elements from iterable and return the rest"""
    return islice(iterable, n, None)

def icross(*sequences):
    """Cartesian product of sequences (recursive version)"""
    if sequences:
        for x in sequences[0]:
            for y in icross(*sequences[1:]):
                yield (x,)+y
    else: yield ()

def get_groups(iterable, n, step):
    """Make groups of 'n' elements from the iterable advancing
    'step' elements each iteration"""
    itlist = tee(iterable, n)
    onestepit = izip(*(starmap(drop, enumerate(itlist))))
    return takeevery(step, onestepit)

def flatten(lstlsts):
    """Flatten a list of lists"""
    return list(chain(*lstlsts))

def ireduce(func, iterable, init=None):
    """Like reduce() but using iterators (also known also scanl). Non-functional version"""
    if init is None:
        iterable = iter(iterable)
        curr = iterable.next()
    else:
        curr = init
        yield init
    for x in iterable:
        curr = func(curr, x)
        yield curr

def quantify(iterable, pred=bool):
    "Count how many times the predicate is true"
    return sum(imap(pred, iterable))

def unique(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in iterable:
            if element not in seen:
                seen_add(element)
                yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element
                
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def next_permutation(seq, pred=cmp):
    """Like C++ std::next_permutation() but implemented as
    generator. Yields copies of seq.
    see http://blog.bjrn.se/2008/04/lexicographic-permutations-using.html"""

    def reverse(seq, start, end):
        # seq = seq[:start] + reversed(seq[start:end]) + \
        #       seq[end:]
        end -= 1
        if end <= start:
            return
        while True:
            seq[start], seq[end] = seq[end], seq[start]
            if start == end or start+1 == end:
                return
            start += 1
            end -= 1

    if not seq:
        raise StopIteration

    try:
        seq[0]
    except TypeError:
        raise TypeError("seq must allow random access.")

    first = 0
    last = len(seq)
    seq = seq[:]

    # Yield input sequence as the STL version is often
    # used inside do {} while.
    yield seq

    if last == 1:
        raise StopIteration

    while True:
        next = last - 1

        while True:
            # Step 1.
            next1 = next
            next -= 1

            if pred(seq[next], seq[next1]) < 0:
                # Step 2.
                mid = last - 1
                while not (pred(seq[next], seq[mid]) < 0):
                    mid -= 1
                seq[next], seq[mid] = seq[mid], seq[next]

                # Step 3.
                reverse(seq, next1, last)

                # Change to yield references to get rid of
                # (at worst) |seq|! copy operations.
                yield seq[:]
                break
            if next == first:
                raise StopIteration
    raise StopIteration

class iter2(object):
    '''Takes in an object that is iterable.  
    http://code.activestate.com/recipes/578092-flattening-an-arbitrarily-deep-list-or-any-iterato/
    Allows for the following method calls (that should be built into iterators anyway...)
    calls:
        - append - appends another iterable onto the iterator.
        - insert - only accepts inserting at the 0 place, inserts an iterable
         before other iterables.
        - adding.  an iter2 object can be added to another object that is
         iterable.  i.e. iter2 + iter (not iter + iter2).  It's best to make
         all objects iter2 objects to avoid syntax errors.  :D
    '''
    def __init__(self, iterable):
        self._iter = iter(iterable)
    
    def append(self, iterable):
        self._iter = chain(self._iter, iter(iterable))
        
    def insert(self, place, iterable):
        if place != 0:
            raise ValueError('Can only insert at index of 0')
        self._iter = chain(iter(iterable), self._iter)
    
    def __add__(self, iterable):
        return chain(self._iter, iter(iterable))
        
    def next(self):
        return self._iter.next()
    
    def __iter__(self):
        return self

def iflatten(iterable):
    '''flatten a list of any depth'''
    iterable = iter2(iterable)
    for e in iterable:
        if hasattr(e, '__iter__'):
            iterable.insert(0, e)
        else:
            yield e