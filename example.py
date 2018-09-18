from LineEmoji.Emoji import Emoji
emoji = Emoji('your Yahoo app id')
text = emoji.convert(string="これはテストです。This is a test.", fake_notification="これは通知には表示されるが実際のメッセージは変化しない。")
print(text)