import requests
import pandas as pd
from io import BytesIO
import traceback
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

class SharePointExcelReader:
    def __init__(self, url, username, password, relative_url):
        self.url = url
        self.username = username
        self.password = password
        self.relative_url = relative_url

    def read_excel(self):

        # Authentication
        self.ctx_auth = AuthenticationContext(self.url)
        if self.ctx_auth.acquire_token_for_user(self.username, self.password):
            self.ctx = ClientContext(self.url, self.ctx_auth)
            self.web = self.ctx.web
            self.ctx.load(self.web)
            self.ctx.execute_query()
            print("Web title: {0}".format(self.web.properties['Title']))
        else:
            print(self.ctx_auth.get_last_error())

        self.response = File.open_binary(self.ctx, self.relative_url)

        # save data to BytesIO stream
        self.bytes_file_obj = io.BytesIO()
        self.bytes_file_obj.write(self.response.content)
        self.bytes_file_obj.seek(0)  # set file object to start

        return self.bytes_file_obj