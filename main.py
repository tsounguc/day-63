from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import INTEGER, VARCHAR, FLOAT
from sqlalchemy.orm import Mapped, mapped_column

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

# create the extension
db = SQLAlchemy()

# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

# initialize the app with the extension
db.init_app(app)


class Books(db.Model):
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR, unique=True, nullable=False)
    author: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    review: Mapped[float] = mapped_column(FLOAT, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books = []
    result = db.session.execute(db.select(Books).order_by(Books.title))
    books = result.scalars().all()
    for book in books:
        b = {
            "title": book.title,
            "author": book.author,
            "rating": book.review,
        }
        all_books.append(b)

    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book = {
            "title": request.form['name'],
            "author": request.form['author'],
            "rating": request.form['rating'],
        }
        # print(book)
        book_to_add = Books(title=book['title'], author=book['author'], review=book['rating'])
        db.session.add(book_to_add)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)
