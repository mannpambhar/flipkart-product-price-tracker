from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from scraper import fetch_product_details
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    current_price = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    rating = db.Column(db.String(10), nullable=True)
    reviews = db.Column(db.Text, nullable=True)  # New field for reviews
    total_purchases = db.Column(db.String(50), nullable=True)  # New field for total purchases
    price_history = db.relationship('PriceHistory', backref='product', lazy=True)

class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    products = Product.query.all()  # Fetch all products for display
    if request.method == 'POST':
        product_url = request.form.get('url')
        product_details = fetch_product_details(product_url)

        if product_details and 'current_price' in product_details:
            product = Product.query.filter_by(url=product_url).first()
            if not product:
                product = Product(
                    url=product_url,
                    title=product_details.get('title', 'N/A'),
                    current_price=product_details.get('current_price', 'N/A'),
                    description=product_details.get('description', 'N/A'),
                    rating=product_details.get('rating', 'N/A'),
                    reviews=product_details.get('reviews', 'N/A'),  # New field
                    total_purchases=product_details.get('total_purchases', 'N/A')  # New field
                )
                db.session.add(product)
                db.session.commit()

                price_history_entry = PriceHistory(price=product.current_price, product=product)
                db.session.add(price_history_entry)
                db.session.commit()
            else:
                product.current_price = product_details.get('current_price', 'N/A')
                price_history_entry = PriceHistory(price=product.current_price, product=product)
                db.session.add(price_history_entry)
                db.session.commit()

            price_history = PriceHistory.query.filter_by(product_id=product.id).all()
            return render_template('index.html', product=product, price_history=price_history, products=products)
        else:
            return render_template('index.html', error="Could not fetch product price details", products=products)

    return render_template('index.html', products=products)

@app.route('/recheck/<int:product_id>', methods=['POST'])
def recheck_price(product_id):
    product = Product.query.get_or_404(product_id)
    product_details = fetch_product_details(product.url)

    if product_details and 'current_price' in product_details:
        product.current_price = product_details.get('current_price', 'N/A')
        price_history_entry = PriceHistory(price=product.current_price, product=product)
        db.session.add(price_history_entry)
        db.session.commit()

    price_history = PriceHistory.query.filter_by(product_id=product.id).all()
    return render_template('index.html', product=product, price_history=price_history, products=Product.query.all())

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    products = Product.query.filter(Product.title.contains(query)).all()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
