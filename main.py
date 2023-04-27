from flask import Flask,jsonify,request

from storage import all_articles, liked_articles, not_liked_articles
from demographic_filtering import output
from content_filtering import get_recommendations

app = Flask(__name__)

@app.route("/get-article")
def get_article():
    return jsonify({
        "data": all_articles[0],
        "status":"success"
    })

@app.route("/liked-article",methods="POST")
def liked_articles():
    articles=all_articles[0]
    all_articles=all_articles[1:]
    liked_articles.append(articles)
    return jsonify({
        "status":"success"
    }) ,201
    
@app.route("/unliked-article",methods="POST")
def unliked_articles():
    articles=all_articles[0]
    all_articles=all_articles[1:]
    unliked_articles.append(articles)
    return jsonify({
        "status":"success"
    }) ,201
    
@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "title": article[0],
            "total_events": article[1]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_articles in liked_articles:
        output = get_recommendations(liked_articles[1])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "total_events": recommended[1]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200


if __name__ == "__main__":
    app.run()