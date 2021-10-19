class TreeViewParser:
    _U = 'units'
    _T = 'techs'

    def __init__(self, tree):
        self.tree = tree.get()
        self.units = self.tree['units']
        self.techs = self.tree['techs']
        self.blacksmith = self.techs['blacksmith']
        self.university = self.techs['university']
        self.codes = {}
        self.names = {}

    # parameters:
    #   civ_codes - dictionary with 'units' aoe codes and 'techs' aoe codes for selected civ
    #   data_names - dictionary with 'units' aoe names and 'techs' aoe names for selected civ
    def archery(self, civ_codes, data_names):
        self.set_data(civ_codes, data_names)
        units = self.unit_info('archery')
        techs = self.tech_info('archery', 'arc_att', 'arc_arm', True, True)
        return units + techs

    def barrack(self, civ_codes, data_names):
        self.set_data(civ_codes, data_names)
        units = self.unit_info('barrack')
        techs = self.tech_info('barrack', 'inf_att', 'inf_arm', True, False)
        return units + techs

    def stable(self, civ_codes, data_names):
        self.set_data(civ_codes, data_names)
        units = self.unit_info('stable')
        techs = self.tech_info('stable', 'inf_att', 'cav_arm', True, False)
        return units + techs

    def siege(self, civ_codes, data_names):
        self.set_data(civ_codes, data_names)
        units = self.unit_info('siege')
        techs = self.tech_info('siege', None, None, False, True)
        return units + techs

    def dock(self, civ_codes, data_names):
        self.set_data(civ_codes, data_names)
        units = self.unit_info('dock')
        return units

    def monastery(self, civ_codes, data_names):
        self.set_data(civ_codes, data_names)
        techs = self.tech_info('monastery', None, None, True, False)
        return techs

    # function get tuple of unit type (example Archer has tuple of 3 units ),
    # format into line "Archer sep Crossbowman sep Arbalester" sep = separator
    # and add discord cross out symbols if unit isn't available for selected civ
    # parameters:
    #   aoe - tuple of aoe codes (unit or technology)
    #   civ_tree - range of aoe available for civ
    #   data_names - dic of aoe  codes : names
    #   separator for result elements
    def _unpack(self, data, type, separator):
        result = ''
        named_data = {code: self.names[type][str(code)] for code in data}

        for code, name in named_data.items():
            if code in self.codes[type]:
                result += name
            else:
                result += '~~{0}~~'.format(name)

            result += separator

        return result[:-len(separator)]

    def set_data(self, codes, names):
        self.codes = codes
        self.names = names

    def unit_info(self, unit_type):
        res = ''
        for unit in self.units[unit_type].values():
            res += self._unpack(unit, 'units', ' -> ') + '\n'
        return res

    def tech_info(self, unit_type, attack_type, armour_type, has_internal_techs, has_university_techs):
        attack = armour = internal = university = ''

        if attack_type:
            attack = '\nАтака: ' + self._unpack(self.blacksmith[attack_type], 'techs', ' -> ')
        if armour_type:
            armour = '\nЗащита: ' + self._unpack(self.blacksmith[armour_type], 'techs', ' -> ')
        if unit_type and has_internal_techs:
            internal = '\nТехнологии: ' + self._unpack(self.techs[unit_type], 'techs', ', ')
        if unit_type and has_university_techs:
            university = '\nУнивер: ' + self._unpack(self.university[unit_type], 'techs', ', ')

        return attack + armour + internal + university




