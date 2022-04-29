class DemoDict:

    def __init__(self, **kwargs):
        # array that stores hash table indexes of insertion
        self._locators_list = [None] * 8
        # Count dictionary items
        self._items_counter = 0
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
        return 0 if not self._table else len(self._table)

    def _add_item(self, key, value):
        if self._items_counter > self._locator_list_size / 2:
            self._locators_list += [None] * self._locator_list_size

        # TODO: check if locator index is already busy and resolve collision
        locator_index = hash(key) % self._locator_list_size
        self._locators_list[locator_index] = self._next_table_index

        self._table.append([
            hash(key),
            key,
            value,
        ])

    def items(self):
        for row in self._table:
            yield row[1], row[2]

    def __len__(self):
        return len(self._table)

    def __getitem__(self, item):
        locator_index = hash(item) % self._locator_list_size
        table_row_index = self._locators_list[locator_index]
        table_row = self._table[table_row_index]
        # TODO: check hash and resolve collision
        return table_row[2]

    def __setitem__(self, key, value):
        self._add_item(key, value)

