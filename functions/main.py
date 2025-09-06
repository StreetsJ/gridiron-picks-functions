# functions/main.py
from firebase_functions import https_fn
from firebase_admin import initialize_app
from google.cloud import secretmanager

# Initialize the Firebase Admin SDK if you need to interact with other Firebase services
# like Firestore, Authentication, etc.
initialize_app()

@https_fn.on_request()
def helloWorld(req: https_fn.Request) -> https_fn.Response:
    """
    A simple HTTP-triggered function that responds with 'Hello from Firebase!'
    You can access this function via its URL after deployment.
    """

    games = get_games_from_api(1)

    return https_fn.Response("Hello from Firebase " + str(games))

# You can also add other types of functions here, e.g., Firestore triggers
# from firebase_functions import firestore_fn
#
# @firestore_fn.on_document_created(document="users/{userId}")
# def newUserAdded(event: firestore_fn.Event[firestore_fn.DocumentSnapshot]) -> None:
#    print(f"New user created: {event.data.id}")

def get_secret(secret_id: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    project_id = "gridiron-picks-16499"
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def get_games_from_api(week: int):
    API_KEY = get_secret("CFP_API_KEY")
    url = f"https://api.collegefootballdata.com/games?year=2025&seasonType=regular&week={week}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(url, headers=headers)
    return response.json().get("games", [])
