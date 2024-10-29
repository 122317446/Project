from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def Landing_Page():
    return render_template('LandingPage.html')

@app.route('/ProductSpread')
def Product_Spread():
    return render_template('ProductSpread.html')

if __name__ == "__main__":
    app.run(debug=True)