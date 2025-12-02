from firebase_admin import credentials, initialize_app

cred = credentials.Certificate("firebase/serviceAccount.json")
initialize_app(cred)

print("Firebase OK")
