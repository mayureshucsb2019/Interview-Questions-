class Entity:
    def __init__(self, path="", type="", hash="", readable=True, link=""):
        self._path = path
        self._type = type  # "folder" / "file" / "symlink"
        self._hash = hash  # if file then it has hash
        self._readable = readable # for files and folder
        self._special = False
        self._link = path if link == "" else link
    @property
    def special(self):
        return self._special

    @special.setter
    def special(self, special):
        self._special = special
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, hash):
        self._hash = hash

    @property
    def readable(self):
        return self._readable

    @readable.setter
    def readable(self, readable):
        self._readable = readable

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, link):
        self._link = link

    def __repr__(self):
        return self._path

    def __lt__(self, other):
        return self._path < other.path

    def __gt__(self, other):
        return self._path > other.path
