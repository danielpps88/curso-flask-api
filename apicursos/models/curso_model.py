from apicursos import db
from .formacao_model import Formacao

class Curso(db.Model):
    __tablename__ = "curso"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(150), nullable=False)
    data_publicacao = db.Column(db.Date, nullable=False)

    formacao_id = db.Column(db.Integer, db.ForeignKey("formacao.id"))
    formacao = db.relationship(Formacao, backref=db.backref("cursos", lazy="dynamic"))
