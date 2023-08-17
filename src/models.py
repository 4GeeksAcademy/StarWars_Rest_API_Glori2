from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorite',backref='user',lazy=True)

    def __repr__(self):
        return f"Usuario {self.email}"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    population = db.Column(db.Integer,nullable=True)
    diameter = db.Column(db.Integer,nullable=True)
    climate = db.Column(db.String(250),nullable=True)
    gravity = db.Column(db.String(250),nullable=True)
    terrain = db.Column(db.String(250),nullable=True)
    surface_water = db.Column(db.String(250),nullable=True)
    my_favorite = db.relationship('Favorite',backref='planet',lazy=True)

    def __repr__(self):
        return f"El planeta {self.name} con ID: {self.id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }
    
class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    height = db.Column(db.Integer,nullable=True)
    mass = db.Column(db.Integer,nullable=True)
    hair_color = db.Column(db.String(250),nullable=True)
    skin_color = db.Column(db.String(250),nullable=True)
    eye_color = db.Column(db.String(250),nullable=True)
    birth_year = db.Column(db.String(250),nullable=True)
    gender = db.Column(db.String(250),nullable=True)
    my_favorite = db.relationship('Favorite',backref='people',lazy=True)

    def __repr__(self):
        return f"El personaje {self.name} con ID: {self.id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
        }
    
class Favorite(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)
    people_id = db.Column(db.Integer,db.ForeignKey('people.id'),nullable = True)
    planet_id = db.Column(db.Integer,db.ForeignKey('planet.id'),nullable = True)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
            "user_id": self.user_id
        }