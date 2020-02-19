from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from movie_service import MovieService

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return ''
    
@app.route('/current_running_movie')
def current_running_movie_get(): 
    movie_service = MovieService()
    response = movie_service.current_running_movie_get()

    return jsonify(response)
    
@app.route('/premovie')
def premovie_get(): 
    movie_service = MovieService()
    response = movie_service.premovie_get()

    return jsonify(response)

@app.route('/movie_story')
def movie_story_get():
    code = request.args.get('code')

    if code is None: return "fail"

    movie_service = MovieService()
    response = movie_service.story_get(code)

    return jsonify(response)

@app.route('/movie_actor')
def movie_actor_get():
    code = request.args.get('code')

    if code is None: return "fail"

    movie_service = MovieService()
    response = movie_service.actor_get(code)

    return jsonify(response)

@app.route('/movie_director')
def movie_director_get():
    code = request.args.get('code')

    if code is None: return "fail"

    movie_service = MovieService()
    response = movie_service.director_get(code)

    return jsonify(response)

@app.route('/movie_photo_last_paging_number')
def movie_photo_last_paging_number_get():
    code = request.args.get('code')

    if code is None: return "fail"

    movie_service = MovieService()
    response = movie_service.photo_last_paging_number_get(code)

    return jsonify(response)

@app.route('/movie_photo')
def movie_photo_get():
    code = request.args.get('code')
    page = request.args.get('page')

    if code is None: return "fail"
    if page is None: return "fail"

    movie_service = MovieService()
    response = movie_service.photo_get(code, page)

    return jsonify(response)

@app.route('/movie_video_trailer')
def movie_video_trailer_get():
    code = request.args.get('code')

    if code is None: return "fail"

    movie_service = MovieService()
    response = movie_service.video_trailer_get(code)

    return jsonify(response)

@app.route('/movie_video_making')
def movie_video_making_get():
    code = request.args.get('code')

    if code is None: return "fail"

    movie_service = MovieService()
    response = movie_service.video_making_get(code)

    return jsonify(response)

@app.route('/movie_video_talk')
def movie_video_talk_get():
    code = request.args.get('code')

    if code is None: return "fail"

    movie_service = MovieService()
    response = movie_service.video_talk_get(code)

    return jsonify(response)

@app.route('/movie_video_link')
def movie_video_link_get():
    code = request.args.get('code')
    media = request.args.get('media')

    if code is None: return "fail"
    if media is None: return "fail"

    movie_service = MovieService()
    response = movie_service.video_link_get(code, media)

    return jsonify(response)
    

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 