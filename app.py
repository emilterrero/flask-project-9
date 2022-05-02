from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('pets', user='emil', password='', host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Pet(BaseModel):
    name = CharField()
    species = CharField()
    age = IntegerField()

db.connect()
db.drop_tables([Pet])
db.create_tables([Pet])

Pet(name='Pinky', species='dog', age='2').save()
Pet(name='Speedy', species='hamster', age='1').save()
Pet(name='Rufus', species='hamster', age='1').save()
Pet(name='Tony', species='cat', age='5').save()
Pet(name='Leo', species='cat', age='2').save()

app = Flask(__name__)

@app.route('/') 
def index():
    return "Connected to Server"

@app.route('/pets/', methods=['GET', 'POST'])
@app.route('/pets/<id>', methods=['GET, DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id: 
            return jsonify(model_to_dict(Pet.get(Pet.id == id)))
        else: 
            all_pets = []
            for pet in Pet.select():
                all_pets.append(model_to_dict(pet))
            return jsonify(all_pets)

    if request.method == 'POST':
        create_pet = dict_to_model(Pet, request.get_json())
        create_pet.save()
        return jsonify({"Pet Created": True})

    if request.method == 'DELETE':
        delete_pet = Pet.get(Pet.id == id)
        delete_pet.delete_instance()
        return jsonify({"Pet deleted": True})

app.run(port=5000, debug=True)
