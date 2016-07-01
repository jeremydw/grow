import os


class Error(Exception):
    pass


class PreprocessorError(Error):
    pass


class BasePreprocessor(object):

    def __init__(self, pod, config, autorun=True, name=None, tags=[],
                 inject=False):
        self.pod = pod
        self.root = pod.root
        self.config = config
        self.logger = self.pod.logger
        self.autorun = autorun
        self.name = name
        self.tags = tags or []
        self.injected = inject

    def first_run(self):
        self.run()

    def run(self, build=True):
        raise NotImplementedError

    def can_inject(self, doc=None):
        """Returns whether the preprocessor can inject data into a doc."""
        return False

    def inject(self, doc=None):
        """Injects data into a doc without modifying the filesystem."""
        pass

    def list_watched_dirs(self):
        return []

    def normalize_path(self, path):
        if path.startswith('/'):
            return os.path.join(self.root, path.lstrip('/'))
        return path
