
from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__)
app.secret_key = 'SPIDERS'

@app.route("/", methods=["GET"])
def home():
  return render_template("index.html")

@app.route("/api/calcTax", methods=["POST"])
def calcTax():
  if request.method == 'POST':
    data = request.get_json(silent=True)

    if not data or "a" not in data or "b" not in data or "c" not in data:
      return jsonify({"error1": "Income can not be blank"}), 400
    

    try:
      a = float(data["a"])
      b = float(data["b"])
      c = float(data["c"])

      session['empl'] = a
      session['savings'] = b
      session['bonus'] = c
      
    except (ValueError, TypeError):
      return jsonify({"error4": "All incomes must be numerical"}), 400
    
    return render_template('index.html')

@app.route('/confirm')
def confirm_page():
  print('confirm')
  return render_template("confirm.html")
  
@app.route("/api/saveTax", methods=["POST"])
def commit_sum():
  data = request.get_json(silent=True)
  
  try:
    a = float(data["a"])
    b = float(data["b"])
    c = float(data["c"])

    if a < 0 or b < 0 or c < 0:
      return jsonify({"error2": "Please provide positive income"}), 400
    savings_tax = 0
    if b < 1000:
      savings_tax = 15/100*(b-1000)
    if a < 25000:
      bonus_tax = 20/100*c
    elif 25000 < a < 50000:
      bonus_tax = 40/100*c
    else:
      bonus_tax = 45/100*c
      
    return jsonify({"taxIncome": 20/100*a, "taxSavings": savings_tax, "taxBonus": bonus_tax}), 200
  
  except (ValueError, TypeError):
    return jsonify({"error": "Error saving"}), 400


if __name__ == "__main__":
    app.run(debug=True)
