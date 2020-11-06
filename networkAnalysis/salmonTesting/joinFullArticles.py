import os

folderSub250 = 'fullArticleInfo'
sub250Files = os.listdir(folderSub250)

over250Data = 'over250FullArticles.csv'

fOver = open(over250Data, 'r')
totalData = fOver.readlines()
fOver.close()

for subF in sub250Files:
    f = open(os.path.join(folderSub250, subF), 'r')
    totalData.extend(f.readlines()[1:])
    f.close()

fTotal = open('TotalFullArticleData.csv', 'w')
for line in totalData:
    fTotal.write(line)

fTotal.close()
print("done aggregating all data!")