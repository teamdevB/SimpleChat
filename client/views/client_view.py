import os
import string
import termcolor
class ClientView:
    BASE_DIR_PATH = './client/templates/'

    @classmethod
    def get_template(cls,template_file, color=None):
        template = os.path.join(cls.BASE_DIR_PATH, template_file)

        with open(template, 'r', encoding='utf-8') as template_file:
            contents = template_file.read()
            contents = contents.rstrip(os.linesep)
            contents = '{splitter}{sep}{contents}{sep}{splitter}{sep}->'.format(
                contents=contents, splitter="=" * 60, sep=os.linesep)
            contents = termcolor.colored(contents, color)
            return string.Template(contents)
