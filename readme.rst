A module for myself and other people working with Upper Necaxa Totonac data.

The default behaviour is UNT orthography -> IPA. The -r argument performs 
IPA -> UNT. In the latter case, beware bugs caused by consonant clusters
such as [ts].

Supports printing to stdout for piping to some other program (eg uni2asjp.pl).

Bad things may happen if your input file isn't encoded in UTF-8 
(you'll probably just get a ValueError exception).

Can be imported to other files for on-the-fly conversion. Before converting,
however, you must run the init_regex_defs() function and either
init_forward_mappings()/init_reverse_mappings() for UNT->IPA or IPA->UNT
conversions (respectively). You can then use unt_to_ipa(), unt_to_asjp(),
and ipa_to_unt() as needed.

The conversion functions can operate on either single strings, a list of
strings, or a set of strings.