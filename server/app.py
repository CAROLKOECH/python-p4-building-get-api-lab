from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_migrate import Migrate
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your models
class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    # Define the relationship to BakedGood
    baked_goods = db.relationship('BakedGood', backref='bakery', lazy=True)

class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'), nullable=False)

# Define routes
@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    return jsonify([b.serialize() for b in bakeries])

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery is None:
        return jsonify({"error": "Bakery not found"}), 404
    return jsonify(bakery.serialize())

@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
    return jsonify([bg.serialize() for bg in baked_goods])

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(desc(BakedGood.price)).first()
    if baked_good is None:
        return jsonify({"error": "No baked goods found"}), 404
    return jsonify(baked_good.serialize())

if __name__ == '__main__':
    app.run(port=5555, debug=True)
