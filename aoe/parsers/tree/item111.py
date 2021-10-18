class TreeItem:

    def get_lang_code(self, name, strings):
        for code, string in strings:
            if name.lower() in string.lower():
                return code
        return None


