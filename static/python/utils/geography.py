import requests
from thefuzz import fuzz

def getCountry(country):
    if len(country) in [3, 2]:
        data = requests.get(f"https://restcountries.com/v2/alpha/{country}")
        data = data.json()

    else:
        data = requests.get(
            f"https://restcountries.com/v2/name/{country}?fullText=true"
        )
        data = data.json()
        if "status" in data:
            data = requests.get(f"https://restcountries.com/v2/name/{country}")
            data = data.json()
            if len(data) == 1:
                pass
            else:
                if "status" in data:
                    raise ValueError('Could not find that country')
                close_dict = {}

                for i, x in enumerate(data):
                    close_dict[i] = fuzz.ratio(country, x["name"])

                index = max(close_dict, key=close_dict.get) if close_dict else None

                if index:
                    data = data[index]
                else:
                    raise ValueError('Could not find that country')

    if "status" in data:
        raise ValueError('Could not find that country')

    else:
        if isinstance(data, list):
            data = data[0]
        return data


print(getCountry("United States"))