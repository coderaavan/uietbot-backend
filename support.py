import spacy
import datetime
nlp=spacy.load('en_core_web_sm')

def keyWordExtractor(text):
    textlist=text.split(" ")

    Months=['january','february','march','april','may','june','july','august','september','october','november','december']
    events=["assignment","assignments","exam","exams"]

    for x in xrange(0,len(textlist)):
        if (textlist[x].endswith('th') or textlist[x].endswith('nd') or textlist[x].endswith('st')) and textlist[x][-3] in [str(i) for i in xrange(1,9)]:
            textlist[x]=textlist[x][:-2]

        if textlist[x] in Months:
            textlist[x]=textlist[x].capitalize()

        if textlist[x] in events and textlist[x][-1] != 's':
            textlist[x]=textlist[x]+'s'


    text= ' '.join(word for word in textlist)

    branches=["IT","it","CSE","cse","ECE","ece"]

    querydict={
        'Branch':"IT",
        'Sem':"7",
        'Section':"B",
        'Event':"assignments",
        'Date':"9999-99-99",
        'BOA':"before"
    }

    for x in textlist:
        if x.lower() in ["before","after"]:
            querydict['BOA']=x.lower()


    for branch in branches:
        if branch in textlist:
            querydict['Branch']=branch.upper()
            i=textlist.index(branch)
            left=0 if i<5 else i-5 
            right=i+5 if i+5<len(textlist)-1 else len(textlist)-1
            for x in xrange(left,right+1):
                if textlist[x] in ['a','A','b','B']:
                    querydict['Section']=textlist[x].upper()
                    break

            for x in xrange(left,right+1):
                if textlist[x] in [str(i) for i in xrange(1,9)] and textlist[x+1].lower() not in Months:
                    querydict['Sem']=textlist[x]

            break


    query=nlp(text)


    # This segment of code can be modified to execute multiple queries. Just remove break and replicate querydict for each query

    for word in query.noun_chunks:
        possibleEvents=word.text.lower().split(" ")
        for pe in possibleEvents:
            if pe in events:
                querydict['Event']=pe
                break

        if querydict['Event']!=" ":
            break


    for word in query.ents:
        if word.label_=="DATE":
            mm=" "
            dd=" "
            dateList=word.text.split(" ")
            print dateList
            for dateItem in dateList:
                if dateItem.lower() in Months:
                    mm=str(Months.index(dateItem.lower())+1)
                    if len(mm)==1:
                        mm='0'+mm
                    else:
                        pass
                elif dd==" " and len(dateItem)<=2:
                    dd=dateItem
                    if len(dd)==1:
                        dd='0'+dd

            date=str(datetime.datetime.now().year)+'-'+mm+'-'+dd
            querydict["Date"]=date

    return querydict