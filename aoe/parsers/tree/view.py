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
        self._set_data(civ_codes, data_names)
        units = self._unit_info('archery')
        techs = self._tech_info('archery', 'arc_att', 'arc_arm', True, True)
        return units + techs

    def barrack(self, civ_codes, data_names):
        self._set_data(civ_codes, data_names)
        units = self._unit_info('barrack')
        techs = self._tech_info('barrack', 'inf_att', 'inf_arm', True, False)
        return units + techs

    def stable(self, civ_codes, data_names):
        self._set_data(civ_codes, data_names)
        units = self._unit_info('stable')
        techs = self._tech_info('stable', 'inf_att', 'cav_arm', True, False)
        return units + techs

    def siege(self, civ_codes, data_names):
        self._set_data(civ_codes, data_names)
        units = self._unit_info('siege')
        techs = self._tech_info('siege', None, None, False, True)
        return units + techs

    def dock(self, civ_codes, data_names):
        self._set_data(civ_codes, data_names)
        units = self._unit_info('dock')
        return units

    def monastery(self, civ_codes, data_names):
        self._set_data(civ_codes, data_names)
        techs = self._tech_info('monastery', None, None, True, False)
        return techs

    # function get tuple of unit type (example Archer has tuple of 3 units ),
    # format into line "Archer sep Crossbowman sep Arbalester" sep = separator
    # and add discord cross out symbols if unit isn't available for selected civ
    # parameters:
    #   data - tuple of codes in one line of tech tree e.g. stable archers line
    #   data_type - type of data codes e.g. 'units' or 'techs'
    #   separator of result elements
    def _unpack(self, data, data_type, separator):
        result = ''
        named_data = {code: self.names[data_type][str(code)] for code in data}

        for code, name in named_data.items():
            if code in self.codes[data_type]:
                result += name
            else:
                result += '~~{0}~~'.format(name)

            result += separator

        return result[:-len(separator)]

    def _set_data(self, codes, names):
        self.codes = codes
        self.names = names

    def _unit_info(self, unit_type):
        res = ''
        for unit in self.units[unit_type].values():
            res += self._unpack(unit, 'units', ' -> ') + '\n'
        return res

    def _tech_info(self, unit_type, attack_type, armour_type, has_internal_techs, has_university_techs):
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
