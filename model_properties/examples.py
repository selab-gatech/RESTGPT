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
    }
]

PARAMETER_EXAMPLE_EXAMPLES = [
    {
        "input": "'The country code associated with the country. Examples are CAD, USD, etc...'",
        "output":
"""AFG, ALA, ALB, DZA, ASM, AND, AGO, AIA, ATA, ATG, ARG, ARM, ABW, AUS, AUT, AZE, BHS, BHR, BGD, BRB, BLR, BEL, 
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
        "input": "'The numbers must values for the percent grades must be to one decimal place (such as 10.6).'",
        "output": "None"
    }

]