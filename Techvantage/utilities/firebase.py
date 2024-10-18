import firebase_admin
from firebase_admin import credentials, auth, storage
from django.conf import settings
from rest_framework import exceptions

# Initialize Firebase App (this should only be done once in your entire project)
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "newproject-7ad97",
  "private_key_id": "869fca585cacc3c9bf91a97e2c1a4054f1df8f10",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDEYnW43aAany7V\nK9bvzXLHBQlmyuBN1ROh9wCfQQvLVJZAGj9VtZPZu2U+FQZB4P8sS9SWv8no+L2r\nhozI8QWlaHumad9t8ZJCTCAyLgOvOSHHREatup+j+NpCxdQjipip3PGCSewAIxrO\nQFZD5Bj4TwKxtQ5wHzt6AFrAS3WvPJPVTh5nNn2lXCK5IzCSK4bi+4NUzs9enwZ+\ntTtCXGUMbl02lifdtOwiaKOGUaCDDF8oq5X7qIkX/nErKioNPJRCjNH/sUhphy8/\nxZ7iDHbZEvPSnYmApGD0QLa2w93ruUimNBbij6JH9v9pwkQGgCION1PMo1nBMa2F\nRdx4kjXrAgMBAAECggEAHoV06V3cd7a8txnApnVmPMMuImEuejo++mGioZ2g4SGM\n1nqd1ErLpz/GLN9koRGAZxiD+kflcAVUqRdYwxQefgYejY8P0A0G37HoIRRgszds\nZgVY/MAv9nKDLXSEk1+DeYbirA6kFKNgE6URIy0Mqm7RKuBKVaes/TmX4SH5MNox\nkpZd4FmPfqru4NqsPnr9euGmm+TdcSudq1EDeCA4QpiqoIUeyMy0WVec/Ryn9RLU\nzYoerOHHL8jHPAjYTIUlu0yVlseSSoUqvozmERAOnXSWiPupYBgwH0jp5sMqYBg8\nUgrveVkIB1SkX19ICewjc2YADytWftIQcWFei1wFnQKBgQD/IG58eVtbKZU8tGzM\nOnxFt2D4S9xyVuzxB45mHMYc/W35K7i5fyU4oFjlfrtbOhMg7KmaKGQbAZCgUI2r\nl4eMm9oF9C6UfGJg4zyQoS4CRAK3VvxaPvVILRGf2wpCIDK8CG58GaLlhSbDfdOI\n2wffc1kIiRpV0r+7f9LPn9AthwKBgQDFDo1oh91gIYLFs6RoAhkk5eeKZ81e4GKN\nVIAM4KC3APDnHEBWYZcZb9coakvV0tZvmbIg2OYAMErhIf088H/g0iJbKPnSkx2c\ndyk3uZ78+Gl/w6U/TE0oWV+knvMsi+JTzpZ6d+F7A7eSnsSb8tOMmQwgYZ933pjF\nO/taPYrtfQKBgQCARBjoQcc5ZQWf2IIeh4T1NAXvr4wsfCFx6L+h/PNpncyNinq7\n3/2ho5QuBXJCokb9tZ5rX8U8gqPoxbcEPxGqEq0hcyt8AbEgTv6jJDXSc8j9ziDf\namm9GNOUj/ZvWmrHeGG7yNPKGxBrFrakRqKFqCNqFCwGXAeDR/d/5TQvvwKBgAVJ\n+bOnieKNo7PouW3tOH2MCiXl2VZFkX+XmARAdy/SP6UEVhm7btHI9a5pA/YOPaEr\nL+O/zpSMt0XJosFi9xuyqCdoNyRWvIG5lQqg2cqSZEqAlsvXIW8GzxFdDsvQSVfU\ngKdy1kN1+xRdXIuO/eyVIwUveZc/Czyn+nwWkMcFAoGATimcG9RGTv1e7yU0EeOF\n5twR1epbpOMvn8T9pm2vKl7/iIpAOP7KabQilEMbEpp/UiLZTGyOny1j65ni8F+y\nGoKGKh5tUVaiDvNjdq4B5sqR/EEXkQ5l+ljDPinFxCv2mZA6GjrQURwgEzWHZgHP\nTQ4lI3ScQS9SDVJwMK1aW48=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-6at0z@newproject-7ad97.iam.gserviceaccount.com",
  "client_id": "115858408144336071349",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-6at0z%40newproject-7ad97.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred, {
    'storageBucket': 'newproject-7ad97.appspot.com'
})

def verify_firebase_token(id_token):
    """
    Verifies the Firebase ID token sent by the client.
    Raises exceptions if the token is invalid or expired.
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except auth.ExpiredIdTokenError:
        raise exceptions.AuthenticationFailed('Token has expired. Please log in again.')
    except auth.InvalidIdTokenError:
        raise exceptions.AuthenticationFailed('Invalid token. Please log in again.')
    except Exception as e:
        raise exceptions.AuthenticationFailed('Token authentication failed.')

def login_firebase_user(email, password):
    """
    Simulates a Firebase login using REST API.
    """
    import requests
    import json

    FIREBASE_WEB_API_KEY = settings.FIREBASE_WEB_API_KEY
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": True
    })
    
    response = requests.post(url, data=payload)
    data = response.json()

    if response.status_code == 200:
        return data  # contains token and user info
    else:
        raise exceptions.AuthenticationFailed(data.get("error", {}).get("message", "Authentication failed"))

def logout_firebase_user(uid):
    """
    Revokes refresh tokens for the user, effectively logging them out.
    """
    auth.revoke_refresh_tokens(uid)

def create_firebase_user(email, password, display_name):
    """
    Creates a new Firebase user with email and password.
    """
    try:
        user = auth.create_user(email=email, password=password, display_name=display_name) 
        return user
    except Exception as e:
        raise exceptions.APIException(f'Error creating user: {str(e)}')
    
def update_user_display_name(uid, new_display_name):
    """
    Function to update Firebase user's displayName.
    """
    user = auth.update_user(
        uid,
        display_name=new_display_name  # Updating displayName
    )
    return user

import mimetypes

from firebase_admin import storage

def upload_file_to_firebase(file, path):
    # Assuming you've already initialized Firebase Storage
    bucket = firebase_admin.storage.bucket()

    # Create a blob for the file
    blob = bucket.blob(path)

    # Upload the file and set the content type
    blob.upload_from_file(file, content_type=mimetypes.guess_type(file.name)[0])

    # Optionally, make the file public or set permissions
    blob.make_public()

    return blob.public_url

def upload_app_file(file, app_name):
    """Upload file to Firebase storage under the specific app's folder."""
    path = f'{app_name}/uploads/{file.name}'
    return upload_file_to_firebase(file, path)
