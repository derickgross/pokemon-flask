from flask import Flask, jsonify, request
import sqlite3
from models import init_db

app = Flask(__name__)
init_db.initialize_database()

@app.route("/api/pokemon/<param_id>", methods=["GET"])
def handle_api_pokemon_id(param_id):
    try:
        id = int(param_id)
    except:
        return jsonify({"error": "Invalid Pokémon ID"}), 400

    if not isinstance(id, int):
        return jsonify({"error": "Invalid Pokémon ID"}), 400
    
    if request.method == "GET":
        return get_pokemon(id)
    

@app.route("/api/pokemon", methods=["POST"])
def handle_api_pokemon():    
    if request.method == "POST":
        return create_pokemon(request.args)
    

def create_pokemon(args):
    required_fields = [
        "name",
        "type_1",
        "total",
        "hp",
        "attack",
        "defense",
        "special_attack",
        "special_defense",
        "speed",
        "generation",
        "legendary"
    ]
    missing_fields = []

    for field in required_fields:
        if field not in args:
            missing_fields.append(field)

    if missing_fields:
        return jsonify({"error": f"Missing required fields to create new Pokémon: {', '.join(missing_fields)}"}), 400
    else:
        con = sqlite3.connect("pokemon.db")
        cur = con.cursor()

        # query database to find out which is the next available pokemon ID
        cur.execute("SELECT COUNT(*) FROM pokemon")
        next_id = cur.fetchone()[0] + 1

        parameter_markers = ", ".join(["?" for field in required_fields])

        field_values = [args.get(field) for field in required_fields]

        cur.execute(f"INSERT INTO pokemon (id, {', '.join(required_fields)}) VALUES (?, {parameter_markers});", [next_id] + field_values)

        con.commit()
        con.close()

        return jsonify({"message": f"Pokemon created successfully with id {next_id}"}), 201
    

def get_pokemon(id):
    con = sqlite3.connect("pokemon.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    res = cur.execute(f"SELECT * FROM pokemon where ID = {id}")
    row = res.fetchone()

    if not row:
        return jsonify({"error": "Pokémon not found"}), 404
    else:
        pokemon = {
            "id": row["id"],
            "name": row["name"],
            "type_1": row["type_1"],
            "type_2": row["type_2"],
            "total": row["total"],
            "hp": row["hp"],
            "attack": row["attack"],
            "defense": row["defense"],
            "special_attack": row["special_attack"],
            "special_defense": row["special_defense"],
            "speed": row["speed"],
            "generation": row["generation"],
            "legendary": row["legendary"]
        }
        return jsonify(pokemon), 200
