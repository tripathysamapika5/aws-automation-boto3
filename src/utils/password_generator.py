import string
import random


class RandomPasswordGenerator:
    min_length_of_password = 8
    max_length_of_password = 15

    @staticmethod
    def generate_random_password():
        password_characters = []

        #generate random password length
        password_length = random.randint(RandomPasswordGenerator.min_length_of_password,
                                         RandomPasswordGenerator.max_length_of_password)

        # Atleast one Uppercase character
        password_characters.append(random.choice(string.ascii_uppercase))

        # Atleast one Lowercase character
        password_characters.append(random.choice(string.ascii_lowercase))

        # Atleast one digit
        password_characters.append(random.choice(string.digits))

        #Atleast one punctuation character
        password_characters.append(random.choice(string.punctuation))

        remaining_password_length = password_length - len(password_characters)

        all_valid_character_list = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation

        for _ in range(remaining_password_length):
            password_characters.append(random.choice(all_valid_character_list))

        return "".join(password_characters)


if __name__ == '__main__':
    print(RandomPasswordGenerator.generate_random_password())