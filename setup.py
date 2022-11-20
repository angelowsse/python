from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

database_name = "API"
DB_URI = "mongodb+srv://LTPANGELOSSE:181661eG@ltpdb01.h7bqfoh.mongodb.net/API?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)

 
class Book(db.Document):
    book_id = db.IntField()
    name = db.StringField()
    author = db.StringField()
    description = db.StringField()

    def to_json(self):
        #converts this document to JSON
        return {
            "book_id": self.book_id,
            "name": self.name,
            "author": self.author,
            "description": self.description
        }

# Esta rota cria os livros dentro do db

@app.route('/api/db_populate', methods=['POST'])
def db_populate():
    book1 = Book(book_id=4, name="Harry Potter", author="J. K. Rowling", description="teste")
    book2 = Book(book_id=5, name="DOM QUIXOTE", author="Miguel de Cervantes", description="teste")
  

    book1.save()
    book2.save()
   
    return make_response("", 201)


# O METODO GET DESTE ENDPOINT MOSTRA A LISTA DE LIVROS DESTE ENDPOINT
# O METODO PUT DESTE ENDPOINT ADICIONA UM LIVRO AO DB    

@app.route('/api/books', methods=['GET','POST'])
def api_books():
    if request.method == "GET":
        books = []
        for book in Book.objects:
            books.append(book)
        return make_response(jsonify(books), 200)
    elif request.method == "POST":
        content = request.json
        book = Book(book_id=content['book_id'],
        name=content['name'],
        author=content['author'])
        book.save()
        return make_response("", 201)

        # GET RETORNA O LIVRO COM O ID CORRESPONDENTE
        # METODO PUT ATUALIZA O AUTOR E O NOME DO LIVRO COM O ID CORRESPONDENTE '{"name": "name", "author": "name"}'
        # DELETE DELETA O LIVRO COM O ID CORRESPONDENTE


@app.route('/api/books/<book_id>', methods=['GET','PUT','DELETE'])
def api_each_book(book_id):
    if request.method == "GET":
        book_obj = Book.objects(book_id=book_id).first()
        if book_obj:
            return make_response(jsonify(book_obj.to_json()),200)
        else:
            return make_response("",404)
    elif request.method == "PUT":
        content = request.json
        book_obj = Book.objects(book_id=book_id).first()
        book_obj.update(author=content['author'], name=content['name'])
        return make_response("",204)
    elif request.method == "DELETE":
        book_obj = Book.objects(book_id=book_id).first()
        book_obj.delete()
        make_response("",204)

if __name__ == '__main__':
    app.run()

