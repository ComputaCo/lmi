from lmi.app.app import App


class RemoteApp(App):
    host: str
    port: str
    remote_app_id: str
