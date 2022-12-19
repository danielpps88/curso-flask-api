from flask import jsonify, make_response, request
from flask_restful import Resource

from apicursos import api

from ..entidades import formacao
from ..schemas import formacao_schema
from ..services import formacao_services


class FormacaoList(Resource):
    def get(self):
        formacoes = formacao_services.listar_formacao()
        fs = formacao_schema.FormacaoSchema(many=True)
        return make_response(fs.jsonify(formacoes), 200)
        

    def post(self):
        fs = formacao_schema.FormacaoSchema()
        validate = fs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            professores = request.json["professores"]
            
            novo_formacao = formacao.Formacao(nome=nome, descricao=descricao, professores=professores)
            resultado = formacao_services.cadastrar_formacao(novo_formacao)
            x = fs.jsonify(resultado)
            return make_response(x, 200)

class FormacaoDetail(Resource):
    def get(self, id):
        formacao_bd = formacao_services.listar_formacao_id(id)
        if formacao_services is None:
            return make_response(jsonify("Formacao não encontrado"), 404)
        cs = formacao_schema.FormacaoSchema()
        return make_response(cs.jsonify(formacao_services), 200)



    def put(self, id):
        formacao_bd = formacao_services.listar_formacao_id(id)
        if formacao_bd is None:
            return make_response(jsonify("Formacao não encontrado"), 404)
        fs = formacao_schema.FormacaoSchema()
        validate = fs.validate(request.json)

        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            professores = request.json["professores"]

            novo_formacao = formacao.Formacao(nome=nome, descricao=descricao, professores=professores)
            formacao_services.atualiza_formacao(formacao_bd, novo_formacao)
            formacao_atualizado = formacao_services.listar_formacao_id(id)
            return make_response(fs.jsonify(formacao_atualizado), 200)
    
    def delete(self, id):
        formacao_bd = formacao_services.listar_formacao_id(id)
        
        if formacao_bd is None:
            return make_response(jsonify("Formacao não encontrado"), 404)
        formacao_services.remove_formacao(formacao_bd)
        return make_response(jsonify("Formacao excluido com sucesso"), 200)





api.add_resource(FormacaoList, '/formacao')
api.add_resource(FormacaoDetail, '/formacao/<int:id>')