import requests
from io import BytesIO
from flask import Flask, render_template, send_file, request

app = Flask(__name__)
url = "https://pokeapi.glitch.me/v1/pokemon/"

if __name__ == "__main__":
    app.run()

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/pokeland/<string:pokeName>")
def pokeland(pokeName):
    try:
        pokeName = getPokemonName(pokeName)
        sprite = getPokemonSprite(pokeName)
        evolutionLine = getPokemonEvolutions(pokeName)
        pokemonDescription = getPokemonDescription(pokeName)
        pokeType = getPokemonType(pokeName)
        return render_template("poke.html", pokeName = pokeName, sprite = sprite, evolutionLine = evolutionLine, pokemonDescription = pokemonDescription, pokeType = pokeType)
    except:
        return render_template("error.html")+
    
def getPokeInfo(pokename):
    r = requests.get(url = url + pokename)
    data = r.json()
    return data[0]

def getPokemonName(pokename):
    pokeinfo = getPokeInfo(pokename)
    pokeName = pokeinfo["name"]
    return pokeName

def getPokemonSprite(pokename):
    pokeinfo = getPokeInfo(pokename)
    sprite = pokeinfo["sprite"]
    return sprite

def getPokemonEvolutions(pokename):
    pokeinfo = getPokeInfo(pokename)
    family = pokeinfo["family"]
    return family["evolutionLine"]

def getPokemonDescription(pokename):
    pokeinfo = getPokeInfo(pokename)
    pokeDescription = pokeinfo["description"]
    return pokeDescription

def getPokemonType(pokename):
    pokeinfo = getPokeInfo(pokename)
    pokeType = pokeinfo["types"]
    return pokeType

@app.route("/pokemonImage/<string:pokeName>")
def getPokemonImage(pokeName):
    url = ""
    try:
        pokeJson = getPokeInfo(pokeName)
        url = pokeJson["sprite"]
    except:
        url = 'https://preview.redd.it/u6vz78jfhn281.png?width=640&crop=smart&auto=webp&s=80e27782a493c347effa17a6b17ee974ea682737'
    find = requests.get(url)
    if find.status_code != 200:
        return "error"
    bufferImage = BytesIO(find.content)
    bufferImage.seek(0)
    return send_file(bufferImage, mimetype='image/png')

@app.route("/getPokedex", methods=['POST'])
def getPokedex():
    pokeName = request.form['pokeName']
    return pokeland(pokeName)