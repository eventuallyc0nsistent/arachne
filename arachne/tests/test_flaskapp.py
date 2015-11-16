from arachne.flaskapp import Arachne, check_dir
from unittest import TestCase

class TestFlaskApp(TestCase):

    def __init__(self):
        self.app = Arachne(__name__)

