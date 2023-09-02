OPERATION_CONSTRAINT_EXAMPLES = [
    {
        "input": """
name: text
description: 'The text to be checked. This or 'data' is required.'""",
        "output": "text | data"
    },
    {
        "input": """
name: bidSelectionMethod
description: 'Valid examples are Đấu thầu rộng rãi, Đấu thầu hạn chế, etc...'""",
        "output": "None"
    },
    {
        "input": """
name: idea
description: 'An idea for a project. This and 'rating' are required.'""",
        "output": "idea & rating"
    },
    {
        "input": """
name: day
description: 'This is the day that the 'letter grade' is published. The field is grades.letter_grade'""",
        "output": "None"
    },
    {
        "input": """
name: comment
description: 'This is used with 'username' to define a post.'""",
        "output": "None"
    },
    {
        "input": """
name: organization
description: 'This is the organization used for finding data. This is required.'""",
        "output": "organization"
    }
]