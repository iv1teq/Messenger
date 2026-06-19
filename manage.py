from app.settings import app , socket





if __name__ == '__main__':
    socket.run(app = app, debug = True, host='0.0.0.0', port=8080)