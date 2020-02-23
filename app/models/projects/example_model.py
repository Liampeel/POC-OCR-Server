from app.models.projects.project_base import ProjectBase
from app import db_mongo as db


class ExampleModel(ProjectBase):
    """Document definition for the example project."""
    ml_toothed = db.BooleanField(required=True)
    ml_breathes = db.BooleanField(required=True)
    ml_legs = db.BooleanField(required=True)

    t_species = db.StringField(default="")
    l_actual_species = db.StringField(default="")
