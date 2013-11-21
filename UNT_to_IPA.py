with open('readme.rst') as readme:
    __doc__ = readme.read()

__author__ = "Matthew Darling"
__email__ = "matthewjdarling@gmail.com"
__version__ = "2.2"
__date__ = "November 20th, 2013"
__doc__ += "\n\nAUTHOR\n\n" + __author__ + ' <' + __email__ + '>' \
           + "\n\nVERSION\n\n" + __version__

#Since UNT_to_IPA is a package, I don't need this stuff here;
#But it's nice to have for the sake of command line usage.
#Plus, I can import my version number from here, which I like.

import codecs, argparse, sys, os
#These four modules are essential, so they can go on one line

import basic_argparse
import re_transliterate as translit

##### UNT -> IPA/ASJP conversion #####
def init_forward_mappings():
    """Creates global regex mappings for use in UNT->IPA transliteration."""
    global re_trigraphs, re_bigraphs, re_monographs, re_special, re_asjp
    re_trigraphs = {u"lh’":u"ɬ’", #ejective lateral fricative
                    VOWELS + u"(:'|':)":ur"\g<1>" + LARYNGEAL + u"ː"}
                    #long laryngealized vowels
    re_bigraphs = {u"ch":u"č", u"lh":u"ɬ", u"nh":u"ŋʔ",
                   u"tz":u"c", u"uj":u"ʍ", #digraph consonants
                   u"s’":u"s’", u"x’":u"š’", #ejectives
                   VOWELS + u":":ur"\g<1>ː",
                   VOWELS + u"'":ur"\g<1>" + LARYNGEAL}
                   #long/laryngealized vowels
    re_monographs = {u"h":u"ʔ", u"r":u"ɾ", u"x":u"š"}
    re_special = {u"j":u"x"}
    re_asjp = {u"ʍ":u"ux"}

def unt_to_ipa(to_convert):
    """Applies mappings in order to turn UNT wordform(s) into IPA."""
    order = [re_trigraphs, re_bigraphs, re_monographs, re_special]
    if hasattr(to_convert, 'pop'): #is a list/set
        return translit.transliterate_all(order, to_convert)
    else: return translit.transliterate(order, to_convert)

def unt_to_asjp(to_convert):
    """Applies mappings in order to turn UNT wordform(s) into ASJP format."""
    order = [re_trigraphs, re_bigraphs, re_monographs, re_special, re_asjp]
    if hasattr(to_convert, 'pop'): #is a list/set
        return translit.transliterate_all(order, to_convert)
    else: return translit.transliterate(order, to_convert)

##### IPA -> UNT conversion #####
def init_reverse_mappings():
    """Creates global regex mappings for use in IPA->UNT transliteration."""
    global rev_trigraphs, rev_bigraphs, rev_monographs, rev_special, rev_asjp
    rev_trigraphs = {u"ɬ’":u"lh’", #ejective lateral fricative
                    VOWELS + LARYNGEAL + u"ː":ur"\g<1>:'"}
                    #long laryngealized vowels
    rev_special = {u"x":u"j"}
    rev_bigraphs = {u"č":u"ch", u"ɬ":u"lh", u"ŋʔ":u"nh",
                    u"c":u"tz", u"ʍ":u"uj", #digraph consonants
                    u"s’":u"s’", u"š’":u"x’", #ejectives
                    VOWELS + u"ː":ur"\g<1>:", VOWELS + LARYNGEAL:ur"\g<1>'"}
                    #long/laryngealized vowels
    rev_monographs = {u"ʔ":u"h", u"ɾ":u"r", u"š":u"x", u"ŋ":u"nh"}
                      #If engma_glottal was turned off, look for non-glottal ones

def ipa_to_unt(to_convert):
    """Applies mappings in order to turn UNT word(s) in IPA into orthography.

    May have subtle bugs due to consonant clusters - check for occurences
    of [ts] and some others."""
    order = [rev_trigraphs, rev_special, rev_bigraphs, rev_monographs]
    if hasattr(to_convert, 'pop'): #is a list/set
        return translit.transliterate_all(order, to_convert)
    else: return translit.transliterate(order, to_convert)

##### File operations #####
def convert_file(in_file, stdout=False, out_file ="./temp.txt", use_asjp=False):
    """Reads UNT words from in_file, outputs to stdout/outfile as IPA/ASJP."""
    words = read_in(in_file)
    init_regex_defs()
    init_forward_mappings()
    
    if use_asjp: words = unt_to_asjp(words)
    else: words = unt_to_ipa(words)

    print_out(words, stdout, out_file)

def reverse_convert_file(in_file, stdout=False, out_file="./temp.txt"):
    """Reads IPA words from in_file, outputs them in orthography."""
    words = read_in(in_file)
    init_regex_defs()
    init_reverse_mappings()
    
    words = ipa_to_unt(words)

    print_out(words, stdout, out_file)

##### Startup tasks #####
def init_regex_defs():
    """Creates some global regex patterns required by other functions."""
    global LARYNGEAL, VOWELS
    LARYNGEAL = ur"\u0330"
    VOWELS = u"([aeiouáéíóú])" #vowels with accents are stressed

def check_requirements(args):
    """Confirms the requirements for running this program are met.

    Right now, this just means that the input file exists. Might be
    worth checking the PYTHONIOENCODING variable, if args.stdout is set."""
    if not os.path.exists(args.input):
        print("Error: Input file does not exist")
        exit(1)

def configure_argparse(parser):
    """Performs program-specific modifications to the argument parser."""
    parser.description = ("Convert a file from Upper Necaxa Totonac "
                         "orthography to IPA, or make the reverse conversion.")
    parser.epilog = ("Note that consonant clusters may cause errors in the "
                    "IPA->orthography conversion. If you use stdout, you "
                    "will want to set the PYTHONIOENCODING environment "
                    "variable to 'utf-8'.")
    parser.add_argument("-r", "--reverse", action="store_true", 
                        help="Pass this argument to convert from IPA to UNT "
                        "orthography.", default=False)
    parser.add_argument("-a", "--asjp", action="store_true",
                        help="Pass this argument to make an IPA variant "
                        "suitable for uni2asjp.pl.", default=False)
    
    parser.add_argument("-i", "--input", default="./input.txt", 
                        help="The file to be converted.")
    output_options = parser.add_mutually_exclusive_group(required=True)
    output_options.add_argument("-o", "--output",
                                help="The file to save the program's output. "
                                "The -std option is an alternative that prints "
                                "to stdout instead.")
    output_options.add_argument("-std", "--stdout", action="store_true",
                                help="If this argument is given, the program "
                                "will use stdout instead of a file.", 
                                default=False)
    return parser

##### I/O #####
def read_in(filename="./UNT.txt"):
    """Opens a utf-8 encoded file and returns a list of its lines."""
    with codecs.open(filename, encoding="utf-8") as temp:
        return temp.readlines()

def print_out(output_list, stdout=False, filename="./temp.txt"):
    """Prints a list of strings to stdout or a file."""
    if stdout:
        print(''.join(output_list))
        return
    with codecs.open(filename, 'w', "utf-8") as temp:
        temp.writelines(output_list)

##### Putting it all together #####
def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = basic_argparse.init_parser("UNT_to_IPA.py", __version__, 
                                        __date__, __doc__)
    parser = configure_argparse(parser)
    args, unknown = parser.parse_known_args(argv)

    check_requirements(args)

    if args.reverse: reverse_convert_file(args.input, args.stdout, args.output)
    else: convert_file(args.input, args.stdout, args.output, args.asjp)

if __name__ == "__main__":
    main()