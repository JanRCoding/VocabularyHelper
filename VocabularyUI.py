from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.properties import ListProperty, StringProperty, DictProperty, ObjectProperty, BooleanProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

import random
from collections import namedtuple
import VocabularyCore as vc


class MenuScreen(Screen):
    text = StringProperty("")
    languages = vc.startup_update()


class SelectionScreen(Screen):

    Direction = namedtuple("Direction", ["origin", "target"])
    direction = ObjectProperty()
    label_text = StringProperty()
    my_lectures = DictProperty()
    session = ObjectProperty()

    lecture_rv = ObjectProperty()

    def enter_selection(self):
        """
        Create selectable recycleview labels from folder specified in languagespinner on menuscreen.
        """
        self.lecture_rv.data = [{"text": x.name[:-4], "path": x}
                                for x in self.my_lectures[self.label_text]]

    def create_session(self):
        selection = [
            x.path for x in self.lecture_rv.selectbox.children if x.selected == True]
        self.session = vc.Session(self.label_text, selection)


class SessionScreen(Screen):
    session = ObjectProperty()
    direction = ObjectProperty()
    my_list = ListProperty()
    question = StringProperty()
    answer = StringProperty()

    sessionbox = ObjectProperty()

    def enter_session(self):
        pass

    def _evaluate(self):
        my_answer = self.sessionbox.answer_text.text
        if my_answer == self.answer:
            self.sessionbox.answer_text.hint_text = f"Correct!\n{self.question} - {self.answer}\nYour answer: {my_answer}"
        else:
            self.sessionbox.answer_text.hint_text = f"Incorrect. You'll get it next time.\n{self.question} - {self.answer}\nYour answer: {my_answer}"

    def _pop_question(self):
        current = self.my_list.pop()
        self.question, self.answer = current[self.direction.origin], current[self.direction.target]

    def next_word(self):
        self._evaluate()
        if len(self.my_list) != 0:
            self._pop_question()
        else:
            self.question = "All done!"

    def get_started(self):
        keys_list = list(self.session.session_dict.items())
        random.shuffle(keys_list)
        self.my_list = keys_list
        self._pop_question()

    def rerun(self):
        self.get_started()


class SessionBoxLayout(BoxLayout):

    answer_text = ObjectProperty()


class SessionTextInput(TextInput):
    """Subclassed to handle more extensive logic in the future."""
    pass


class LanguageSpinner(Spinner):
    """Handles folderselection dfor selection_screen."""

    def __init__(self, **kwargs):
        super(LanguageSpinner, self).__init__(**kwargs)
        self.text = "Languages"
        self.size_hint = (None, None)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """Adds selection and focus behaviour to the view."""


class SelectableLabel(RecycleDataViewBehavior, Label):
    """Add selection support to the Label."""
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    path = None

    def refresh_view_attrs(self, rv, index, data):
        """Catch and handle the view changes."""
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        """Add selection on touch down."""
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """Respond to the selection of items in the view."""
        self.selected = is_selected


class RV(RecycleView):
    selectbox = ObjectProperty()

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)


class VocabularyApp(App):
    pass


if __name__ == '__main__':
    VocabularyApp().run()
