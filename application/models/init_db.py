import csv, os, sqlite3

def initialize_database():
    print("initializing database!")

    con = sqlite3.connect("pokemon.db")
    cur = con.cursor()

    table_fields = [
        "id",
        "name",
        "type_1",
        "type_2",
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

    create_table = """
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type_1 TEXT NOT NULL,
            type_2 TEXT,
            total INTEGER NOT NULL,
            hp INTEGER NOT NULL,
            attack INTEGER NOT NULL,
            defense INTEGER NOT NULL,
            special_attack INTEGER NOT NULL,
            special_defense INTEGER NOT NULL,
            speed INTEGER NOT NULL,
            generation INTEGER NOT NULL,
            legendary BOOLEAN NOT NULL DEFAULT 0
        );
    """

    cur.execute(create_table)

    # confirm table is empty before attempting to seed data
    cur.execute("SELECT COUNT(*) FROM pokemon")
    count = cur.fetchone()[0]

    if count == 0:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        csv_path = os.path.join(dir_path, "..", "static_files", "Pokemon.csv")

        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)


            table_inserts = []
            parameter_markers = ", ".join(["?" for field in table_fields]) # count of parameter markers in insert statement below must match field count

            # order of fields in table_fields must match CSV column order
            for row in reader:
                row_values = tuple([row[field] for field in table_fields])
                table_inserts.append(row_values)

        cur.executemany(f"INSERT INTO pokemon ({', '.join(table_fields)}) VALUES ({parameter_markers});", table_inserts)

    con.commit()
    con.close()
    print("Database initialization complete")
