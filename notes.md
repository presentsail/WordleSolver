# 31 Mar 2022
 - In the interest of adding Python 3.9.6 to PATH, uninstalled 3.9.6 from laptop.
 - The version available on https://www.python.org/downloads/ was 3.10.4, so downloaded that and ticked the option to add it to PATH.

# 4 Apr 2022
 - How to open file in parent directory
```py
import os.path
filename = 'words.txt'
path = f'{os.path.dirname(__file__)}/../{filename}'
with open(path) as f:
    pass
```

or 

```py
open(os.path.join(os.path.dirname(__file__), os.pardir, 'filename.txt'))
```
