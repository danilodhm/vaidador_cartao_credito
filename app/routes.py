import re
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
    

def get_card_brand(card_number):
    """
    Identifica a bandeira do cartão com base nos prefixos (BIN) usando regex.
    """
    patterns = {
        "Visa": r"^4\d{12}(\d{3})?$",  # Começa com 4, 13 ou 16 dígitos
        "MasterCard": r"^(5[1-5]\d{14}|2(2[2-9]|[3-6][0-9]|7[01]|720)\d{12})$",  # 51-55 ou 2221-2720
        "American Express": r"^3[47]\d{13}$",  # Começa com 34 ou 37, 15 dígitos
        "Diners Club": r"^(3(0[0-5]|[68]\d)\d{11})$",  # 300-305, 36, 38, 14 dígitos
        "Discover": r"^(6011\d{12}|65\d{14}|64[4-9]\d{13}|622(12[6-9]|1[3-9]\d|[2-8]\d{2}|9[0-2]\d|92[0-5])\d{10})$",  # Vários intervalos
        "JCB": r"^(352[8-9]\d{12}|35[3-8]\d{13})$",  # 3528-3589
        "enRoute": r"^(2014|2149)\d{11}$",  # 2014, 2149, 15 dígitos
        "Voyager": r"^8699\d{11}$",  # 8699
        "Hipercard": r"^(38\d{17}|60\d{14})$",  # 38 ou 60, longos
        "Aura": r"^50\d{14}$"  # Começa com 50, 16 dígitos
    }

    for brand, pattern in patterns.items():
        if re.match(pattern, card_number):
            return brand

    return "Unknown"



@bp.route("/", methods=["GET", "POST"])
def index():
    validation_result = None
    card_number = ""
    card_brand = "Unknown"

    if request.method == "POST":
        card_number = request.form.get("card_number")
        if card_number:
            validation_result = validate_card(card_number)
            card_brand = get_card_brand(card_number)

    return render_template("index.html", result=validation_result, brand=card_brand, card_number=card_number)

