from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import Book, Cart
import sys

# Python 3.13+ compatibility fix for sys.getframe
# This fixes AttributeError: module 'sys' has no attribute 'getframe'
if not hasattr(sys, 'getframe') and hasattr(sys, '_getframe'):
    sys.getframe = sys._getframe

app = Flask(__name__)
app.secret_key = 'your_secret_key'   # Required for session management


# Create a cart instance to manage the cart
cart = Cart()

# Create a global books list to avoid duplication
BOOKS = [
    Book("The Great Gatsby", "Fiction", 10.99, "/static/images/books/the_great_gatsby.jpg"),
    Book("1984", "Dystopia", 8.99, "/static/images/books/1984.jpg"),
    Book("I Ching", "Traditional", 18.99, "/static/images/books/I-Ching.jpg"),
    Book("Moby Dick", "Adventure", 12.49, "/static/images/books/moby_dick.jpg")
]

def get_book_by_title(title):
    """Helper function to find a book by title"""
    return next((book for book in BOOKS if book.title == title), None)


def get_books_by_category(category):
    """Helper function to find books by category"""
    if not category:
        return BOOKS
    return [book for book in BOOKS if book.category.lower() == category.lower()]


def get_all_categories():
    """Helper function to get all unique categories"""
    return list(set(book.category for book in BOOKS))


@app.route('/')
def index():
    return render_template('index.html', books=BOOKS, cart=cart)


@app.route('/category/<category_name>')
def browse_by_category(category_name):
    """Route to browse books by category"""
    books_in_category = get_books_by_category(category_name)
    
    if not books_in_category:
        flash(f'No books found in category "{category_name}"!', 'info')
        return redirect(url_for('index'))
    
    categories = get_all_categories()
    return render_template('index.html', books=books_in_category, cart=cart, 
                         current_category=category_name, categories=categories)


@app.route('/categories')
def list_categories():
    """Route to list all available categories"""
    categories = get_all_categories()
    category_counts = {}
    for category in categories:
        category_counts[category] = len(get_books_by_category(category))
    
    return render_template('categories.html', categories=category_counts, cart=cart)


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    book_title = request.form.get('title')
    
    # Get quantity with more robust validation
    quantity_str = request.form.get('quantity', '1')
    
    # Handle None, empty string, or whitespace-only strings
    if not quantity_str or not quantity_str.strip():
        quantity_str = '1'
    
    try:
        # Strip whitespace and validate
        quantity_str = quantity_str.strip()
        
        # Check for decimal values which would cause invalid literal error
        if '.' in quantity_str:
            flash('Quantity must be a whole number!', 'error')
            return redirect(url_for('index'))
        
        quantity = 1
    except (ValueError, TypeError) as e:
        flash('Invalid quantity! Please enter a valid whole number.', 'error')
        return redirect(url_for('index'))
    
    if quantity < 1:
        flash('Quantity must be at least 1!', 'error')
        return redirect(url_for('index'))

    book = get_book_by_title(book_title)
    
    if book:
        cart.add_book(book, quantity)
        flash(f'Added {quantity} "{book.title}" to cart!', 'success')
    else:
        flash('Book not found!', 'error')

    return redirect(url_for('index'))


@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    book_title = request.form.get('title')
    cart.remove_book(book_title)
    flash(f'Removed "{book_title}" from cart!', 'success')
    return redirect(url_for('view_cart'))


@app.route('/update-cart', methods=['POST'])
def update_cart():
    """
    Update the quantity of a book in the cart.
    This function handles HTTP POST requests to update the quantity of a book in the user's cart.
    If the quantity is set to 0 or less, the book is effectively removed from the cart.
    Args:
        None (uses form data from the request)
    Returns:
        Response: Redirects to the view_cart page after updating the cart.
    Form Parameters:
        title (str): The title of the book to update.
        quantity (int): The new quantity of the book. Defaults to 1.
    Flash Messages:
        - Confirmation of removal if quantity <= 0
        - Confirmation of update otherwise
    """
    book_title = request.form.get('title')
    
    # Get quantity with more robust validation
    quantity_str = request.form.get('quantity', '1')
    
    # Handle None, empty string, or whitespace-only strings
    if not quantity_str or not quantity_str.strip():
        quantity_str = '1'
    
    try:
        # Strip whitespace and validate
        quantity_str = quantity_str.strip()
        
        # Check for decimal values which would cause invalid literal error
        if '.' in quantity_str:
            flash('Quantity must be a whole number!', 'error')
            return redirect(url_for('view_cart'))
        
        # Convert to integer
        quantity = int(quantity_str)
    except (ValueError, TypeError) as e:
        flash('Invalid quantity! Please enter a valid whole number.', 'error')
        return redirect(url_for('view_cart'))
    
    cart.update_quantity(book_title, quantity)
    
    if quantity <= 0:
        flash(f'Removed "{book_title}" from cart!', 'success')
    else:
        flash(f'Updated "{book_title}" quantity to {quantity}!', 'success')
    
    return redirect(url_for('view_cart'))


@app.route('/cart')
def view_cart():
    return render_template('cart.html', cart=cart)


@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    cart.clear()
    flash('Cart cleared!', 'success')
    return redirect(url_for('view_cart'))


@app.route('/checkout')
def checkout():
    if cart.is_empty():
        flash('Your cart is empty!', 'error')
        return redirect(url_for('index'))
    
    total_price = cart.get_total_price()
    return render_template('checkout.html', cart=cart, total_price=total_price)


if __name__ == '__main__':
    app.run(debug=True)