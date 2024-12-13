

QUESTIONS = {
    'Q1': {
        'section': 'Primary objective',
        'text': 'The principle objective of this investment is…',
        'options': {
            'a': ('To generate income', 3),
            'b': ('To preserve or guarantee investment capital', 6),
            'c': ('To achieve real returns (i.e. returns that beat inflation)', 9),
            'd': ('To achieve maximum capital growth', 10)
        }
    },
    'Q2': {
        'section': 'Investment term',
        'text': 'The investment term for this investment is…',
        'options': {
            'a': ('Less than 1 year', 3),
            'b': ('1 to 3 years', 6),
            'c': ('3 to 5 years', 9),
            'd': ('More than 5 years', 13)
        }
    },
    'Q3': {
        'section': 'Risk profile',
        'text': 'I understand the effects of inflation. I prefer:',
        'options': {
            'a': ('To accept an appropriate level of risk as I require my investment to perform well ahead of inflation over time', 5),
            'b': ('To accept an appropriate level of risk as I require my investment to keep up with inflation over time', 3),
            'c': ('To preserve my capital at all costs even though this may mean returns are sometimes less than inflation', 1)
        }
    },
    'Q4': {
        'section': 'Risk profile',
        'text': 'How important is it to you to achieve stable, consistent returns from this investment year in & year out?',
        'options': {
            'a': ('Not very important, provided that the long-term outcome produces an above-average return that outpaces inflation', 5),
            'b': ('Reasonably important, but I can accept marginal variances in the value of my portfolio', 3),
            'c': ('Very important and I wish to avoid volatile swings in my fund values', 1)
        }
    },
    'Q5': {
        'section': 'Risk profile',
        'text': 'What is the maximum capital loss that you would be willing to bear over the short-term if markets fell?',
        'options': {
            'a': ('Above 20% - I am prepared to accept above average risk', 7),
            'b': ('10% to 20% - I consider myself to be a moderate-risk investor', 5),
            'c': ('0% to 10% - I consider myself to be a cautious investor', 4),
            'd': ('I would really not like to face the possibility of a capital loss', 3)
        }
    },
    'Q6': {
        'section': 'Risk profile',
        'text': 'My first consideration when approaching this investment is:',
        'options': {
            'a': ('I am willing to take more risk in order to beat inflation and obtain possible capital growth', 5),
            'b': ('I am committed to the investment term and believe that I have the discipline required', 3),
            'c': ('The level of risk is most important to me and I am willing to achieve more subdued returns', 1)
        }
    },
    'Q7': {
        'section': 'Risk profile',
        'text': 'When it comes to investing:',
        'options': {
            'a': ('I invest in shares, make my own decisions on what to buy and sell', 5),
            'b': ('I fully understand financial matters but do not actively manage my investments', 3),
            'c': ('I consider my investment knowledge to be average', 2),
            'd': ('I consider my investment knowledge to be below average', 1)
        }
    },
    'Q8': {
        'section': 'Risk profile',
        'text': 'In times of excessive market volatility and fluctuation I:',
        'options': {
            'a': ('Am able to adhere to a long-term strategy', 5),
            'b': ('Am tempted to sell after a year if things have not recovered', 3),
            'c': ('Will sell if the underperformance prevails for more than six months', 2),
            'd': ('Am very concerned and am tempted to sell immediately', 1)
        }
    },
    'Q9': {
        'section': 'Risk profile',
        'text': 'Assuming an inflation rate of 6%, which outcome is most acceptable for R100,000 over five years?',
        'options': {
            'a': ('Best case: R250,000; worst case R80,000', 10),
            'b': ('Best case: R195,000; worst case R90,000', 5),
            'c': ('Best case: R140,000; worst case R100,000', 1)
        }
    },
    'Q10': {
        'section': 'Risk profile',
        'text': 'How dependent are you on the proceeds of this investment?',
        'options': {
            'a': ('Not dependent at all; I can take risks that may lead to capital losses', 7),
            'b': ('Partially dependent; I can tolerate a marginal loss of 5-10%', 6),
            'c': ('Fairly dependent; I would not like to lose more than 5%', 5),
            'd': ('Totally dependent; I would not like to lose capital', 3)
        }
    },
    'Q11': {
        'section': 'Risk profile',
        'text': 'Would you accept risk to potentially enhance your return significantly?',
        'options': {
            'a': ('I am prepared to take the chance and accept more risk than normal', 5),
            'b': ('I am prepared to accept higher risk with reasonable certainty of higher returns', 4),
            'c': ('I would be inclined to follow the safer route', 3),
            'd': ('I am unwilling to take on more risk than I have to', 2)
        }
    }
}

RISK_PROFILES = {
    (20, 30): ('Conservative', {
        'Local equity': 10,
        'Local bonds': 50,
        'Local cash': 25,
        'Global assets': 15
    }),
    (31, 45): ('Cautious', {
        'Local equity': 15,
        'Local bonds': 50,
        'Local cash': 20,
        'Global assets': 15
    }),
    (46, 65): ('Moderate', {
        'Local equity': 20,
        'Local bonds': 45,
        'Local cash': 20,
        'Global assets': 15
    }),
    (66, 77): ('Aggressive', {
        'Local equity': 25,
        'Local bonds': 45,
        'Local cash': 15,
        'Global assets': 15
    })
}
