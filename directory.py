import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


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
                # raise SyntaxError("Parent node does not exist")
        if pieces:
            if pieces[-1] in temp_trie:
                logging.warning("Node already exists")
                return None
                # raise SyntaxError("Node already exists")
            else:
                temp_trie[pieces[-1]] = {}
        else:
            logging.error("Something bad")
            return None
        return path

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
        pass # this one is a bit harder...

    @property
    def paths(self):
        return self._paths

    @property
    def end(self):
        return self.__end

class FakeFs(object):

    def __init__(self):
        self._dirs = _Trie()
        self._paths = set("/")

    def mknode(self, directory):
        if self._dirs.add(directory):
            self._paths.add(directory)


    def dir_exists(self, dir_path):
        return self._dirs.exists(dir_path)

    def rm(self, dir_path):
        if self.dir_exists(dir_path):
            return self._dirs.remove(dir_path)
        else:
            logging.error("Cannot remove directory.")

    def rmdir(self, directory):
        pass

    def touch(self, filename):
        pass


    @property
    def paths(self):
        return self._paths

if __name__ == '__main__':
    fs = FakeFs()
    fs.mknode("/poo/woo/soo/doo/poo")
    fs.mknode("/etc")
    fs.mknode("/")
    fs.mknode("/tmp")
    fs.mknode("/tmp/whatever")
    fs.mknode("/var/www/mysite")
    fs.mknode("/etc")
    fs.dir_exists("/sadsad")
    fs.dir_exists("/etc")
    print(fs.paths)
