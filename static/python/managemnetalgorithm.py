"""
Essentially this is a time management

you input how many hours you have and how much time that you want

--base-- makes intervals
    
--premium
"""


def basefunction(timestudy, timerelax):
    timeneeded = timestudy - timerelax
    remainder = timeneeded % 25
    if remainder < 10:
        return int(timeneeded / timerelax)
    else:
        return int(timeneeded / timerelaxed) + 1


# we needa
