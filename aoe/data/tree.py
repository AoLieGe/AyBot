class TreeView:
    @staticmethod
    def get():
        return {
            'units': {
                'barrack': {
                    'militia': (74, 75, 77, 473, 567),
                    'spearman': (93, 358, 359),
                    'eagle': (753, 752),
                    'condotier': (882,),
                },

                'archery': {
                    'archer': (4, 24, 492),
                    'skirm': (7, 6, 1155),
                    'slinger': (185,),
                    'ca': (39, 474),
                    'cannoneer': (5,),
                    'genitour': (1010, 1012)
                },

                'stable': {
                    'scout': (448, 546, 441, 1707),
                    'knight': (38, 283, 569),
                    'camel': (329, 330, 207),
                    'elephant': (1132, 1134),
                    'lancer': (1370, 1372),
                    'xolotl': (1570,)
                },

                'siege': {
                    'ram': (1258, 422, 548),
                    'mangonel': (280, 550, 588),
                    'scorp': (279, 542),
                    'bombard': (36,),
                    'houfnice': (1709,),
                },

                'dock': {
                    'galley': (539, 21, 442),
                    'fireship': (1103, 529, 532),
                    'demolition': (1104, 527, 528),
                    'cannon': (420, 691)
                }
            },

            'techs': {
                'barrack': (215, 602, 716),

                'archery': (437, 436),

                'stable': (435, 39),

                'blacksmith': {
                    'inf_att': (67, 68, 75),
                    'arc_att': (199, 200, 201),
                    'inf_arm': (74, 76, 77),
                    'cav_arm': (81, 82, 80),
                    'arc_arm': (211, 212, 219)
                },

                'university': {
                    'archery': (47, 93),
                    'siege': (377,)
                },

                'monastery': (316, 319, 231, 252, 45, 233, 230, 438, 441, 439),

                'dock': (373, 374, 375)
            }
        }
