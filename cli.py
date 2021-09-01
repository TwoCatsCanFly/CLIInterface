import os
import menu_functions as target


class CLI:
    def __init__(self, props, variants, special_variants=None):
        self.version = '0.02'
        self.build_in_commands = [
            {
                'name': 'Clear screen',
                'command': 'cls',
                'description': 'Clear app screen',
                'repr': 'cls',
                'async': False,
                'menu_reprint': False,
                'background': False,
            },
            {
                'name': 'Exit',
                'command': 'quit',
                'description': 'Exit app',
                'repr': 'q',
                'async': False,
                'menu_reprint': False,
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
        info = f' {self.props["app_name"]} v{self.props["version"]} '
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

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')
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
        self.props = {
            'version': 0.1,
            'app_name': 'Test App',
            't_size': 115,
            'var_title_len': 30,
        }
        self.variants = [
            {
                'name': 'Example',
                'description': 'example thing',
                'command': 'example_command'
            }
        ]
        self.special_variants = [
            {
                'name': 'Example Special',
                'command': 'special_example',
                'description': '',
                'repr': 'se'
            }
        ]
        self.cli = CLI(self.props, self.variants, self.special_variants)
        self.cli.menu_print()
        self.main_loop()

    def get_params(self):
        app_version = 0.1
        app_name = 'Test App'
        t_size = 115
        var_title_len = 30
        variants = [
            {
                'name': 'Example',
                'description': 'example thing',
                'command': 'example_command'
            }
        ]
        special_variants = [
            {
                'name': 'Example Special',
                'command': 'special_example',
                'description': '',
                'repr': 'se'
            }
        ]





    def main_loop(self):
        while True:
            var = self.cli.choose()
            try:
                eval(f'target.{var}()')
            except Exception as err:
                print(err)

# class SettingsGrabber:
#

if __name__ == '__main__':
    Worker()
