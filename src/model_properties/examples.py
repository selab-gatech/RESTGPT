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

PARAMETER_FORMAT_EXAMPLES = [
    {
        "input": "'The list of percent grades corresponding to the student.'",
        "output": "type array, items number, format None"
    },
    {
        "input": "'This should contain the email of the sender.'",
        "output": "type string, items None, format email"
    },
    {
        "input": "'This value should be true if the assignment is available for regrade.'",
        "output": "type boolean, items None, format None"
    },
    {
        "input": "'A URL containing the website for evaluation.'",
        "output": "type string, items None, format url"
    },
    {
        "input": "'The date of the contest. The date must be within the last three months.'",
        "output": "type string, items None, format date"
    },
    {
        "input": "'The time that the project must be completed. Use Eastern Standard Timezone (EST).'",
        "output": "type string, items None, format date-time"
    }
]

PARAMETER_CONSTRAINT_EXAMPLES = [
    {
        "input": "'An idea for a project. This and 'rating' are required.'",
        "output": "min None, max None"
    },
    {
        "input": "'The maximum value is 50. If nothing is put in, default to 0.'",
        "output": "min None, max 50"
    },
    {
        "input": "'The timer counter. The value must be between 15.0 and 120.'",
        "output": "min 15.0, max 120"
    },
    {
        "input": "'The input range. The smallest value possible is -120.8. The largest should be 179.652.'",
        "output": "min -120.8, max 179.652"
    },
    {
        "input": "'The number of items to be investigated. The maximum is 9,999.99'",
        "output": "min None, max 9999.99"
    },
    {
        "input": "The stock quantity. The smallest possible value is 1,200. All the values should be less than 8,999.",
        "output": "min 1200, max 8999"
    },
    {
        "input": "'The name of the movie. The movie name cannot be shorter than 10 characters and longer than 20 characters.'",
        "output": "minLength 10, maxLength 20"
    }
]

PARAMETER_EXAMPLE_EXAMPLES = [
    {
        "input": "'The country code associated with the country. Examples are CAD, USD, etc...'",
        "output":
"""PROVIDED: CAD, USD +++ GENERATED: AED, AFN, ALL, AMD, ANG, AOA, ARS, AUD, AWG, AZN, BAM, BBD, BDT, BGN, BHD, BIF, BMD, BND, BOB"""
    },
    {
        "input": "'The numbers for the percent grades must be to one decimal place (such as 10.6).'",
        "output":
"""PROVIDED: 10.6 +++ GENERATED: 0.0, 10.0, 20.1, 30.2, 40.3, 50.4, 60.5, 70.6, 80.7, 90.8, 100.0"""
    },
    {
        "input": "'The title of the book to be rated.'",
        "output":
"""PROVIDED: None +++ GENERATED: To Kill a Mockingbird, 1984, Pride and Prejudice, The Great Gatsby, Moby-Dick, The Catcher in the Rye, Harry Potter 
and the Sorcerer's Stone, The Lord of the Rings, One Hundred Years of Solitude, Brave New World, Sapiens: A Brief 
History of Humankind, The Immortal Life of Henrietta Lacks, Thinking, Fast and Slow, The Wright Brothers, The Diary of 
a Young Girl, Educated, The Art of War, The 7 Habits of Highly Effective People, Freakonomics, Quiet: The Power of 
Introverts in a World That Can't Stop Talking, Dune, Ender's Game, Neuromancer"""
    }
]

IDL_OPERATION_CONSTRAINT_EXAMPLES = [
    {
        "input" : """
name: text 
description: The text to be checked. This or 'data' is required.""", 
        "output": "Or(text, data);"
    }, 
    { "input": """ 
     name: idea
     description: 'An idea for a project. This and 'rating' are required.'""", 
     "output": "OnlyOne(idea AND rating);"
    }, 
    {"input": """
      name: partID
      description: 'The ID of the part. If partModel is specified partID must be specified'""",
      "output": "IF partModel THEN partID;"
    }, 
    {"input": """
       name: language 
       description: The language of the client, not required if the country-code is USA or CAN.""",
       "output": "IF country-code!='USA' OR country-code=='CAN' THEN language;"
    },
    {
        'input': """
        name: cost
        description: The cost of the product, this - profit must be greater than 500.""", 
        'output': "cost - profit > 500;"
    }
]