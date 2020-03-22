from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, DateTime
from flask_cors import CORS
import json 
import os
from datetime import datetime, timedelta
from sqlalchemy import desc

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
# Create the database tables.
db.create_all()s
ma = Marshmallow(app)
################################################## M O D E L S ##################################################

class Evento(db.Model): # Deve estar apenas na Plataforma
    __tablename__ = 'eventos'

    idEvento = db.Column(db.Integer, primary_key=True)
    nomeEvento = db.Column(db.String(80))
    localEvento = db.Column(db.String(30))
    horaInicioEvento = db.Column(db.String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    horaTerminoEvento = db.Column(db.String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    precoIngresso = db.Column(db.String(10))
    lines = db.relationship('Atracao', backref='eventos', lazy=True)


    def __init__(self, nomeEvento, localEvento, horaInicioEvento, horaTerminoEvento, precoIngresso, lines):
        self.nomeEvento = nomeEvento
        self.localEvento = localEvento
        self.horaInicioEvento = horaInicioEvento
        self.horaTerminoEvento = horaTerminoEvento
        self.precoIngresso = precoIngresso
        self.lines = lines

    def to_dict(self):
        response = {
            "idEvento": self.idEvento,
            "nomeEvento": self.nomeEvento,
            "localEvento": self.localEvento,
            "horaInicioEvento": self.horaInicioEvento,
            "horaTerminoEvento": self.horaTerminoEvento,
            "precoIngresso": self.precoIngresso,
            "lines": self.lines
        }
        return response


class Atracao(db.Model): # Deve ser apenas da Plataforma

    __tablename__ = 'atracoes'


    idAtracao = db.Column(db.Integer, primary_key=True)
    nomeAtracao = db.Column(db.String(80), unique=False)
    quantPessoas = db.Column(db.String(30), unique=False)
    tempoAtracao = db.Column(db.String(30), unique=False)
    vazaoAtracao = db.Column(db.String(30), unique=False)
    dataAtracao = db.Column(db.String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

 #   coluna = db.Column(db.Integer, )

#Column('person_id', Integer, ForeignKey(eventos.idEvento), primary_key=True)
    idEvento = db.Column(db.Integer, db.ForeignKey('eventos.idEvento'),nullable=False)
    waitingVisitors = db.relationship('Espera', backref='atracoes', lazy=True)

    cupons = db.relationship('Cupom', backref='atracoes', lazy=True)
    
    def __init__(self, nomeAtracao, quantPessoas, tempoAtracao, vazaoAtracao, dataAtracao, idEvento):
        self.nomeAtracao = nomeAtracao
        self.quantPessoas = quantPessoas
        self.tempoAtracao = tempoAtracao
        self.vazaoAtracao = vazaoAtracao
        self.dataAtracao = dataAtracao
        self.idEvento = idEvento
            
    def to_dict(self):
        response = {
            "idAtracao": self.idAtracao,
            "nomeAtracao": self.nomeAtracao,
            "quantPessoas": self.quantPessoas,
            "tempoAtracao": self.tempoAtracao,
            "vazaoAtracao": self.vazaoAtracao,
            "dataAtracao": self.dataAtracao,
            "eventId": self.idEvento,
            "waitingVisitors": self.waitingVisitors
        }
        return response

class Visitante(db.Model):
    __tablename__ = 'visitantes'

    idVisitante = db.Column(db.Integer, primary_key=True)
    nomeVisitante = db.Column(db.String(80))
    idAtracao = db.Column(db.Integer, db.ForeignKey('atracoes.idAtracao'))

    def __init__(self, nomeVisitante):
        self.nomeVisitante = nomeVisitante

    def to_dict(self):
        response = {
            "idVisitante": self.idVisitante,
            "nomeVisitante": self.nomeVisitante,
            "idAtracao": self.idAtracao
        }
        return response

class Espera(db.Model):
    __tablename__ = 'esperas'

    idEspera = db.Column(db.Integer, primary_key=True)

    idAtracao = db.Column(db.Integer, db.ForeignKey('atracoes.idAtracao'))
    idVisitante = db.Column(db.Integer, db.ForeignKey('visitantes.idVisitante'))

    horaEntrada = db.Column(db.String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    horaChamada = db.Column(db.String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    checkIn = db.Column(db.Boolean, default = False)


    def __init__(self, idAtracao, idVisitante, horaEntrada, horaChamada, checkIn):
        self.idAtracao = idAtracao
        self.idVisitante = idVisitante
        self.horaEntrada = horaEntrada
        self.horaChamada = horaChamada
        self.checkIn = checkIn

    def to_dict(self):
        response = {
            "idEspera": self.idEspera,
            "checkIn": self.checkIn,
            "idAtracao": self.idAtracao,
            "idVisitante": self.idVisitante,
            "horaChamada": self.idAtracao
        }
        return response

class Evento(db.Model): # Deve estar apenas na Plataforma
    __tablename__ = 'eventos'

    idEvento = db.Column(db.Integer, primary_key=True)
    nomeEvento = db.Column(db.String(80))
    localEvento = db.Column(db.String(30))
    horaInicioEvento = db.Column(db.String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    horaTerminoEvento = db.Column(db.String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    precoIngresso = db.Column(db.String(10))
    lines = db.relationship('Atracao', backref='eventos', lazy=True)


    def __init__(self, nomeEvento, localEvento, horaInicioEvento, horaTerminoEvento, precoIngresso, lines):
        self.nomeEvento = nomeEvento
        self.localEvento = localEvento
        self.horaInicioEvento = horaInicioEvento
        self.horaTerminoEvento = horaTerminoEvento
        self.precoIngresso = precoIngresso
        self.lines = lines

    def to_dict(self):
        response = {
            "idEvento": self.idEvento,
            "nomeEvento": self.nomeEvento,
            "localEvento": self.localEvento,
            "horaInicioEvento": self.horaInicioEvento,
            "horaTerminoEvento": self.horaTerminoEvento,
            "precoIngresso": self.precoIngresso,
            "lines": self.lines
        }
        return response


class Cupom(db.Model):
    idCupom = Column(Integer, primary_key=True)
    nomeCupom = db.Column(db.String(50), unique=False)
    descricao = db.Column(db.String(500), unique=False)
    quantidade = db.Column(db.String(50), unique=False)
    desconto = db.Column(db.String(3), unique=False)
    validade = db.Column(db.String(50), unique=False)#(DateTime, default=datetime.datetime.utcnow)

    idAtracao = db.Column(db.Integer, db.ForeignKey('atracoes.idAtracao'),nullable=False)
    

    def __init__(self, nomeCupom, descricao, quantidade, desconto, validade):
        self.nomeCupom = nomeCupom
        self.descricao = descricao
        self.quantidade = quantidade
        self.desconto = desconto
        self.validade = validade
    
    def toDict(self):
        response = {
            "idCupom": self.idCupom,
            "nomeCupom": self.nomeCupom,
            "descricao": self.descricao,
            "quantidade": self.quantidade,
            "desconto": self.desconto,
            "validade": self.validade
        }
        return response



################################################## S C H E M A ##################################################
class AtracaoSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('nomeAtracao', 'quantPessoas', 'tempoAtracao', 'vazaoAtracao', 'dataAtracao')
atracao_schema = AtracaoSchema()
atracaos_schema = AtracaoSchema(many=True)

class EventoSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('nomeEvento', 'localEvento', 'horaInicioEvento', 'horaTerminoEvento', 'precoIngresso', 'idEvento')
evento_schema = EventoSchema()
eventos_schema = EventoSchema(many=True)

class VisitanteSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('idVisitante', 'nomeVisitante')
visitante_schema = VisitanteSchema()
visitantes_schema = VisitanteSchema(many=True)

class EsperaSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('idAtracao', 'idVisitante', 'horaEntrada', 'horaChamada', 'checkIn')
espera_schema = EsperaSchema()
esperas_schema = EsperaSchema(many=True)

class CupomSchema(ma.Schema):
    class Meta:
        #Fields to expose
        fields = ('idCupom', 'nomeCupom', 'descricao', 'quantidade', 'desconto', 'validade', 'idAtracao')
cupom_schema = CupomSchema()
cupons_schema = CupomSchema(many=True)

################################################## R O U T E S ##################################################

# endpoint to create new event
@app.route("/evento", methods=["POST"])
def add_evento():

    nomeEvento= request.json['nomeEvento']
    localEvento = request.json['localEvento']
    horaInicioEvento = request.json['horaInicioEvento']
    horaTerminoEvento = request.json['horaTerminoEvento']
    precoIngresso = request.json['precoIngresso']
    lines = []
    new_evento = Evento(nomeEvento, localEvento, horaInicioEvento, horaTerminoEvento, precoIngresso, lines)
    db.session.add(new_evento)
    db.session.commit()
    response = new_evento.to_dict()
    return response 

# endpoint to get event detail by id
@app.route("/evento/<id>", methods=["GET"])
def evento_detail(id):
    evento = Evento.query.get(id)
    response = evento.to_dict()
    return response 

# endpoint to get my events
@app.route("/evento/meus_eventos/<idVisitante>", methods=["GET"])
def get_my_events(idVisitante):
    all_eventos = Evento.query.all()
    dict_result = {}
    for entry in all_eventos:
        event_dict = entry.to_dict()
        dict_result[event_dict['idEvento']] = event_dict
    return json.loads(json.dumps(dict_result))


# endpoint to create new line
@app.route("/atracao", methods=["POST"])
def add_atracao():
    nomeAtracao = request.json['nomeAtracao']
    quantPessoas = request.json['quantPessoas']
    tempoAtracao = request.json['tempoAtracao']
    vazaoAtracao = request.json['vazaoAtracao']
    dataAtracao = request.json['dataAtracao']
    idEvento = request.json['idEvento']
    
    new_atracao = Atracao( nomeAtracao, quantPessoas, tempoAtracao, vazaoAtracao, dataAtracao, idEvento)
    db.session.add(new_atracao)
    db.session.commit()
    response = new_atracao.to_dict()
    return response 

# endpoint to get attraction detail by id
@app.route("/atracao/<id>", methods=["GET"])
def atracao_detail(id):
    atracao = Atracao.query.get(id)
    response = atracao.to_dict()
    return response 

    
# endpoint to show all lines in an event
@app.route("/atracao_por_evento/<idEvento>", methods=["GET"])
def get_atracao_by_event(idEvento):
    all_atracoes = Atracao.query.filter_by(idEvento = idEvento).all()
    dict_result = {}
    return json.loads(json.dumps(all_atracoes))

# endpoint to update attraction
@app.route("/atracao/<id>", methods=["PUT"])
def atracao_update(id):
    atracao = Atracao.query.get(id)
    if 'nomeAtracao' in request.json.keys():
        atracao.nomeAtracao = request.json['nomeAtracao']
    if 'quantPessoas' in request.json.keys():
        atracao.quantPessoas = request.json['quantPessoas']
    if 'tempoAtracao' in request.json.keys():
        atracao.tempoAtracao = request.json['tempoAtracao']
    if 'vazaoAtracao' in request.json.keys():
        atracao.vazaoAtracao = request.json['vazaoAtracao']
    if 'dataAtracao' in request.json.keys():
        atracao.dataAtracao = request.json['dataAtracao']  
    db.session.commit()
    return atracao_schema.jsonify(atracao)


# endpoint to delete attraction
@app.route("/atracao/<id>", methods=["DELETE"])
def user_delete(id):
    atracao = Atracao.query.get(id)
    db.session.delete(atracao)
    db.session.commit()
    return atracao_schema.jsonify(atracao)

# endpoint to get visitor detail by id
@app.route("/visitante/<id>", methods=["GET"])
def visitante_detail(id):
    visitante = Visitante.query.get(id)
    response = visitante.to_dict()
    return response 


# endpoint to create new visitor
@app.route("/visitante", methods=["POST"])
def add_visitante():

    nomeVisitante= request.json['nomeVisitante']

    new_visitante = Visitante(nomeVisitante)
    db.session.add(new_visitante)
    db.session.commit()
    response = new_visitante.to_dict()
    return response


#TEST ENDPOINT  get all waits
@app.route("/espera", methods=["GET"])
def get_esperas():
    all_esperas = Espera.query.all()
    dict_result = {}
    for entry in all_esperas:
        espera_dict = entry.to_dict()
        dict_result[espera_dict['idEspera']] = espera_dict
    return json.loads(json.dumps(dict_result))

# endpoint to create new wait
@app.route("/espera/esperar_em_atracao", methods=["POST"])
def add_espera():
    
    hora = datetime.now()

    checkIn = False
    idAtracao = request.json['idAtracao']
    visitanteId = request.json['idVisitante']
    horaEntrada = hora.strftime("%Y-%m-%d %H:%M:%S:%f")

    #TODO pegar tempo de espera da atracao com id = idAtracao
    waitMin = 10
    horaChamada = hora + timedelta(minutes=waitMin)
    
    #Find if user is waiting in a line
    espera = Espera.query.filter_by(idVisitante = visitanteId).order_by(Espera.idEspera.desc()).first()
    
    #If he is still in line (espera exists AND espera.checkIn == false), return error
    if espera is None:
        new_espera = Espera(idAtracao, visitanteId, horaEntrada, horaChamada, checkIn)
        db.session.add(new_espera)
        db.session.commit()
        response = new_espera.to_dict()
        return response
    else:
        if espera.checkIn:
            new_espera = Espera(idAtracao, visitanteId, horaEntrada, horaChamada, checkIn)
            db.session.add(new_espera)
            db.session.commit()
            response = new_espera.to_dict()
            return response
        if espera.idAtracao == idAtracao:
            return 'Ops! Você já está esperando nesta fila :)', 400
        else:
            return 'Ops! Você já está esperando em uma fila. Saia dela primeiro, e depois venha para esta :)', 400

#endpoint to cancel wait
@app.route("/espera/cancelar_espera", methods=["POST"])
def espera_delete():

    idAtracao = request.json['idAtracao']
    visitanteId = request.json['idVisitante']

    espera = Espera.query.filter_by(idVisitante = visitanteId).order_by(Espera.idEspera.desc()).first()
    if espera is None:
        return 'Você não estava esperando em nenhuma fila!', 400
    else:
        if espera.idAtracao == idAtracao and not espera.checkIn:
            #Cancelling the right attraction
            db.session.delete(espera)
            db.session.commit()
            return espera_schema.jsonify(espera)
        else:
            return "Você não estava esperando nesta fila...", 400

#endpoint to check-in a visitor on an attraction
@app.route("/espera/check_in", methods=["PUT"])
def espera_check_in():

    idAtracao = request.json['idAtracao']
    visitanteId = request.json['idVisitante']

    #get the last line that the visitor is
    espera = Espera.query.filter_by(idVisitante = visitanteId).order_by(Espera.idEspera.desc()).first()    
    if espera is None:
        return 'Visitante não está em nenhuma fila', 400
    else:
        if espera.checkIn:
            return 'Visitante não está em nenhuma fila ativa', 400
        else:
            if idAtracao == espera.idAtracao:
                espera.checkIn = True
                db.session.commit()
                return espera_schema.jsonify(espera)
            else: 'Visitante está em outra fila!', 400

# endpoint to distribute a coupon
@app.route("/cupom/distribuir_cupom", methods=["POST"])
def distribuir_cupom():

    nomeCupom = request.json['nomeCupom']
    descricaoCupom = request.json["descricao"]
    quantidade = request.json["quantidade"]
    desconto = request.json["desconto"]
    validade = request.json["validade"]
    idAtracao = request.json["idAtracao"]

    new_cupom = Cupom(nomeCupom, descricao, quantidade, desconto, validade, idAtracao)
    db.session.add(new_cupom)
    bd.session.commit()
    response = new_cupom.toDict()
    return response


# endpoint to get valid coupons detail by attraction id
@app.route("/cupom/<idAtracao>", methods=["GET"])
def visitante_detail(idAtracao):
    cupons = Cupom.query.filter_by(idAtracao = idAtracao).filter_by(datetime.now().strftime("%Y-%m-%d %H:%M:%S") < validade)

    dict_result = {}
    for entry in cupons:
        cupom_dict = entry.to_dict()
        dict_result[cupom_dict['idCupom']] = cupom_dict
    return json.loads(json.dumps(dict_result))

############################################################################################################
if __name__ == '__main__':
    app.run(debug=True)