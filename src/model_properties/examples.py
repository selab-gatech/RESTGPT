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
"""PROVIDED: CAD, USD +++ GENERATED: AFG, ALA, ALB, DZA, ASM, AND, AGO, AIA, ATA, ATG, ARG, ARM, ABW, AUS, AUT, AZE, BHS, BHR, BGD, BRB, BLR, BEL, 
BLZ, BEN, BMU, BTN, BOL, BES, BIH, BWA, BVT, BRA, IOT, BRN, BGR, BFA, BDI, CPV, KHM, CMR, CAN, CYM, CAF, TCD, 
CHL, CHN, CXR, CCK, COL, COM, COG, COD, COK, CRI, CIV, HRV, CUB, CUW, CYP, CZE, DNK, DJI, DMA, DOM, ECU, EGY, 
SLV, GNQ, ERI, EST, SWZ, ETH, FLK, FRO, FJI, FIN, FRA, GUF, PYF, ATF, GAB, GMB, GEO, DEU, GHA, GIB, GRC, GRL, 
GRD, GLP, GUM, GTM, GGY, GIN, GNB, GUY, HTI, HMD, VAT, HND, HKG, HUN, ISL, IND, IDN, IRN, IRQ, IRL, IMN, ISR, 
ITA, JAM, JPN, JEY, JOR, KAZ, KEN, KIR, PRK, KOR, KWT, KGZ, LAO, LVA, LBN, LSO, LBR, LBY, LIE, LTU, LUX, MAC, 
MDG, MWI, MYS, MDV, MLI, MLT, MHL, MTQ, MRT, MUS, MYT, MEX, FSM, MDA, MCO, MNG, MNE, MSR, MAR, MOZ, MMR, NAM, 
NRU, NPL, NLD, NCL, NZL, NIC, NER, NGA, NIU, NFK, MKD, MNP, NOR, OMN, PAK, PLW, PSE, PAN, PNG, PRY, PER, PHL, 
PCN, POL, PRT, PRI, QAT, REU, ROU, RUS, RWA, BLM, SHN, KNA, LCA, MAF, SPM, VCT, WSM, SMR, STP, SAU, SEN, SRB, 
SYC, SLE, SGP, SXM, SVK, SVN, SLB, SOM, ZAF, SGS, SSD, ESP, LKA, SDN, SUR, SJM, SWE, CHE, SYR, TWN, TJK, TZA, 
THA, TLS, TGO, TKL, TON, TTO, TUN, TUR, TKM, TCA, TUV, UGA, UKR, ARE, GBR, USA, UMI, URY, UZB, VUT, VEN, VNM, 
VGB, VIR, WLF, ESH, YEM, ZMB, ZWE"""
    },
    {
        "input": "'The numbers for the percent grades must be to one decimal place (such as 10.6).'",
        "output":
"""PROVIDED: 10.6 +++ GENERATED: 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 
2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 
4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 
6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0, 
9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10.0, 99.9, 100.0"""
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