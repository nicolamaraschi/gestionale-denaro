from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Imposta il percorso del database
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "instance/finance.db")}'
db = SQLAlchemy(app)

# Modello di database per le spese
class Spese(db.Model):
    __tablename__ = 'Spese'  # Specifica il nome della tabella
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    importo = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Spesa {self.categoria}: {self.importo}€>'

# Modello di database per lo stipendio
class Stipendi(db.Model):
    __tablename__ = 'Stipendi'  # Specifica il nome della tabella
    id = db.Column(db.Integer, primary_key=True)
    importo = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Stipendio {self.importo}€>'

# Route per aggiungere una spesa
@app.route('/add_spesa', methods=['POST'])
def add_spesa():
    data = request.json
    nuova_spesa = Spese(categoria=data['categoria'], importo=data['importo'])
    db.session.add(nuova_spesa)
    db.session.commit()
    return jsonify({'message': 'Spesa aggiunta con successo'})

# Route per aggiungere lo stipendio
@app.route('/add_stipendio', methods=['POST'])
def add_stipendio():
    data = request.json
    nuovo_stipendio = Stipendi(importo=data['importo'])
    db.session.add(nuovo_stipendio)
    db.session.commit()
    return jsonify({'message': 'Stipendio aggiunto con successo'})

# Route per ottenere le spese per categoria
@app.route('/get_spese_categorie', methods=['GET'])
def get_spese_categorie():
    spese = db.session.query(Spese.categoria, db.func.sum(Spese.importo)).group_by(Spese.categoria).all()
    spese_categorie = {categoria: importo for categoria, importo in spese}
    return jsonify(spese_categorie)

# Route per ottenere lo storico delle spese mensili
@app.route('/get_storico_mensile', methods=['GET'])
def get_storico_mensile():
    spese = db.session.query(db.func.strftime('%Y-%m', Spese.data), db.func.sum(Spese.importo)).group_by(db.func.strftime('%Y-%m', Spese.data)).all()
    storico_mensile = {mese: importo for mese, importo in spese}
    return jsonify(storico_mensile)

if __name__ == '__main__':
    app.run(debug=True)
