import unittest
from unittest import mock

import urwid

from subiquitycore.testing import view_helpers

from subiquity.controllers.welcome import WelcomeController
from subiquity.models.locale import LocaleModel
from subiquity.ui.views.welcome import WelcomeView


class WelcomeViewTests(unittest.TestCase):

    def make_view_with_languages(self, languages):
        controller = mock.create_autospec(spec=WelcomeController)
        model = mock.create_autospec(spec=LocaleModel)
        model.get_languages.return_value = languages
        return WelcomeView(model, controller)

    def test_basic(self):
        # Clicking the button for a language calls "switch_language"
        # on the model and "done" on the controller.
        view = self.make_view_with_languages([('code', 'native')])
        but = view_helpers.find_button_matching(view, "^native$")
        view_helpers.click(but)
        view.model.switch_language.assert_called_once_with("code")
        view.controller.done.assert_called_once_with()

    def test_initial_focus(self):
        # The initial focus for the view is the button for the first
        # language.
        view = self.make_view_with_languages([
            ('code1', 'native1'),
            ('code2', 'native2'),
            ])
        for w in reversed(view_helpers.get_focus_path(view)):
            if isinstance(w, urwid.Button):
                self.assertEqual(w.label, "native1")
                break
        else:
            self.fail("No button found in focus path")
