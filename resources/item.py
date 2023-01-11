from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item")
class Items(MethodView):
    @blp.response(200,ItemSchema(many=True))
    @jwt_required()
    def get(self):
        return ItemModel.query.all()
    
    
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    @jwt_required()
    def post(self,item_data):
        item=ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="an error occured while inserting an item.")
        return item

@blp.route("/item/<int:item_id>")
class Items_list(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        item=ItemModel.query.get_or_404(item_id)
        return item
        
    @jwt_required()
    def delete(self,item_id):
        item=ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"item deleted "}

    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    @jwt_required()
    def put(self,item_data,item_id):
        item=ItemModel.query.get_or_404(item_id)
        if item:
            item.name=item_data["name"]
            item.price=item_data["price"]
        else:
            new_item=ItemModel(id=item_id**item_data)
        db.session.add(item)
        db.commit() 
        return item