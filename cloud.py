# coding: utf-8

# from leancloud import HttpsRedirectMiddleware
from leancloud import Engine
from leancloud import LeanEngineError
import leancloud
import os

from app import app

PhotoSet = leancloud.Object.extend('PhotoSet')
Photo = leancloud.Object.extend('Photo')


# 需要重定向到 HTTPS 可去除下一行的注释。
# app = HttpsRedirectMiddleware(app)
engine = Engine(app)


@engine.define
def hello(**params):
    uploadFileName()
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'


@engine.before_save('Todo')
def before_todo_save(todo):
    content = todo.get('content')
    if not content:
        raise LeanEngineError('内容不能为空')
    if len(content) >= 240:
        todo.set('content', content[:240] + ' ...')

def uploadFileName():
    path = '/Users/hugh/Projects/Feeling_Code/ToolProject/Upload-Python/static/wedding/'
    fileNames = os.listdir(path)
    print(fileNames)
    for fileName in fileNames:
        photoSet = PhotoSet()
        photoSet.set('tags', ['婚纱'])
        photoSet.set('title', '婚纱')
        print(fileName + ' uploading!')
        with open(path + fileName) as f:
            print(path + fileName)
            avatar = leancloud.File(fileName, f, 'image/jpeg')
            photo = Photo()
            photo.set('metaData', {
                "format": "jpeg",
                "height": 1365,
                "orientation": "Top-left",
                "colorModel": "ycbcr",
                "width": 2048
            })
            photo.set('photoFile', avatar)
            photo.save()
            photoSet.set('coverPhoto', photo)
            relation = photoSet.relation('photos')
            relation.add(photo)
            photoSet.save()
