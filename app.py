from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/aloevera')
# def aloevera():
#     return render_template('aloevera.html')


# @app.route('/chamomile')
# def chamomile():
#     return render_template('chamomile.html')


# @app.route('/fenugreek')
# def fenugreek():
#     return render_template('fenugreek.html')


# @app.route('/stevia')
# def stevia():
#     return render_template('stevia.html')


# @app.route('/tulsi')
# def tulsi():
#     return render_template('tulsi.html')


# Route for all pages instead of hardcoding : dynamic routing...

@app.route('/plants/<plant_name>')
def plant_page(plant_name):
    try:
        return render_template(f'{plant_name}.html')
    except:
        return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
