import json
import glob
import os
import zipfile


class MetaData:
    def __init__(self):
        self.metaVersion = 2
        self.emojis = []

    def addEmoji(self, fileName):
        emoji = Emoji()
        emoji.fileName = fileName
        emoji.emoji.name = os.path.splitext(os.path.basename(fileName))[0]
        self.emojis.append(emoji)


class Emoji:
    def __init__(self):
        self.fileName = ""
        self.downloaded = True
        self.emoji = self.EmojiSpecify()

    class EmojiSpecify:
        def __init__(self):
            self.name = ""
            self.category = None
            self.aliases = []
            self.license = None
            self.localOnly = False
            self.isSensitive = False
            self.roleIdsThatCanBeUsedThisEmojiAsReaction = []


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, MetaData) or isinstance(o, Emoji) or isinstance(o, Emoji.EmojiSpecify):
            return o.__dict__
        return json.JSONEncoder.default(self, o)


if __name__ == '__main__':
    data = MetaData()
    for name in glob.glob('./emojis/*.png'):
        data.addEmoji(os.path.basename(name))
    with open('./emojis/meta.json', 'w') as f:
        json.dump(data, f, cls=MyEncoder)
    compFile = zipfile.ZipFile('./emojis.zip', 'w', zipfile.ZIP_DEFLATED)
    for name in glob.glob('./emojis/*'):
        compFile.write(name, os.path.basename(name))
    compFile.close()
