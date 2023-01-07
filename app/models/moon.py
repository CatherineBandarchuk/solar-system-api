from app import db

class Moon(db.Model):
    #__tablename__ = "moon"
    #__tablename__ = "moon"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    size = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    #parent_id = Column(Integer, ForeignKey("parent_table.id"))
    planet = db.relationship("Planet", back_populates="moon")

    def to_dict(self):
        moon_as_dict = {}
        moon_as_dict["id"] = self.id
        moon_as_dict["name"] = self.name
        moon_as_dict["size"] = self.size
        moon_as_dict["description"] = self.description
        return moon_as_dict


    @classmethod
    def from_dict(cls,moon_data):
        new_moon = Moon(name=moon_data["name"],
                        size=moon_data["size"],
                        description=moon_data["description"])
        return new_moon