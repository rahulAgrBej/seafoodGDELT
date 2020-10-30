import googletrans

f = open('R_working_dir/TotalFullArticleData.csv', 'r')
data = f.readlines()
f.close()

translator = googletrans.Translator()


for lineIdx in range(len(data)):
    if lineIdx >= 1:
        line = data[lineIdx].rstrip('\n')
        cells = line.split(',')
        title = cells[7]
        lang = cells[-1]
        #print(lang)
        if lang == 'Spanish':
            print(f"LANG {lang} {title} {type(title)}")
            newTitle = translator.translate(title).text
            while newTitle == title:
                print("trying again")
                try:
                    translator = googletrans.Translator() 
                    newTitle = translator.translate(title).text
                except Exception as e:
                    print(e)
            print(f"NEW TITLE {newTitle}")
            cells[7] = newTitle
            newRow = ''
            for cell in cells:
                newRow += cell + ','
            newRow = newRow[:-1] + '\n'
            #print(newRow)
            data[lineIdx] = newRow

fOut = open('R_working_dir/translatedFullArticleData.csv', 'r')
for lOut in data:
    fOut.write(lOut)

fOut.close()
print("DONE!!!")