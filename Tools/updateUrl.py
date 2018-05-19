import leancloud
from datetime import datetime

leancloud.init("ene47sdq2i57smk1vmmn8u05x1am9hjskq8poz9f1om6d7t4",
               "e01cu3fln3kal14ibjtwthkvgfgoazcd679ha0icwqx0ehx9")


def update_url(begin_time):
    Post = leancloud.Object.extend('Post')
    query = leancloud.Query('Post')
    query.add_ascending('createdAt')
    query.limit(1000)
    query.greater_than('createdAt', begin_time)
    posts = query.find()
    if len(posts) <= 0:
        return
    print(posts[len(posts) - 1].get('createdAt'))
    _posts = []
    for post in posts:
        content = post.get('content')
        if not content:
            continue
        content = content.replace('ac-ene47sdq', 'lc-ene47sdq').\
            replace('dn-ene47sdq', 'lc-ene47sdq').\
            replace('.qbox.me', '.cn-n1.lcfile.com').\
            replace('.clouddn.com', '.cn-n1.lcfile.com')
        if content != post.get('content'):
            post.set('content', content)
            _posts.append(post)
    if len(_posts) > 0:
        try:
            Post.save_all(_posts)
        except Exception:
            {}
    if len(posts) == 1000:
        return update_url(posts[999].get('createdAt'))


if __name__ == '__main__':
    update_url(datetime(2016, 10, 12))
