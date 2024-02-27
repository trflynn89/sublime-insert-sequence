import itertools
import string

import sublime
import sublime_plugin


def next_number(first_selection):
    """
    Starting from the first selection, yield a sequence of numbers converted to strings.
    """
    for number in itertools.count(first_selection):
        yield str(number)


def next_letter(first_selection, letters):
    """
    Starting from the first selection, yield a sequence of alphabetic characters.

    If the first selection is 'a', this will yield ('a', 'b', 'c', ..., 'z', 'aa', 'ab', 'ac', ...)
    and so on.

    If the first selection is 'f', this will yield ('f', 'g', 'h', ..., 'z', 'aa', 'ab', 'ac', ...)
    and so on.
    """
    for size in itertools.count(1):
        next_letters = letters[letters.find(first_selection):]
        first_selection = letters[0]

        for s in itertools.product(next_letters, repeat=size):
            yield ''.join(s)


class InsertSequenceCommand(sublime_plugin.TextCommand):
    """
    Command to insert a sequence of numbers or letters into the viewports active selection.
    """

    def run(self, edit):
        generator = self._create_sequence()

        for (selection, sequence) in zip(self.view.sel(), generator):
            self.view.insert(edit, selection.begin(), sequence)

        for selection in self.view.sel():
            self.view.erase(edit, selection)

    def _create_sequence(self):
        """
        Parse the first selection in the viewport and determine what sequence will be inserted.
        """
        selections = self.view.sel()
        assert len(selections) > 0

        first_selection = self.view.substr(selections[0]).strip()

        if first_selection.isdigit():
            return next_number(int(first_selection))

        if len(first_selection) == 1 and first_selection.isalpha():
            if first_selection.islower():
                return next_letter(first_selection, string.ascii_lowercase)

            return next_letter(first_selection, string.ascii_uppercase)

        return next_number(1)
