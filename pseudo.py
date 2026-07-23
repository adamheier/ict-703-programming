#I have a jar of M&M's (red, green, yellow, blue, brown). I want to sort them into their colours but I want to throw away the blue M&M's.

def sort_mms(mms):
    '''Jede Farbe bekommt ihre eigene Dose, blaue M&M\'s werden weggeworfen.'''
    red_dose = []
    green_dose = []
    yellow_dose = []
    brown_dose = []

    for mm in mms:
        match mm:
            case 'blue':
                # blaue M&M's werden nicht in eine Dose gelegt, sondern weggeworfen
                pass
            case 'red':
                red_dose.append(mm)
            case 'green':
                green_dose.append(mm)
            case 'yellow':
                yellow_dose.append(mm)
            case 'brown':
                brown_dose.append(mm)

    return red_dose, green_dose, yellow_dose, brown_dose


# main
if __name__ == "__main__":
    mms = ['red', 'green', 'blue', 'yellow', 'brown', 'blue', 'green', 'red', 'yellow', 'brown']
    red_dose, green_dose, yellow_dose, brown_dose = sort_mms(mms)
    print("Red M&M's:", red_dose)
    print("Green M&M's:", green_dose)
    print("Yellow M&M's:", yellow_dose)
    print("Brown M&M's:", brown_dose)


#Three jars of lollies. Three piles and I want to eat my favorite lillies last. Pile1 are my favourite lollies and pile 3 my least favourite. The lollies are: pile3 = orange, pile2 = berry, pile1 = cherry.
'''
For all lollies in the jar do the following:
if lollie is cherry
    put on pile1
elif lollie is berry
    put on pile2
else lollie is orange
    put on pile3
'''

def sort_lollies(lollies):
    '''Sort lollies into piles based on preference.'''
    pile1 = []  # Favorite lollies (cherry)
    pile2 = []  # Medium preference (berry)
    pile3 = []  # Least favorite (orange)

    for lollie in lollies:
        if lollie == 'cherry':
            pile1.append(lollie)
        elif lollie == 'berry':
            pile2.append(lollie)
        else:  # lollie is orange
            pile3.append(lollie)

    return pile1, pile2, pile3

# main
if __name__ == "__main__":
    lollies = ['orange', 'berry', 'cherry', 'orange', 'berry', 'cherry', 'cherry', 'berry', 'cherry', 'cherry']
    pile1, pile2, pile3 = sort_lollies(lollies)
    print("Pile 1 (Favorite - Cherry):", pile1)
    print("Pile 2 (Medium - Berry):", pile2)
    print("Pile 3 (Least Favorite - Orange):", pile3)