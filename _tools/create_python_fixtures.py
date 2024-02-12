import json

topic = 1

questions = [
    'Who is the creator of Python?',
    'In what year was the first public version of Python released?',
    'What is the "print()" function in Python used for?',
    'sentence": "What does the acronym "PEP" stand for in the context of Python?',
    'What is the difference between a list and a tuple in Python?',
    'What is Object-Oriented Programming (OOP) and how is it implemented in Python?',
    'What is the difference between "==" and "is" in Python?',
    'What is a dictionary in Python and how is it declared?',
    'What is a "for" loop and how is it used in Python?',
    'What is the "len()" function in Python and what is it commonly used for?'
]

answers = {
    "1": [
        "Guido van Rossum",
        "Linus Torvalds",
        "Tim Berners-Lee",
        "Donald Knuth"
    ],
    "2": [
        "1991",
        "1989",
        "1995",
        "2000"
    ],
    "3": [
        "To display output on the screen",
        "To read input from the user",
        "To perform mathematical calculations",
        "To create a new variable"
    ],
    "4": [
        "Python Enhancement Proposal",
        "Python External Package",
        "Python Engineering Practice",
        "Python Error Protocol"
    ],
    "5": [
        "The main difference is that lists are mutable and tuples are immutable",
        "Tuples can contain only integers while lists can contain any data type",
        "Lists are indexed starting from 1 while tuples are indexed starting from 0",
        "There is no difference, they can be used interchangeably"
    ],
    "6": [
        "OOP is a programming paradigm based on the concept of objects, which can contain data and code",
        "OOP is a programming language developed by Microsoft",
        "OOP is a library in Python used for file I/O operations",
        "OOP is a Python module for creating graphical user interfaces (GUIs)"
    ],
    "7": [
        "'==' compares the values of two objects, while 'is' compares their memory addresses",
        "'==' compares the memory addresses of two objects, while 'is' compares their values",
        "'==' is used for assignment, while 'is' is used for comparison",
        "'==' is used for comparison of strings, while 'is' is used for comparison of numbers"
    ],
    "8": [
        "A dictionary is a collection of key-value pairs, declared using curly braces {}",
        "A dictionary is a sorted collection of elements, declared using square brackets []",
        "A dictionary is an ordered collection of elements, declared using parentheses ()",
        "A dictionary is a collection of elements, declared using the keyword 'dict'"
    ],
    "9": [
        "A 'for' loop is used to iterate over a sequence (such as a list, tuple, or string) in Python",
        "A 'for' loop is used to define a function in Python",
        "A 'for' loop is used to perform arithmetic operations in Python",
        "A 'for' loop is used to declare variables in Python"
    ],
    "10": [
        "The 'len()' function returns the length (number of elements) of a sequence",
        "The 'len()' function converts a string to lowercase",
        "The 'len()' function returns the largest element in a sequence",
        "The 'len()' function returns the smallest element in a sequence"
    ]
}

question_fixtures = []
answers_fixtures = []
for i, sentence in enumerate(questions):
    qpk = i + 1
    question = dict(
        model = "trivia.Question",
        pk = qpk,
        fields=dict(
            sentence = sentence,
            topic = topic
        )
    )
    question_fixtures.append(question)

    for j, sentence in enumerate(answers[str(qpk)]):
        answer = dict(
            model = "trivia.Answer",
            pk = len(answers_fixtures) + 1,
            fields = dict(
                sentence = sentence,
                is_correct = True if j == 0 else False,
                question = qpk
            )
        )
        answers_fixtures.append(answer)

with open('question_fixtures.json', "w", encoding='utf-8') as file:
    json.dump(question_fixtures, file, indent=4, ensure_ascii=False)

with open('anwer_fixtures.json', "w", encoding='utf-8') as file:
    json.dump(answers_fixtures, file, indent=4, ensure_ascii=False)