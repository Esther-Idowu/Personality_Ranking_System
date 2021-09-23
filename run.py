from app import app
if __name__ == "__main__":
    app.run(debug =True)
    app.config['TEMPLATES_AUTO_RELOAD']
    #model = pickle.load(open("model.pkl", "rb"))

