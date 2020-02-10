from flask import Flask, abort, render_template, request, send_from_directory, url_for, redirect, jsonify
import pandas as pd 
import numpy as np 
import json
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hasil',methods=['GET','POST'])
def recommendation():
    if request.method == 'POST':
        body = request.form
        fav = body['name']
        fav = fav.capitalize()

        if fav not in list(df_pokemon['Name']):
            return redirect('/notFound')
        ind_fav = df_pokemon[df_pokemon['Name']==fav].index.values[0]
        
        recom_poke = sorted(list(enumerate(csScore[ind_fav])), key=lambda a: a[1], reverse=True) 
        fav_poke = df_pokemon.iloc[ind_fav][cols]

        poke_sembarang = []
        for i in recom_poke:
            klop = {}
            if i[0] == ind_fav:
                continue
            else:
                num = df_pokemon.iloc[i[0]]['#']
                name = df_pokemon.iloc[i[0]]['Name']
                tipe = df_pokemon.iloc[i[0]]['Type 1']
                gen = df_pokemon.iloc[i[0]]['Generation']
                legend = df_pokemon.iloc[i[0]]['Legendary']
                klop['num'] = num
                klop['name'] = name
                klop['tipe'] = tipe
                klop['gen'] = gen
                klop['legend'] = legend
            poke_sembarang.append(klop)
            if len(poke_sembarang) == 6:
                break
        # print(poke_sembarang)
    return render_template('hasil.html', recommendation = poke_sembarang, myFav = fav_poke)

@app.route('/filetemp/<path:path>')                           
def filetemp(path):
    return send_from_directory('./templates/image', path)

@app.route('/notFound')
def notFound():
    return render_template('notFound.html')

if __name__ == "__main__":
    df_pokemon = pd.read_csv('Pokemon.csv')
    # print(df_pokemon['Name'][0])
    df_pokemon['Legendary'] = df_pokemon['Legendary'].replace({True: 'Legend', False:'Not Legend'})
    cols = ['#','Name','Type 1','Generation','Legendary']
    df_pokemon = df_pokemon[cols]
    df_pokemon['Compare'] = df_pokemon.apply (lambda i: f"{i['Type 1']},{(i['Generation'])},{(i['Legendary'])}", axis= 1)

    cv = CountVectorizer(tokenizer= lambda a: a.split(','))
    cvPoke = cv.fit_transform(df_pokemon['Compare'])

    csScore = cosine_similarity(cvPoke)

    app.run(debug=True, port=4400)