import random
import json
import csv
import sys
import pandas as pd
from pathlib import Path


def startup_update():
    """
    Go through each Folder in Lectures. Parse to dict with Folder as Key and .txt Files in directory as value(list). Used to iteratively create interfaceoptions on startup/update.
    """
    all_lectures = {}
    p = Path.cwd() / "Lectures"
    for e in list(p.glob("*")):
        if e.is_dir():
            all_lectures[e.stem] = list(
                (p / "Lectures" / str(e)).glob("*.txt"))
    return all_lectures


class Session():
    """
    Main class created from subset of lectures. Handles creation of session dictionary and tracks scores.
    """

    def __init__(self, language, lectures, scored=False):
        self.path = Path.cwd() / "Lectures" / language
        self.lectures = lectures
        self.session_dict = self._create_session()
        self.session_scores = {}
        for word in self.session_dict:
            self.session_scores[word] = [0, 0]
        self.alltime_scores = {}
        self.scored = scored
        if self.scored:
            with open(self.path / "score_dict.json", "r", encoding="utf-8") as json_file:
                self.alltime_scores = json.load(json_file)

    def _create_session(self):
        """
        Called upon initialization, creates dictinary native language as key and foreign language as value from passed in lecture list.
        """
        temp_session = []
        for file in self.lectures:
            with open(file, "r", encoding="utf-8") as file:
                session_part = []
                for line in file:
                    for word in (line.strip("\"\n")).split(","):
                        session_part.append(word)
                temp_session.extend(session_part)
        session_dictionary = dict(zip(temp_session[::2], temp_session[1::2]))
        return session_dictionary

    def _update_scores(self):
        """
        Placeholder for more elaborate scoring system. Not implemented in gui yet.
        """
        for word in self.session_scores:
            for i, e in enumerate(self.session_scores.get(word)):
                self.alltime_scores[word][i] += e
        for word in self.scores:
            with open(self.path / "score_dict - Copy.json", "w", encoding="utf-8") as update_file:
                json.dump(self.scores, update_file, indent=2)

    """
    Original non-gui test version.
    """
    # def french_to_english(self):
    #     """Go through each element of the dictionary once."""
    #     print(self.lesson_dict)
    #     for e in self.lesson_dict:
    #         if input("{} ".format(e)) == self.lesson_dict[e]:
    #             print("Good boy! Have a frogleg!")
    #             self.session_scores[e][1] += 1
    #         else:
    #             print("Wrong!")
    #             self.session_scores[e][0] += 1
    #     if self.scored == True:
    #         self._update_scores()

    # def english_to_french(self):
    #     """Go through each element of the dictionary once."""
    #     for e in self.lesson_dict:
    #         if input("{} ".format(self.lesson_dict[e])) == e:
    #             print("Good boy! Have a snail!")
    #             self.session_scores[e][1] += 1
    #         else:
    #             print("Wrong! It's {}".format(e))
    #             self.session_scores[e][0] += 1
    #     if self.scored == True:
    #         self._update_scores()

    # def mixed_session(self):
    #     for e in lesson_dict:
    #         if random.randint(1, 2) == 1:
    #             if input("{} ".format(self.lesson_dict[e])) == e:
    #                 print("Well done!")
    #                 self.session_scores[e][1] += 1
    #             else:
    #                 print("Wrong. It's {}".format(e))
    #                 self.session_scores[e][0] += 1
    #         else:
    #             if input("{} ".format(e)) == self.lesson_dict[e]:
    #                 print("Well done!")
    #                 self.session_scores[e][1] += 1
    #             else:
    #                 print("Wrong.")
    #                 self.session_scores[e][0] += 1
    #     if self.scored == True:
    #         self._update_scores()


class LessonUpdate():
    """
    Updates a specific lecture. If no lecture is passed in the user is prompted to create a new lecture. Dataframe is created from passed lecture or newly created empty lecture.
    """

    def __init__(self, lesson=None):
        self.lesson = lesson
        if self.lesson == None:
            title = input("Enter the Title for your new lesson: ")
            # check namespace collision, allow access to specific folder
            main_path = Path.cwd()
            p = main_path / "Lectures"
            self.lesson = "{}/{}.csv".format(p, title)

        with open(self.lesson, "r", encoding="utf-8") as main:
            gen_dict = csv.DictReader(main, delimiter="-")
            frame_list = []
            headers = gen_dict.fieldnames
            for row in gen_dict:
                frame_list.append(dict(row))
        self.df = pd.DataFrame(frame_list, columns=headers)

    def _add_word(self):
        """Adds word from userinput directly to file."""
        word = input("New word:")
        translation = input("Means:")
        with open(self.lesson, "w", encoding="utf-8") as lesson:
            lesson.write("{},{}\n".format(word, translation))
        if input("Add another word: y/n?") == y:
            self._add_word()

    def delete_word(self, position):
        """Deletes word from dataframe. Changes must be saved separately."""
        self.df.drop(index=position, inplace=True)

    def update_csv(self):
        self.df.to_csv(self.lesson, index=False)


if __name__ == "__main__":
    all_lectures = startup_update()
    print(all_lectures)
    #test = Lecture("French", ["C:/Users/Jan/Desktop/Coding/Vocabulary_Helper/Lectures/French/French_Lecture_1.txt"], False)
