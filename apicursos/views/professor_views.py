from flask import jsonify, make_response, request
from flask_restful import Resource

from apicursos import api

from ..entidades import professor
from ..schemas import professor_schema
from ..services import professor_services

class ProfessorList(Resource):
    def get(self):
        professores = professor_services.listar_professor()
        ps = professor_schema.ProfessorSchema(many=True)
        return make_response(ps.jsonify(professores), 200)        

    def post(self):
        ps = professor_schema.ProfessorSchema()
        validate = ps.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            idade = request.json["idade"]
            
            novo_professor = professor.Professor(nome=nome, idade=idade)
            resultado = professor_services.cadastrar_professor(novo_professor)
            x = ps.jsonify(resultado)
            return make_response(x, 200)

class ProfessorDetail(Resource):
    def get(self, id):
        professor_bd = professor_services.listar_professor_id(id)
        if professor_services is None:
            return make_response(jsonify("Professor não encontrado"), 404)
        ps = professor_schema.ProfessorSchema()
        return make_response(ps.jsonify(professor_services), 200)

    def put(self, id):
        professor_bd = professor_services.listar_professor_id(id)
        if professor_bd is None:
            return make_response(jsonify("Professor não encontrado"), 404)
        fs = professor_schema.ProfessorSchema()
        validate = fs.validate(request.json)

        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            idade = request.json["idade"]
            novo_professor = professor.Professor(nome=nome, idade=idade)
            professor_services.atualiza_professor(professor_bd, novo_professor)
            professor_atualizado = professor_services.listar_professor_id(id)
            return make_response(fs.jsonify(professor_atualizado), 200)
    
    def delete(self, id):
        professor_bd = professor_services.listar_professor_id(id)
        
        if professor_bd is None:
            return make_response(jsonify("Professor não encontrado"), 404)
        professor_services.remove_professor(professor_bd)
        return make_response(jsonify("Professor excluido com sucesso"), 200)

api.add_resource(ProfessorList, '/professor')
api.add_resource(ProfessorDetail, '/professor/<int:id>')

