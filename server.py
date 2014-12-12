from flask import Flask, request, render_template
from search_engine import SearchEngine
app = Flask(__name__)


def get_html(filename):
    return open(filename, 'r').read()


@app.route('/')
def main_page():
    return get_html('main_page.html')


@app.route('/search/')
def search():
    keyword = request.args.get('keyword', '')
    engine = SearchEngine()
    pages_searched = engine.search(keyword)
    return render_template(
        'results.html', keyword=keyword, pages_searched=pages_searched)


if __name__ == '__main__':
    app.run(debug=True)
