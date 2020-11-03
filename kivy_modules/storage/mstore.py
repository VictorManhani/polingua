from json import loads, dump

import os

class MStore:
    _data = {}
    _is_changed = False
    filename = ""
    indent = None
    sort_keys = False

    def __init__(self, *args, **kwargs):
        # self.filename = kwargs.get("filename", "")
        self.indent = kwargs.get("indent", None)
        self.sort_keys = kwargs.get("sort_keys", False)

    def __repr__(self):
        return str(self._data)

    def __setitem__(self, key, val):
        self._data[key] = val
        self.store_save()

    def __getitem__(self, key):
        return self.get(key)

    def __delitem__(self, key):
        return self.keys()

    def __contains__(self, key):
        return self.exists(key)

    def __len__(self):
        return self.count()

    def __iter__(self):
        for key in self.keys():
            yield key



    def get(self, key):
        '''Get the key-value pairs stored at `key`. If the key is not found, a
        `KeyError` exception will be thrown.
        '''
        return self.store_get(key)

    def keys(self):
        '''Return a list of all the keys in the storage.
        '''
        return self.store_keys()

    def exists(self, key):
        '''Check if a key exists in the store.
        '''
        return self.store_exists(key)

    def count(self):
        '''Return the number of entries in the storage.
        '''
        return self.store_count()



    def store_get(self, key):
        return self._data[key]

    def store_exists(self, key):
        return key in self._data

    def store_load(self, filename):
        """Get the file and open as dict, if not exists, create it."""
        try:
            self.filename = filename

            if not os.path.isfile(self.filename):
                self.store_save()

            with open(self.filename, 'r', encoding="utf-8") as fd:
                self._data = fd.read()
                if not self._data:
                    self._data = "{}"
                self._data = loads(self._data)
        except Exception as e:
            raise Exception(f"Error {str(e)}")

    def store_save(self):
        """Save dict in file."""
        try:
            with open(self.filename, 'w', encoding="utf-8") as fd:
                dump(
                    self._data, fd, ensure_ascii = False,
                    indent=self.indent, sort_keys=self.sort_keys)
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

    def store_put(self, key, value):
        self._data[key] = value
        self._is_changed = True
        return True

    def store_delete(self, key):
        del self._data[key]
        self._is_changed = True
        self.store_save()
        return True

    def store_find(self, filters):
        for key, values in iter(self._data.items()):
            found = True
            for fkey, fvalue in iter(filters.items()):
                if fkey not in values:
                    found = False
                    break
                if values[fkey] != fvalue:
                    found = False
                    break
            if found:
                yield key, values

    def store_count(self):
        return len(self._data)

    def store_keys(self):
        return list(self._data.keys())
