import os
from configparser import ConfigParser
import threading
import time


class Controller:

    def __init__(self):
        self.ext = ExternalConfigs()
        self.conf = self.ext.config
        # Here you can add menu functions, and set app parameters
        self.parameters = {
            'app_version': 0.1,
            'app_name': 'Test App',
            't_size': 115,
            'var_title_len': 30,
            'variants': [
                {
                    'name': 'Example',
                    'description': 'example thing',
                    'command': 'example_command',
                    'menu_reprint': False,
                    'hide_menu': False,
                    'background': False,
                },
                {
                    'name': 'Example async',
                    'description': 'example thing',
                    'command': 'example_command_async',
                    'menu_reprint': False,
                    'hide_menu': False,
                    'background': True,
                }
            ],
            'special_variants': [
                {
                    'name': 'Example Special',
                    'command': 'special_example',
                    'description': '',
                    'repr': 'se',
                    'menu_reprint': False,
                    'hide_menu': False,
                    'background': False,
                }
            ]
        }

    # Here all you menu methods go

    def example_command(self):
        print('Hi, example_command')
        print(self.conf['App']['example'])

    def example_command_async(self):
        time.sleep(3)
        print('Hi, example_command_async')
        time.sleep(2)
        print('Background task')
        time.sleep(1)
        print('Complete')
        print(self.conf['App']['example'])

    @staticmethod
    def special_example():
        print('Hi, special_example')


class CLI:
    def __init__(self, props, variants, special_variants=None):
        self.version = '0.05'
        self.build_in_commands = [
            {
                'name': 'Clear screen',
                'command': 'cls',
                'description': 'Clear app screen',
                'repr': 'cls',
                'menu_reprint': False,
                'hide_menu': False,
                'background': False,
            },
            {
                'name': 'Exit',
                'command': 'quit',
                'description': 'Exit app',
                'repr': 'q',
                'menu_reprint': False,
                'hide_menu': False,
                'background': False,
            }
        ]
        self.props = props
        self.variant_title_len = self.variant_title_len_setup()
        self.term_size = self.term_size_setup()
        self.variants = variants
        self.special_variants = self.special_variants_setup(special_variants)
        self.command_dict = self.command_dict_create()
        self.build_in_command_dict = self.build_in_command_dict_create()
        self.regular_variants_array = self.prepare_variants()
        self.special_variants_array = self.prepare_special_variants()
        self.menu = self.render_menu()

    @staticmethod
    def get_input(message):
        return input(message)

    def variant_title_len_setup(self):
        length = 40
        if ('var_title_len' in self.props) and (self.props['var_title_len'] != ''):
            length = self.props['var_title_len']
        return length

    def special_variants_setup(self, special_variants):
        result = []
        if special_variants:
            result += special_variants
        result += self.build_in_commands
        return result

    def term_size_setup(self):
        length = 110
        if ('t_size' in self.props) and (self.props['t_size'] != ''):
            length = self.props['t_size']
        return length

    def command_dict_create(self):
        command_dict = {}
        for ind, variant in enumerate(self.variants, 1):
            index = str(ind)
            if 'repr' in variant:
                index = variant["repr"]
            command_dict[index] = variant["command"]
        for variant in self.special_variants:
            ind = variant["repr"]
            command_dict[ind] = variant["command"]
        return command_dict

    def build_in_command_dict_create(self):
        command_dict = {}
        for variant in self.build_in_commands:
            ind = variant["repr"]
            command_dict[ind] = variant["command"]
        return command_dict

    def choose(self):
        while True:
            var = self.get_input('>>> ')
            if var in self.build_in_command_dict.keys():
                eval(f'self.{self.build_in_command_dict[var]}()')
                continue
            if var in self.command_dict.keys():
                return self.command_dict[var]
            else:
                print('Wrong input')

    def available_variants(self):
        var_pack = {}
        for ind, variant in enumerate(self.variants, 1):
            var_pack[str(ind)] = variant['command']
        for variant in self.special_variants:
            var_pack[variant['repr']] = variant['command']
        return var_pack

    def prepare_special_variants(self):
        variants = []
        for var in self.special_variants:
            name = f'| {var["repr"]}. {var["name"]}'

            name_len = len(name)
            diff = self.variant_title_len - name_len
            if diff > 0:
                var['name'] = name + (' ' * diff)
            elif diff < 0:
                var['name'] = name[:diff]
            else:
                var['name'] = name
            name_len = len(var['name'])
            description = var['description']
            description_len = len(description)
            diff = self.term_size - (name_len + 2 + description_len)
            if diff > 0:
                var['description'] = description + (' ' * diff)
            elif diff < 0:
                var['description'] = description[:diff - 3] + '...'
            else:
                var['description'] = description
            variants.append(var)
        return variants

    def prepare_variants(self):
        variants = []
        for ind, var in enumerate(self.variants, 1):
            name = f'| {ind}. {var["name"]}'

            name_len = len(name)
            diff = self.variant_title_len - name_len
            if diff > 0:
                var['name'] = name + (' ' * diff)
            elif diff < 0:
                var['name'] = name[:diff]
            else:
                var['name'] = name
            name_len = len(var['name'])
            description = var['description']
            description_len = len(description)
            diff = self.term_size - (name_len + 2 + description_len)
            if diff > 0:
                var['description'] = description + (' ' * diff)
            elif diff < 0:
                var['description'] = description[:diff - 3] + '...'
            else:
                var['description'] = description
            variants.append(var)
        return variants

    def print_header(self):
        info = f' {self.props["app_name"]} v{self.props["app_version"]} '
        return self.print_center(info, '#')

    def print_bottom(self):
        txt = f' CLI ver.{self.version} by TwoCatsCanFly '
        return self.print_center(txt, '#')

    def print_center(self, txt, outline):
        len_txt = len(txt)
        z = (self.term_size // 2) - (len(txt) // 2) - 1
        f = self.term_size - (z + len_txt + 1)
        result = f'|{outline * z}{txt}{outline * f}|'
        return result

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def cls(self):
        self.clear_screen()
        print(self.menu)

    @staticmethod
    def quit():
        quit()

    def print_underline(self):
        result = f'|{"_" * (self.variant_title_len - 1)}|{"_" * (self.term_size - self.variant_title_len - 1)}|'
        return result

    def print_upperline(self):
        result = f'|{"-" * (self.variant_title_len - 1)}|{"-" * (self.term_size - self.variant_title_len - 1)}|'
        return result

    def print_topline(self):
        result = f'|{"-" * (self.term_size - 1)}|'
        return result

    def print_variants(self):
        variants = []
        self.print_header()
        self.print_topline()
        for var in self.regular_variants_array:
            line = f'{var["name"]}| {var["description"]}|'
            variants.append(line)
        variants.append(self.print_upperline())
        for var in self.special_variants_array:
            line = f'{var["name"]}| {var["description"]}|'
            variants.append(line)
        variants.append(self.print_underline())
        return variants

    def render_menu(self):
        menu = []
        renderable = ''
        menu += [self.print_header()]
        menu += [self.print_topline()]
        menu += self.print_variants()
        menu += [self.print_bottom()]
        for i in menu:
            renderable += i
            renderable += '\n'
        return renderable

    def menu_print(self):
        print(self.menu)


class Worker:
    def __init__(self):
        self.controller = Controller()
        self.props = {
            'app_version': self.from_target()['app_version'] or self.default()['app_version'],
            'app_name': self.from_target()['app_name'] or self.default()['app_name'],
            't_size': self.from_target()['t_size'] or self.default()['t_size'],
            'var_title_len': self.from_target()['var_title_len'] or self.default()['var_title_len'],
        }
        self.variants = self.from_target()['variants'] or self.default()['variants']
        self.special_variants = self.from_target()['special_variants'] or self.default()['special_variants']
        self.cli = CLI(self.props, self.variants, self.special_variants)
        self.cli.menu_print()
        self.params = self.list_of_params(self.variants, self.special_variants)
        self.main_loop()

    def list_of_params(self, variants, special_variants):
        list_params = {}
        for i in variants:
            list_params[i['command']] = {
                'menu_reprint': i['menu_reprint'],
                'hide_menu': i['hide_menu'],
                'background': i['background'],
            }
        for i in special_variants:
            list_params[i['command']] = {
                'menu_reprint': i['menu_reprint'],
                'hide_menu': i['hide_menu'],
                'background': i['background'],
            }
        return list_params

    def executor(self, command):
        try:
            list_of_params = self.params[command]
            if list_of_params['hide_menu']:
                self.cli.clear_screen()
            if list_of_params['background']:
                self.async_execution(command)
            else:
                self.regular_execution(command)
            if list_of_params['hide_menu'] or list_of_params['menu_reprint']:
                print(self.cli.menu)
        except Exception as err:
            print(err)

    def regular_execution(self, command):
        eval(f'self.controller.{command}()')

    def async_execution(self, command):
        thread = threading.Thread(target=self.regular_execution, args=[command])
        thread.start()

    def main_loop(self):
        while True:
            var = self.cli.choose()
            self.executor(var)

    def default(self):
        return {
            'app_version': 0.1,
            'app_name': 'Test App',
            't_size': 115,
            'var_title_len': 30,
            'variants': [
                {
                    'name': 'Example',
                    'description': 'example thing',
                    'command': 'example_command',
                    'menu_reprint': False,
                    'hide_menu': False,
                    'background': False,
                }
            ],
            'special_variants': [
                {
                    'name': 'Example Special',
                    'command': 'special_example',
                    'description': '',
                    'repr': 'se',
                    'menu_reprint': False,
                    'hide_menu': False,
                    'background': False,
                }
            ]
        }

    def from_target(self):
        return self.controller.parameters


class ExternalConfigs:

    def __init__(self):
        self.config = self.external_settings()

    def external_settings(self):
        data = 'config.ini'
        config = ConfigParser()
        config.read(data)
        return config


if __name__ == '__main__':
    Worker()
