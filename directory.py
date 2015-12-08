import logging

def _input_path_sanitizer(func):
    def inner(trie, path):
        if not path.startswith("/"):
            raise SyntaxError("Path must starts with a / character")
        return func(trie, path)
    return inner

class _Trie(object):

    _paths = {}
    __end = 'end'

    def make_trie(self, *args):
        for path in args:
            self.add(path)

    @staticmethod
    def get_pieces(path):
        return path.split("/")[1:]

    @_input_path_sanitizer
    def add(self, path):
        logging.info("Adding node {}".format(path))
        pieces = self.get_pieces(path)
        temp_trie = self._paths
        for piece in pieces[:-1]:
            if piece in temp_trie:
                temp_trie = temp_trie[piece]
            else:
                logging.warning("Parent node does not exist")
                return None
        if pieces:
            if pieces[-1] in temp_trie:
                logging.warning("Node already exists")
                return None
            else:
                temp_trie[pieces[-1]] = {}
        else:
            logging.error("Something bad")
            return None
        return path

    @_input_path_sanitizer
    def can_add(self, path):
        pieces = self.get_pieces(path)
        temp_trie = self._paths
        for piece in pieces[:-1]:
            if piece in temp_trie:
                temp_trie = temp_trie[piece]
            else:
                logging.warning("Parent node does not exist")
                return None
        if pieces:
            if pieces[-1] in temp_trie:
                logging.warning("Node already exists")
                return None
            else:
                return True
        else:
            return None

    @_input_path_sanitizer
    def exists(self, path):
        pieces = self.get_pieces(path)
        temp = self._paths
        for piece in pieces:
            if piece not in temp:
                logging.info("{} does not exist".format(path))
                return False
            temp = temp[piece]
        logging.info("{} exists".format(path))
        return True

    @_input_path_sanitizer
    def remove(self, path):
        logging.info("Removing node {}".format(path))
        pieces = self.get_pieces(path)
        temp_trie = self._paths
        for piece in pieces[:-1]:
            if piece in temp_trie:
                temp_trie = temp_trie[piece]
            else:
                logging.warning("Parent node does not exist")
                return None
        if pieces:
            if pieces[-1] in temp_trie:
                del temp_trie[pieces[-1]]
            else:
                logging.warning("Node doesn't exist")
                return None
        else:
            logging.error("Something bad")
            return None
        return path

    @_input_path_sanitizer
    def ls(self, path):
        pieces = self.get_pieces(path)
        temp = self._paths
        for piece in pieces:
            if piece not in temp:
                logging.info("{} does not exist".format(path))
                return False
            temp = temp[piece]
        out = [
                path + '/' + i
                for i
                in temp.keys()
             ]
        return out


    @property
    def paths(self):
        return self._paths

    @property
    def end(self):
        return self.__end

class Directory(object):

    def __init__(self):
        self._dirs = _Trie()
        self._data = {"/" : None}

    def mknode(self, directory, data=None):
        if self._dirs.add(directory):
            self._data[directory] = data

    def exists(self, dir_path):
        return self._dirs.exists(dir_path)

    def rm(self, dir_path):
        if self._dirs.remove(dir_path):
            path_data = self._data.pop(dir_path, None)
            # TODO delete all children
            return (dir_path, path_data, "stat")
        else:
            logging.error("Cannot remove directory.")
            return None

    def ls(self, path):
        return self._dirs.ls(path)

    def can_mknode(self, path):
        return self._dirs.can_add(path)

    @property
    def data(self):
        return self._data

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    fs = Directory()
    fs.mknode("/poo/woo/soo/doo/poo")
    fs.mknode("/etc")
    fs.mknode("/etc/1")
    fs.mknode("/etc/1/2")
    print fs.ls("/etc")
    fs.mknode("/etc/1/2/3")
    fs.mknode("/etc/1/2/3/4")
    fs.rm("/etc/1/2/3")
    fs.mknode("/")
    fs.mknode("/tmp")
    fs.mknode("/tmp/whatever")
    fs.rm("/tmp/whatever")
    fs.mknode("/var/www/mysite")
    fs.mknode("/etc")
    fs.exists("/sadsad")
    fs.exists("/etc")
    print(fs.data)
