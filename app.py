from flask import Flask, render_template, abort, request, Response

app = Flask(__name__,
            static_url_path='',
            static_folder='frambu/static',
            template_folder='frambu/templates')


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
