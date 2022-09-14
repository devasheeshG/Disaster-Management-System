from pyresparser import ResumeParser
from docx import Document
from flask import Flask,render_template,redirect,request
import pandas as pd
import re
from ftfy import fix_text
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

hello_2 = set(stopwords.words('english'))

data_set =pd.read_csv('job_final.csv') 
data_set['test']=data_set['Job_Description'].apply(lambda x: 
    ' '.join([word for word in str(x).split() if len(word)>2 and word not in (hello_2)]))

webapp=Flask(__name__)
choice=input("answer")
if(choice=="y"):
    exec(open("second_version.py").read())
else:
 @webapp.route('/')
 def hello():
    return render_template("model.html")



 @webapp.route("/home")
 def home():
    return redirect('/')

 @webapp.route('/submit',methods=['POST'])
 def submit_data():
    if request.method == 'POST':
        
        f=request.files['userfile']
        f.save(f.filename)
        try:
            documents = Document()
            with open(f.filename, 'r') as file:
                documents.add_paragraph(file.read())
                documents.save("text.docx")
                data = ResumeParser('text.docx').get_extracted_data()
                
        except:
            data = ResumeParser(f.filename).get_extracted_data()
        resume=data['skills']
        print(type(resume))
    
        skills_set=[]
        skills_set.append(' '.join(word for word in resume))
        org_name_change = skills_set
        
        def ngrams(fixstring, n=3):
            fixstring = fix_text(fixstring) # fix text
            fixstring = fixstring.encode("ascii", errors="ignore").decode() #remove non ascii chars
            fixstring = fixstring.lower()
            chars_to_remove = [")","(",".","|","[","]","{","}","'"]
            rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
            fixstring = re.sub(rx, '', fixstring)
            fixstring = fixstring.replace('&', 'and')
            fixstring = fixstring.replace(',', ' ')
            fixstring = fixstring.replace('-', ' ')
            fixstring = fixstring.title() # normalise case - capital at start of each word
            fixstring = re.sub(' +',' ',fixstring).strip() # get rid of multiple spaces and replace with a single
            fixstring = ' '+ fixstring +' ' # pad names for ngrams...
            fixstring = re.sub(r'[,-./]|\sBD',r'', fixstring)
            ngrams = zip(*[fixstring[i:] for i in range(n)])
            return [''.join(ngram) for ngram in ngrams]
        vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams, lowercase=False)
        tfidf = vectorizer.fit_transform(org_name_change)
        print('Vector transformation completed...')
        
        
        def getNearestN(query):
          queryTFIDF_ = vectorizer.transform(query)
          distances, indices = nbrs.kneighbors(queryTFIDF_)
          return distances, indices
        nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf)
        unique_org = (data_set['test'].values)
        distances, indices = getNearestN(unique_org)
        unique_org = list(unique_org)
        matches = []
        for i,j in enumerate(indices):
            dist=round(distances[i][0],2)
  
            temp = [dist]
            matches.append(temp)
        matches = pd.DataFrame(matches, columns=['Match confidence'])
        data_set['match']=matches['Match confidence']
        data_sort1=data_set.sort_values('match')
        data_sort2=data_sort1[['Position', 'Company','Location']].head(10).reset_index()
        
        
        
        
        
   
    return render_template('model.html',tables=[data_sort2.to_html(classes='job')],titles=['na','Job'])
        
        
        
        
        
if __name__ =="__main__":
    
    
    webapp.run()