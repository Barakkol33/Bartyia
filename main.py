
"""
Questions:
Give Definitions
yes/no questions
If someone guesses - give a new one


Draw:
Split into groups
I send subjects

Pick group that
Pick volunteer
Someone picks a subject and sends to volunteer
Volunteer has 90 seconds
"""

import random
import os

USERS_DETAILS = [["name", "phone"]]

PHONE_NUMBER_LENGTH = 9
CURRENT_DEFINITIONS_FILENAME = "current_definitions.txt"
ALL_DEFINITIONS_FILENAME = "definitions.txt"


class User(object):
    def __init__(self, name, phone_number, definition=None):
        self.name = name
        assert(len(phone_number))
        self.phone_number = phone_number
        self.definition = definition

    def get_whatsapp_link(self, message):
        message = message.replace(" ", "%20").replace("\n", "%0A")
        return "https://wa.me/{0}?text={1}".format("972" + self.phone_number, message)


class Game:
    def __init__(self):
        self._users = self._create_users()
        self.definitions = self._get_definitions()

    def _get_definitions(self):
        if os.path.exists(CURRENT_DEFINITIONS_FILENAME):
            definitions_filename = CURRENT_DEFINITIONS_FILENAME
        else:
            definitions_filename = ALL_DEFINITIONS_FILENAME

        definitions = open(definitions_filename).read().split("\n")

        return definitions

    def _create_users(self):
        return [User(*details) for details in USERS_DETAILS]

    def _pick_definition(self):
        if not self.definitions:
            raise RuntimeError("No more definitions!")

        index = random.randint(0, len(self.definitions) - 1)

        definition = self.definitions[index]

        del self.definitions[index]

        return definition

    def start_round(self):
        header = ["Definitions:"]

        # Create Configuration
        configuration = ["{0} - {1}".format(user.name, self._pick_definition()) for user in self._users]
        links = []

        for index, user in enumerate(self._users):
            # Filter user definition
            user_configuration = list(configuration)
            del user_configuration[index]
            user_configuration = "\n".join(header + user_configuration)

            # Get user link.
            link = user.get_whatsapp_link(user_configuration)
            links.append(link)

        print("\n\n".join(links))

    def __del__(self):
        open(CURRENT_DEFINITIONS_FILENAME, "w").write("\n".join(self.definitions))


def random_groups():
    users = [name[0] for name in USERS_DETAILS]
    groups_amount = 3
    users_per_group = [3, 3, 4]
    groups = []
    for index in range(groups_amount):
        group = []
        for members_amount in range(users_per_group[index]):
            i = random.randint(0, len(users) - 1)
            user = users[i]
            del users[i]
            group.append(user)
        groups.append(group)

    for index, group in enumerate(groups):
        print("Group {0}: {1}".format(index + 1, ", ".join(group)))


def main():
    Game().start_round()
    #random_groups()

main()
