
import io
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload, MediaIoBaseDownload

from django.http import StreamingHttpResponse

from google_drive_API.config import SCOPES
from chat.utils import generator


class GoogleServices(object):
    @staticmethod
    def get_credentials():
        credentials = None

        if os.path.exists('./google_drive_API/json/token.json'):
            credentials = Credentials.from_authorized_user_file(
                './google_drive_API/json/token.json', SCOPES)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './google_drive_API/json/credentials.json', SCOPES)
                credentials = flow.run_local_server(port=3000)

            with open('./google_drive_API/json/token.json', 'w') as token:
                token.write(credentials.to_json())

        return credentials


class GoogleDrive(GoogleServices):
    def __init__(self):
        self.service = build('drive', 'v3', credentials=self.get_credentials())

    def get_file(self, file_id):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while done is False:
            _, done = downloader.next_chunk()

        return fh

    def put_file(self, filename, body):
        file_metadata = {'name': filename}

        file = self.service.files().create(
            body=file_metadata,
            media_body=MediaInMemoryUpload(body),
            fields='id'
        ).execute()

        return file.get('id')


def google_drive_serve(request, file_id, *args, **kwargs):
    content = g_drive.get_file(file_id)

    return StreamingHttpResponse(generator(content))


def upload_to_google_drive(filename, content):
    return g_drive.put_file(filename, content)


g_drive = GoogleDrive()
