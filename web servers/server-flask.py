from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_get():
    return "Salut!", 200

@app.route('/', methods=['POST'])
def handle_post():
    try:
        data = request.get_json(force=True)
        nume = data.get('nume', '')
    except:
        nume = 'eroare'
    
    return f"Salut, {nume}!", 200

if __name__ == '__main__':
    app.run(port=8080)
