import unittest
import sys
import jinja2

sys.path.append('../..')

from dataReport import resolve_variables_from_config_files

def test_resolve_variables_from_config_files():
    context = {  
        'PNG_HEIGHT' : self.envConfData['PNG_HEIGHT']
    }
    path = 'Users\AZO\Desktop\collect_util_data\templates'
    filename = 'conf_file.json'

    rendered = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path)
    ).get_template(filename).render(context)

    
    assert self.envConfData['PNG_HEIGHT'] in rendered