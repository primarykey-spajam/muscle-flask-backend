from flask import Flask, request, jsonify
import feedparser
import parser as parser
import news as news

app = Flask(__name__, static_folder='music')

@app.route("/news")
def get_url():
    category = request.args.get('category')

    file_name = news.main(category)
    return jsonify(ResultSet="http://localhost:80/" + file_name)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)

