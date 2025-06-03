from flask import Blueprint, render_template, request
from .fuzzy_model import evaluar_riesgo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')  # nombre correcto

@main.route('/evaluar', methods=['POST'])
def evaluar():
    ingreso = float(request.form['ingreso'])
    deuda = float(request.form['deuda'])
    historial = float(request.form['historial'])

    resultado = evaluar_riesgo(ingreso, deuda, historial)
    return f'El riesgo crediticio es: {resultado}'
