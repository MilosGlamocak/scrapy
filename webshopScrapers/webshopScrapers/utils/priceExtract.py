import re

def extractPrices(item):
    '''with open('threedbox/threedboxItems.json', encoding='utf-8') as itemsFile:
        items = json.load(itemsFile)
    htmlString = json.dumps(items[1245]["price"], indent=4, ensure_ascii=False)'''
    pattern = re.compile(r'(\d{1,3}(?:\.\d{3})*,\d{2})')
    matches = pattern.findall(item)

    def convertPrice(str):
        return float(str.replace('.','').replace(',','.'))

    matches = [convertPrice(price) for price in matches]

    maxValue = matches[0]
    minValue = matches[0]

    for number in matches:
        if maxValue < number:
            maxValue = number
        if minValue > number:
            minValue = number

    
    maxValueString = format(maxValue, '.2f').replace('.', ',')
    if minValue == maxValue:
        minValue = None
    else:
        minValueString = format(minValue, '.2f').replace('.', ',')
    print([maxValue, minValue])

    return({"regular": maxValue, "sale": minValue})
