from flask import Blueprint, render_template, request

bp = Blueprint('main', __name__)

# Algoritmo de Luhn para validar o cartão
def validate_card(card_number):
    digits = [int(d) for d in card_number if d.isdigit()]
    checksum = 0
    is_second = False

    for digit in reversed(digits):
        if is_second:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
        is_second = not is_second

    return checksum % 10 == 0

@bp.route("/", methods=["GET", "POST"])
def index():
    validation_result = None
    card_number = ""

    if request.method == "POST":
        card_number = request.form.get("card_number")
        if card_number:
            validation_result = validate_card(card_number)

    return render_template("index.html", result=validation_result, card_number=card_number)
