import googletrans

def translateTitle(oldTitle):
    try:
        translator = googletrans.Translator()
        newTitle = translator.translate(oldTitle).text
    except:
        return oldTitle
    return newTitle

f = open('R_working_dir/TotalFullArticleData.csv', 'r')
data = f.readlines()
f.close()

#translator  = googletrans.Translator()
incorrectRows = []

for lineIdx in range(len(data)):
    if lineIdx >= 1:
        line = data[lineIdx].rstrip('\n')
        cells = line.split(',')
        title = cells[7]
        lang = cells[-1]
        #print(lang)
        if title != 'FIS':
            if lang != 'English':
                print(f"LANG {lang} {title} {type(title)}")
                newTitle = translateTitle(title)
                if newTitle == title:
                    print("added to didn't work")
                    incorrectRows.append(line)
                else:
                    print(f"NEW TITLE {newTitle}")
                    cells[7] = newTitle
                    newRow = ''
                    for cell in cells:
                        newRow += cell + ','
                    newRow = newRow[:-1] + '\n'
                    #print(newRow)
                    data[lineIdx] = newRow


fIncorrect = open('R_working_dir/nonTranslatedArticles.csv', 'w')
fIncorrect.write(data[0])
for row in incorrectRows:
    fIncorrect.write(row + '\n')
fIncorrect.close()

fOut = open('R_working_dir/translatedFullArticleData.csv', 'w')
for lOut in data:
    fOut.write(lOut)

fOut.close()
print("DONE!!!")