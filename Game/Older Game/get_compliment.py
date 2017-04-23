def get_complement(nucleotide):
    """ Returns the complementary nucleotide
        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """
    # TODO: implement this
    if nucleotide == "C":
        return("G")
    if nucleotide == "G":
        return("C")
    if nucleotide == "A":
        return("T")
    if nucleotide == "T":
        return ("A")

get_complement("A")
