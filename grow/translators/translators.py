from . import google_translator_toolkit
from grow.common import utils


_kinds_to_classes = {}
_builtins = (
    google_translator_toolkit.GoogleTranslatorToolkitTranslator,
)


def install_translator(translator):
    _kinds_to_classes[translator.KIND] = translator


def install_builtins():
    global _destination_kinds_to_classes
    for builtin in _builtins:
        install_translator(builtin)


def create_translator(pod, kind, config, inject=False,
                      project_title=None, instructions=None):
    install_builtins()
    if kind not in _kinds_to_classes:
        raise ValueError('No translator exists: "{}"'.format(kind))
    translator = _kinds_to_classes[kind]
    return translator(pod=pod, config=config, inject=inject,
                      project_title=project_title, instructions=instructions)


def register_extensions(extension_paths, pod_root):
    for path in extension_paths:
        cls = utils.import_string(path, [pod_root])
        install_translator(cls)
