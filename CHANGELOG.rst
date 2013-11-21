========
Versions
========

* Version 2.2: ipa_to_unt/asjp and unt_to_ipa now transparently take 1+ strings
* Version 2.1: Made transliteration functions their own module; the switch
  for non-glottal engmas is temporarily removed because of this.
  Will put it back in if necessary.
* Version 2.0: Mappings are now specified using regular expressions, which is
  100% more awesome. There's one small cost: reversing a conversion
  is a bit more complicated. Since I can't just say "swap value for
  key" anymore, you need to set up a second set of mappings that
  perform the reverse.

  However, this does simplify the "API" a bit: instead of
  having forward/backwards versions of every conversion function,
  now it's just a question of which mappings to apply and their
  order.

  Help with Unicode regex is from http://stackoverflow.com/a/393915
* Version 1.9: convert_word and convert now have keyword arguments for whether
               to use the asjp mapping.
* Version 1.8: Added an option for whether engma [ŋ] or [ŋʔ] should be used in 
               conversion. Mainly useful when comparing between Dr. Beck's data
               and the comparative data.
* Version 1.7: Four new functions for other Python scripts to use as needed.
               convert_all and reverse_convert_all operate on lists of words.
               convert_word and reverse_convert_word operate on a single word.
* Version 1.6: A translation matrix for some typos, and an asjp option
               which turns [ʍ] into "ux" after performing the other operations
* Version 1.5: Fixed a bug from v1.2 with reverse conversion, and "nh"
               is now translated to [ŋʔ]
* Version 1.4: "tz" now translated to [c]
* Version 1.3: Completed documentation
* Version 1.2: Now acts like real command line software
* Version 1.1: Performs reverse conversion, too
* Version 1.0: Works!