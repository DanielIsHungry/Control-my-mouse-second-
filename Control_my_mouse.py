try:
    import time
    import os
    import pyautogui
    from pynput.mouse import Controller
    import firebase_admin
    from firebase_admin import credentials, db
except ModuleNotFoundError:
    import os
    os.system('pip install pyautogui')
    os.system('pip install pynput')
    os.system('pip install firebase_admin')

class CloudVariable:
    def __init__(self,
                 value,
                 name,
                 cred_path="python-backend-test-229d2-firebase-adminsdk-fbsvc-f463d3b6e9.json",
                 db_url="https://python-backend-test-229d2-default-rtdb.firebaseio.com/"):

        if not firebase_admin._apps:
            if cred_path and db_url:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': db_url
                })
            else:
                raise ValueError("Firebase not initialized and no credentials provided.")

        self.name = name
        self.ref = db.reference(name)
        self.set(value)

    def get(self):
        return self.ref.get()

    def set(self, value):
        self.ref.set(value)

    def __repr__(self):
        return f"CloudVariable(name='{self.name}', value={self.get()})"

    def __add__(self, other):
        new_value = self.get() + other
        self.set(new_value)
        return new_value

    def __sub__(self, other):
        new_value = self.get() - other
        self.set(new_value)
        return new_value

    def __mul__(self, other):
        new_value = self.get() * other
        self.set(new_value)
        return new_value

    def __truediv__(self, other):
        new_value = self.get() / other
        self.set(new_value)
        return new_value

if __name__ == '__main__':
    mpx = CloudVariable(0, 'mouse pointer x')
    mpy = CloudVariable(0, 'mouse pointer y')

    if os.getenv('USERNAME') == 'lucky_5t21e5h': # my desktop
        print('admin detected. ur mouse can be moved by others.')

        def redirect_mouse():
            while True:
                pyautogui.moveTo(x=int(mpx.get()), y=int(mpy.get()))
                time.sleep(0.05)

        redirect_mouse()
    else:
        print('user detected. you can control admin mouse')

        mouse = Controller()
        def capture_mouse():
            while True:
                x, y = mouse.position
                mpx.set(x)
                mpy.set(y)
                time.sleep(0.05)
