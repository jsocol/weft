import os
import yaml
from weft.commands._base import make_option, BaseCommand
from weft.entities._base import BaseEntity


class Command(BaseCommand):
    command_options = (
        make_option('config', action='store', dest='config',
                    help='Config file to sync to remote system.'),
    )
    help = 'Synchronize remote state with configuration.'

    def parse_config_file(self, path):
        with open(path) as fp:
            return yaml.safe_load(fp.read())

    def find_entities(self, entity_path=None):
        entity_path = 'weft/entities'
        return  [f[:-3] for f in os.listdir(entity_path) if not
                 f.startswith('_') and f.endswith('.py')]

    def load_entity_classes(self):
        entity_classes = []
        for m in self.find_entities():
            mod = __import__('weft.entities.' + m)
            for o in dir(mod):
                if BaseEntity in o.__bases__:
                    entity_classes.append(o)
        return entity_classes

    def build_entities(self, entity_cls, entries):
        entities = []
        if entity_cls.uses_key:
            for key in entries:
                entities.append(entity_cls.from_python(key, entries[key]))
        else:
            for entry in entries:
                entities.append(entity_cls.from_python(entry))
        return entities

    def handle(self, **options):
        config = self.parse_config_file(options.config)
        for entity_cls in self.load_entity_classes():
            if entity_cls.root_key in config:
                entities = self.build_entities(entity_cls,
                                               config[entity_cls.root_key])
                for e in entities:
                    e.sync()
