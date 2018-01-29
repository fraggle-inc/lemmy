# coding: utf8
"""Functions for lemmatizing using a set of lemmatization rules."""
from collections import defaultdict
import logging
import time


class SimpleLemmatizer(object):
    """Class for lemmatizing Danish words. Inspired by the spaCy lemmatizer."""

    def __init__(self, exceptions=None):
        """Initialize a lemmatizer using specified set of exceptions."""
        self.exceptions = exceptions
        self.rules = {
            "adj": [
                ["mle", "mmel"],
                ["elt", "el"],
                ["mme", "m"],
                ["øst", "øs"],
                ["ede", "et"],
                ["ngt", "ng"],
                ["dt", "d"],
                ["lle", "l"],
                ["igt", "ig"],
                ["tte", "t"],
                ["ist", "is"],
                ["ivt", "iv"],
                ["rit", "ri"],
                ["vne", "ven"],
                ["alt", "al"],
                ["nne", "n"],
                ["rt", "r"],
                ["kne", "ken"],
                ["ent", "en"],
                ["øjt", "øj"],
                ["ønt", "øn"],
                ["sne", "ssen"],
                ["ilt", "il"],
                ["rkt", "rk"],
                ["blåt", "blå"],
                ["gne", "gen"],
                ["ldne", "lden"],
                ["adne", "aden"],
                ["dne", "dden"],
                ["ble", "bel"],
                ["bne", "ben"],
                ["tne", "ten"],
                ["ppe", "p"],
                ["lt", "l"],
                ["somt", "som"],
                ["e", ""]],
            "adv": [],
            "verb": [["ede", "e"], ["re", "re"], ["te", "e"], ["er", "e"], ["dt", "de"], ["st", "se"], ["t", ""]],
            "noun": [
                ["numre", "nummer"],
                ["derne", "de"],
                ["ttet", "t"],
                ["alen", "ale"],
                ["ejde", "ejde"],
                ["ale", "ale"],
                ["strene", "ster"],
                ["dlet", "ddel"],
                ["lykker", "lykke"],
                ["møde", "møde"],
                ["rykket", "ryk"],
                ["stret", "ster"],
                ["sret", "sret"],
                ["nner", "n"],
                ["nnerne", "n"],
                ["asken", "aske"],
                ["aske", "aske"],
                ["ttene", "t"],
                ["iker", "iker"],
                ["kerne", "ker"],
                ["tter", "t"],
                ["lser", "lse"],
                ["llerne", "lle"],
                ["llene", "l"],
                ["lgerne", "lger"],
                ["unger", "unge"],
                ["mænd", "mand"],
                ["erne", ""],
                ["ene", ""],
                ["et", ""],
                ["en", ""],
                ["er", ""],
                ["e", ""]]
        }

    def fit(self, X, y):
        """Train a lemmatizer on specified training data."""
        self.exceptions = defaultdict(lambda: defaultdict(lambda: []))
        train_start = time.time()
        for word_class in self.rules:
            logging.debug("building exceptions for word class '%s'", word_class)
            self.exceptions[word_class] = self._build_exceptions(word_class, X, y)
        exception_count = sum(len(excs) for d in self.exceptions.values() for excs in d.values())
        logging.debug("training complete: %s rules in %.2fs", exception_count, time.time() - train_start)

    def lemmatize(self, word_class, full_form):
        """Return lemma for specified full form word of specified word class."""
        if full_form in self.exceptions[word_class]:
            return self.exceptions[word_class][full_form]
        return self._apply_rules(word_class, full_form)

    def _build_exceptions(self, word_class, X, y):
        temp_exceptions = defaultdict(set)
        for (word_class_, full_form), lemma in zip(X, y):
            if word_class_ != word_class:
                continue
            predicted = self._apply_rules(word_class, full_form)
            if predicted == [lemma]:
                continue
            temp_exceptions[full_form].add(lemma)
        return dict((word_class, list(temp_set)) for word_class, temp_set in temp_exceptions.items())

    def _apply_rules(self, word_class, full_form):
        for full_form_suffix, lemma_suffix in self.rules[word_class]:
            if full_form.endswith(full_form_suffix):
                form = full_form[:-len(full_form_suffix)] + lemma_suffix
                return [form]
        return [full_form]