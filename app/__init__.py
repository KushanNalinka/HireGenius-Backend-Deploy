# from flask import Flask
# from flask_cors import CORS
# from pymongo import MongoClient
# import os

# # Initialize shared components
# client = None
# db = None

# def download_model():
#     url = "https://drive.google.com/file/d/1xGKKIC4bAHoiphw7KDzPFN4yHViYqDkW/view?usp=drive_link"  # Replace with your cloud file link
#     output_path = "local_model/model.safetensors"
#     if not os.path.exists(output_path):  # Download only if the file is missing
#         print("Downloading model file...")
#         response = requests.get(url)
#         with open(output_path, "wb") as file:
#             file.write(response.content)
#         print("Download complete.")


# def create_app():
#     global client, db

#     # Download the model
#     download_model()

#     # Initialize Flask app
#     app = Flask(__name__)
#     CORS(app, resources={r"/*": {"origins": "*"}})

#     # MongoDB connection
#     client = MongoClient("mongodb+srv://Kushan:Kus12NG*MDB@cluster0.vssd7k3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#     db = client['ResumeProjectDB']

#     # Register Blueprints
#     from app.routes.job_routes import job_routes
#     from app.routes.candidate_routes import candidate_routes

#     app.register_blueprint(job_routes)
#     app.register_blueprint(candidate_routes)

#     return app

# import os
# from flask import Flask
# from flask_cors import CORS
# from pymongo import MongoClient

# # shared db object
# client = None
# db     = None

# def create_app():
#     global client, db

#     # 1) Flask + CORS
#     app = Flask(__name__)
#     CORS(app, resources={r"/*": {"origins": "*"}})

#     # 2) MongoDB: use the URL from the environment
#     mongo_url = os.environ.get("MONGO_URL")
#     client    = MongoClient(mongo_url)
#     db        = client["ResumeProjectDB"]

#     # 3) Register your routes
#     from app.routes.job_routes       import job_routes
#     from app.routes.candidate_routes import candidate_routes

#     app.register_blueprint(job_routes)
#     app.register_blueprint(candidate_routes)

#     return app

import os
from flask import Flask, request
from flask_cors import CORS
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from pathlib import Path
from dotenv import load_dotenv

# ─── load MiniLM once ───
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ---------- load .env when running locally ----------
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path, override=False)   # ignored if the file is absent

# shared DB handle
client = None
db     = None

def create_app():
    global client, db
    app = Flask(__name__)
    CORS(app)

    # connect to Mongo using the secret
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI not set. Add it to .env (local) "
                           "or pass it as an environment variable in production.")

    client = MongoClient(mongo_uri)
    db     = client["ResearchProjectNewDB"]

    # example MiniLM route:
    @app.route("/encode", methods=["POST"])
    def encode():
        text = request.json["text"]
        vec  = model.encode(text).tolist()
        return {"embedding": vec}

    # register your existing blueprints
    from app.routes.job_routes       import job_routes
    from app.routes.candidate_routes import candidate_routes
    app.register_blueprint(job_routes)
    app.register_blueprint(candidate_routes)

    return app
#new uoncommented code
