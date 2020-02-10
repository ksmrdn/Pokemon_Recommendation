from flask import Flask, abort, render_template, request, send_from_directory, url_for, redirect, jsonify
import pandas as pd 
import numpy as np 
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        poke= request.form['pokemon']
        poki = poke.lower()
        url = 'https://pokeapi.co/api/v2/pokemon'
        raw_data = requests.get(url)
        pokemon_allData = raw_data.json()
        pokemon_listed = pokemon_allData['results']
        i = 0
        while i in range(len(pokemon_listed)):
            cek = pokemon_listed[i]['name']
            if poki == cek :
                url_poke = 'https://pokeapi.co/api/v2/pokemon/'+poki+'/'
                raw_data = requests.get(url_poke)
                allData = raw_data.json()
                nama_pokemon = allData['forms'][0]['name']
                pokemon_id =allData['id']
                tinggi = allData['height'] 
                berat = allData['weight']
                url_image = allData['sprites']['front_default']
                return render_template('result.html', nama_pokemon=nama_pokemon.capitalize(), pokemon_id=pokemon_id, tinggi=tinggi, url_image=url_image, berat=berat)
            i+=1
        else:
            return render_template('notFound.html')
    else:
        poke= request.form['pokemon']
        poki = poke.lower()
        url = 'https://pokeapi.co/api/v2/pokemon'
        raw_data = requests.get(url)
        pokemon_allData = raw_data.json()
        pokemon_listed = pokemon_allData['results']
        i = 0
        while i in range(len(pokemon_listed)):
            cek = pokemon_listed[i]['name']
            if poki == cek :
                url_poke = 'https://pokeapi.co/api/v2/pokemon/'+poki+'/'
                raw_data = requests.get(url_poke)
                allData = raw_data.json()
                nama_pokemon = allData['forms'][0]['name']
                pokemon_id =allData['id']
                tinggi = allData['height'] 
                berat = allData['weight']
                url_image = allData['sprites']['front_default']
                return render_template('result.html', nama_pokemon=nama_pokemon.capitalize(), pokemon_id=pokemon_id, tinggi=tinggi, url_image=url_image, berat=berat)
            i+=1
        else:
            return render_template('notFound.html')    
#========================================================================================================
# TEMP IMAGE
@app.route('/filetemp/<path:path>')                           
def filetemp(path):
    return send_from_directory('./templates/image', path)

@app.errorhandler(404)                                              
def notFound(error) :                                               
    return render_template('error.html')

if __name__ == '__main__':                 
    app.run(debug = True)  