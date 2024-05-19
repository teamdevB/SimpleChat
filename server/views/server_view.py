import os
import string
import termcolor



class ServerView:

    def __init__(self, base_dir_path):
        self.base_dir_path = base_dir_path

    def _validate_template(func):
        def _wrapper(self, template_file, color=None):
            if not os.path.isdir(self.base_dir_path):
                raise NotADirectoryError

            template_path = os.path.join(self.base_dir_path, template_file)

            if not os.path.isfile(template_path):
                raise FileNotFoundError

            return func(self, template_path, color)

        return _wrapper

    @_validate_template
    def template(self, template_file, color=None):

        with open(template_file, 'r', encoding='utf-8') as template_file:
            contents = template_file.read()
            contents = contents.rstrip(os.linesep)
            #contents = '{splitter}{sep}{contents}{sep}{splitter}{sep}'.format(
                #contents=contents, splitter="-" * 60, sep=os.linesep)
            contents = termcolor.colored(contents, color)
            return string.Template(contents)
