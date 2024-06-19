from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contraseña_hash = db.Column(db.String(255), nullable=False)  # Aquí se utiliza contraseña_hash en vez de contraseña
    fechaNacimiento = db.Column(db.Date, nullable=False)
    pais = db.Column(db.String(100), nullable=False)  # Ajustado a String(100) según tu diseño
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Usuario %r>' % self.nombre

    def set_password(self, password):
        self.contraseña_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contraseña_hash, password)
