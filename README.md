LineEmoji
====

## Overview
Convert text to LineEmoji
![demo](./images/demo.png)

Fake notification  
![fake](https://user-images.githubusercontent.com/16555696/45687850-c92f4780-bb8a-11e8-99a3-dd6e101cf51e.PNG)
## Requirements
- python3
- requests
- Yahoo デベロッパーネットワーク appid

## Usage
```python
from LineEmoji.Emoji import Emoji
emoji = Emoji('your Yahoo app id')
text = emoji.convert(string="これはテストです。This is a test.", fake_notification="これは通知には表示されるが実際のメッセージは変化しない。")
print(text)
```
## Install
``` 
git clone https://github.com/k0tayan/LineEmoji.git
```
## Licence

[MIT](https://github.com/k0tayan/LineEmoji/blob/master/LICENSE)

## Author

[k0tayan](https://twitter.com/kotayan_0415)
