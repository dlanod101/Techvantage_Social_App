import firebase_admin
from firebase_admin import credentials, auth, storage
from django.conf import settings
from rest_framework import exceptions

# Initialize Firebase App (this should only be done once in your entire project)
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "newproject-7ad97",
  "private_key_id": "7a7c9f9251a23a895ff2635c0747a6d4bbd234ad",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDbRGHT6njVbcDn\nE6Z/H6XWwE9oauGihSEAOgZdeVzmBuRQiNZCF0+OL9ewF25URv6zeEiIKBa/rZH8\nqtVQ+z40CvGB1WfBVaOpNOhy9kaNgYGdaD997dgCKJ8kKVDL0mJANmHgxV2IYzxb\ndmFfmU4LiSSKgWzJXsm6kW4QIhTeFjE0+WyvJcWk7F7Lqu1my7wy65kGOFPoK8fB\npKFuChidURUtNcLv/W89mNvDloTwj6v33CIAO1nHKoBabbBc8xnzYZ3T2c+FAaMH\nQwZTCYsycrgKCEXVywhgMU6TbFf7OlJ7g4EwU6VTf/fMmt1WPx6kPanZkQbQwsDw\n+LwXMxFLAgMBAAECggEAOFmWFJqVDDClGx2rM89j1NFedvTE4Pn6ta6z1RDsBXeu\n9F1+RsTr3pw//5K9+W23ZlMavNckpYULWBZlNOckoMZRM68u93o1UbZ1qJnPHu2x\n7EyOyKO32DItV+NATulV86+mLtg6BeOO7uh49NMWwhMwL2I8nXG9QTO/x+iiWUJ7\n4NlRusdK84mM6nNOoa/wpDAWDH0IXAnr6hlKaUJxzCLm3hMUqExiDnxpVQgvrqqn\nNVUb6URBoqVNAeXW7ovAVpZEw57EsSOCzPx3XtzA5rgUgjQIxi+BiGMPjU+IZNBR\nacO/Pc1cBVLo2QXUyuyYPLS5UHEdZb9WS3zLqp2dvQKBgQD4S3EJr+FYf7Tl6nzN\nCe/j+4XPjYPMQUOh5g+KU/HByyUet21TJ2ATijbPM5rTiXq8W/B8ynp9iNiy8nvM\nd2lXpkeQO2nNPJRsm3/Ga6jbtTiCmSMY1YRP43Ppya8msl1gdasnPxxEyz2z7PGe\nbw9uP2epkUtreG0lZzXTulQkfwKBgQDiElVMrMsu0mLeLXit7qr5BdvHOnoDeYv8\nTTY4tSQn77tk5LnXaqpB3vQJbLB3eLFtAZ/D2MRZomcOhqCwT495zxZmXPIVLW/C\natTaXX4CW6jEewR8xefF05q3dfroVhVixcTCR4qJejFQnp5+qWTTFR87kOWZyBYS\nie9NsUr9NQKBgHcvp5Qx1CcqLkjLVZsK8Rdr7mCiGqkajv+RMtaA0yTmgewLurPW\ny9y1VPgDWoe+j6cJLxiIDWJjJTpJAbo1e+CyFdobWv9E3C6COkSh+01z4St3nQxX\nugqrMUIBKU2XAxHBiiXtuoEfWoAa9iTKRQrz7qvL7fsptKLmt0TqRWe7AoGBAJmx\nkxI0q1HisFqSGWhOSShRhlBU/hycpsHZkFJPPAx2nDUElx/PoX503/4ESZh/kkgk\ngYR5O0wg7+VdO6OCA23xjy36ZI5nPIK1dI4cX42k2QDzDWLyfRbuPFIbwH/x/koP\nYCwgzRuX2i0QGXrNGQG0a25onN/GutLRucJdFTk9AoGBAOIeX7316ZNnk6+uAOqo\nUf9J2NvI+iaZTcH+VSdmFCC0BrOfE63o2nFxiNnKMpbE2LVifDUlf3DjyNXQX8Md\nYc/jtJFxE+jCQDhUyiiuqJKq6t34PKZuKv6dKbw91VfsUtR0eJo/QDRbX+JedKjl\nRiu4u9u6DAy4ZQgc0MPbZR/+\n-----END PRIVATE KEY-----\n",
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
