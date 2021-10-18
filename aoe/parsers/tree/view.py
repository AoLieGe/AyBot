class AoeTreeParser:
    _U = 'units'
    _T = 'techs'

    def __init__(self, tree):
        self._tree = tree.get()

    # function get tuple of unit type (example Archer has tuple of 3 units ),
    # format into line "Archer sep Crossbowman sep Arbalester" sep = separator
    # and add discord cross out symbols if unit isn't available for selected civ
    # parameters:
    #   aoe - tuple of aoe codes (unit or technology)
    #   civ_tree - range of aoe available for civ
    #   data_names - dic of aoe  codes : names
    #   separator for result elements
    def _unpack_line(self, data, civ_codes, data_names, separator):
        result = ''
        named_data = {code: data_names[str(code)] for code in data}

        for code, name in named_data.items():
            if code in civ_codes:
                result += name
            else:
                result += '~~{0}~~'.format(name)

            result += separator

        return result[:-len(separator)]

    # parameters:
    #   civ_codes - dictionary with 'units' aoe codes and 'techs' aoe codes for selected civ
    #   data_names - dictionary with 'units' aoe names and 'techs' aoe names for selected civ
    def get_archers(self, civ_codes, data_names):
        units = ''
        techs = ''

        for unit_type in self._tree[self._U]['archery'].values():
            units += self._unpack_line(unit_type, civ_codes['units'], data_names['units'], ' -> ') + '\n'

        techs += '\nАтака: ' + self._unpack_line(self._tree['techs']['blacksmith']['arc_att'], civ_codes['techs'], data_names['techs'], ' -> ')
        techs += '\nЗащита: ' + self._unpack_line(self._tree['techs']['blacksmith']['arc_arm'], civ_codes['techs'], data_names['techs'], ' -> ')
        techs += '\nТехнологии: ' + self._unpack_line(self._tree['techs']['archery'], civ_codes['techs'], data_names['techs'], ', ')
        techs += ', ' + self._unpack_line(self._tree['techs']['university']['archery'], civ_codes['techs'], data_names['techs'], ', ')

        return units + techs

    def get_infantry(self, civ_codes, data_names):
        units = ''
        techs = ''

        for unit_type in self._tree[self._U]['barrack'].values():
            units += self._unpack_line(unit_type, civ_codes['units'], data_names['units'], ' -> ') + '\n'

        techs += '\nАтака: ' + self._unpack_line(self._tree['techs']['blacksmith']['inf_att'], civ_codes['techs'],
                                                 data_names['techs'], ' -> ')
        techs += '\nЗащита: ' + self._unpack_line(self._tree['techs']['blacksmith']['inf_arm'], civ_codes['techs'],
                                                  data_names['techs'], ' -> ')
        techs += '\nТехнологии: ' + self._unpack_line(self._tree['techs']['barrack'], civ_codes['techs'],
                                                      data_names['techs'], ', ')

        return units + techs

    def get_stable(self, civ_codes, data_names):
        units = ''
        techs = ''

        for unit_type in self._tree[self._U]['stable'].values():
            units += self._unpack_line(unit_type, civ_codes['units'], data_names['units'], ' -> ') + '\n'

        techs += '\nАтака: ' + self._unpack_line(self._tree['techs']['blacksmith']['inf_att'], civ_codes['techs'],
                                                 data_names['techs'], ' -> ')
        techs += '\nЗащита: ' + self._unpack_line(self._tree['techs']['blacksmith']['cav_arm'], civ_codes['techs'],
                                                  data_names['techs'], ' -> ')
        techs += '\nТехнологии: ' + self._unpack_line(self._tree['techs']['stable'], civ_codes['techs'],
                                                      data_names['techs'], ', ')

        return units + techs

    def get_siege(self, civ_codes, data_names):
        units = ''
        techs = ''

        for unit_type in self._tree[self._U]['siege'].values():
            units += self._unpack_line(unit_type, civ_codes['units'], data_names['units'], ' -> ') + '\n'

        techs += '\nТехнологии: ' + self._unpack_line(self._tree['techs']['university']['siege'], civ_codes['techs'], data_names['techs'], ', ')

        return units + techs

    def get_dock(self, civ_codes, data_names):
        units = ''
        techs = ''

        for unit_type in self._tree[self._U]['dock'].values():
            units += self._unpack_line(unit_type, civ_codes['units'], data_names['units'], ' -> ') + '\n'

        return units + techs

    def get_monastery(self, civ_codes, data_names):
        units = ''
        techs = ''

        techs += '\nТехнологии: ' + self._unpack_line(self._tree['techs']['monastery'], civ_codes['techs'], data_names['techs'], ', ')

        return units + techs
