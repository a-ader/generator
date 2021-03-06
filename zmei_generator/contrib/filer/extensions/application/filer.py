from zmei_generator.contrib.admin.extensions.application.suit import \
    SuitAppExtension
from zmei_generator.domain.application_def import ApplicationDef
from zmei_generator.domain.extensions import ApplicationExtension
from zmei_generator.parser.gen.ZmeiLangParser import ZmeiLangParser
from zmei_generator.parser.utils import BaseListener


class FilerAppExtension(ApplicationExtension):

    @classmethod
    def get_name(cls):
        return 'filer'

    def get_required_deps(self):
        return [
            'git+git://github.com/nephila/django-filer@feature/django-2.0#egg=django-filer']

    def get_required_apps(self):
        return [
            'easy_thumbnails',
            'filer',
            'mptt',
        ]

    @classmethod
    def write_settings(cls, apps, f):
        f.write('\nTHUMBNAIL_HIGH_RESOLUTION = True\n')

    def post_process(self):
        if self.application.supports(SuitAppExtension):
            self.application[
                SuitAppExtension].menu.append(
                {'label': 'Files & folders', 'app': 'filer'})


class FilerAppExtensionParserListener(BaseListener):
    def __init__(self, application: ApplicationDef) -> None:
        super().__init__(application)

        self.filer_extension = None

    def enterAn_filer(self, ctx: ZmeiLangParser.An_filerContext):
        self.filer_extension = FilerAppExtension(self.application)
        self.application.extensions.append(self.filer_extension)
        self.application.register_extension(self.filer_extension)

        self.application.extensions.append(
            self.filer_extension
        )
