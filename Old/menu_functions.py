# CLI example use

parameters = {
    'app_version': 0.1,
    'app_name': 'Test App',
    't_size': 115,
    'var_title_len': 30,
    'variants': [
        {
            'name': 'Example',
            'description': 'example thing',
            'command': 'example_command',
            'async': False,
            'menu_reprint': False,
            'background': False,
        }
    ],
    'special_variants': [
        {
            'name': 'Example Special',
            'command': 'special_example',
            'description': '',
            'repr': 'se',
            'async': False,
            'menu_reprint': False,
            'background': False,
        }
    ]
}

def example_command(config):
    print('Hi, example_command')


def special_example(config):
    print('Hi, special_example')
