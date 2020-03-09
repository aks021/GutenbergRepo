import mysql.connector

def getBaseQuery():
    return("""
    SELECT 
        book_id,
        download_count,
        birth_year,
        death_year, 
        author, 
        title, 
        language, 
        subjectName, 
        bookShelfName, 
        mime_type, 
        url
        FROM (
            SELECT 
                b.gutenberg_id book_id,
                b.download_count,
                a.birth_year,
                a.death_year, 
                a.name author, 
                b.title, 
                l.code language, 
                bs.name subjectName, 
                bb.name bookShelfName, 
                bf.mime_type, 
                bf.url
            FROM 
                books_author as a, 
                books_book as b, 
                books_book_authors as c, 
                books_language as l, 
                books_book_languages as lm,
                books_subject as bs,
                books_book_subjects as bbs,
                books_bookshelf as bb,
                books_book_bookshelves as bbsv,    
                books_format as bf
            WHERE 
                a.id = c.author_id AND b.id = c.book_id AND 
                lm.book_id = b.id AND lm.language_id = l.id AND
                bs.id = bbs.subject_id AND bbs.book_id = b.id AND
                bb.id = bbsv.bookshelf_id AND bbsv.book_id = b.id AND
                bf.book_id = b.id 
            ) 
        as T
""")

def composeFilters(filterDict):
    filterList = []
    if ('book_id' in filterDict.keys()):
        filterList.append("book_id IN "+str(tuple(filterDict['book_id'])))
    if ('language' in filterDict.keys()):
        filterList.append("language IN "+str(tuple(filterDict['language'])))
    if ('mime_type' in filterDict.keys()):
        filterList.append("mime_type IN "+str(tuple(filterDict['mime_type'])))
    if ('topic' in filterDict.keys()):
        filterList.append('subjectName REGEXP "('+('|'.join(filterDict['topic']))+')"')
        filterList.append('bookShelfName REGEXP "('+('|'.join(filterDict['topic']))+')"')
    if ('author' in filterDict.keys()):
        filterList.append('author REGEXP REGEXP "('+('|'.join(filterDict['author']))+')"')
    if ('title' in filterDict.keys()):
        filterList.append('title REGEXP REGEXP "('+('|'.join(filterDict['title']))+')"')
    return(' WHERE '+(' AND '.join(filterList)))

def getFinalQuery(filterDict, offset):
    filterQuery = ''
    if(filterDict != {}):
        filterQuery = composeFilters(filterDict)
    return(getBaseQuery() + filterQuery + ' ORDER BY download_count DESC LIMIT 25 OFFSET '+str(offset)+';')

def convertToDict(cursorObj, resultList):
    row_headers=[x[0] for x in cursorObj.description]
    json_data=[]
    for result in resultList:
        dataToPush = {}
        for index in range(0, len(row_headers)):
            dataToPush[row_headers[index]] = result[index]
        json_data.append(dataToPush)
    return json_data

def fetchDataFromDataBase(filterDict, page):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="bookstore",
        auth_plugin='mysql_native_password'
    )
    cursorObj = mydb.cursor()
    cursorObj.execute(getFinalQuery(filterDict, 25*page))
    myresult = cursorObj.fetchall()
    resultJson = convertToDict(cursorObj, myresult)
    return resultJson
