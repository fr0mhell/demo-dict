class DemoDict:
    _initial_size = 8

    def __init__(self, **kwargs):
        # array that stores hash table indexes of insertion
        self._locators_list = [None] * self._initial_size
        # hash table
        self._table = []

        for key, value in kwargs.items():
            self._add_item(key, value)

    @property
    def _locator_list_size(self):
        """Size of locators list."""
        return len(self._locators_list)

    @property
    def _next_table_index(self):
        """Index of table row to insert new item."""
        return len(self)

    def _add_item(self, key, value):
        if len(self) > self._locator_list_size / 2:
            self._double_locator_list()

        locator_index, table_index = self._get_locator_index_and_table_row_index_by_key(key)

        if table_index is None:
            self._locators_list[locator_index] = self._next_table_index
            self._table.append([hash(key), key, value])
        else:
            self._table[table_index] = [hash(key), key, value]

    def _double_locator_list(self):
        """Doubles locator list with empty cells."""
        self._locators_list += [None] * self._locator_list_size

    def _get_locator_index_and_table_row_index_by_key(self, key, locator_index=None):
        """Get locator index and hash table row number by key.

        Resolve hash collision using open addressing and linear probing with step equal to 1.
        https://en.wikipedia.org/wiki/Hash_table#Open_addressing

        """
        if locator_index is None:
            locator_index = hash(key) % self._locator_list_size

        table_row_index = self._locators_list[locator_index]

        if table_row_index is None:
            return locator_index, table_row_index

        old_hash, old_key, old_value = self._table[table_row_index]
        if old_hash is not None and old_key == key:
            return locator_index, table_row_index

        # Perform linear probing - check next locator index
        locator_index = (locator_index + 1) % self._locator_list_size
        return self._get_locator_index_and_table_row_index_by_key(key, locator_index)

    def items(self):
        return [(key, value) for _, key, value in self._table]

    def keys(self):
        return [key for _, key, _ in self._table]

    def values(self):
        return [value for _, _, value in self._table]

    def update(self, obj=None, **kwargs):
        if obj:
            keys_method = getattr(obj, 'keys')
            if callable(keys_method):
                for key in obj.keys():
                    self[key] = obj[key]
            else:
                for key, value in obj:
                    self[key] = value

        for key, value in kwargs.items():
            self[key] = value

    def __len__(self):
        return sum(i is not None for i in self._locators_list)

    def __getitem__(self, item):
        locator_index, table_index = self._get_locator_index_and_table_row_index_by_key(item)

        if table_index is None:
            raise KeyError(f'Key "{item}" not found')

        hash_value, key, value = self._table[table_index]
        return value

    def __setitem__(self, key, value):
        self._add_item(key, value)

    def __iter__(self):
        for _, key, _ in self._table:
            yield key

    def __delitem__(self, key):
        locator_index, table_index = self._get_locator_index_and_table_row_index_by_key(key)

        if table_index is None:
            raise KeyError(f'Key "{key}" not found')

        self._locators_list[locator_index] = None
        self._table[table_index] = [None, None, None]

