from flask import Blueprint, render_template

home_route = Blueprint('home', __name__)

@home_route.route('/home', methods=['GET'])
def home():
    return render_template('home.html')