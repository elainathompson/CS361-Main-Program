import webbrowser

# data structures
# ===============

from enum import Enum
class UiState(Enum):
    HOME   = 1
    UNREAD = 2
    READ   = 3
    ALL    = 4
    ADD    = 5
    REMOVE = 6
    EXIT   = 7

# temporary hardcoded example data
# ================================

phony_feeds = [
    'https://foo.bar.com/atom.xml',
    'https://another.site/feed.xml',
]

phony_posts = [
    ('Phony Post 1', 'https://foo.bar.com/123321', 'https://foo.bar.com/atom.xml'),
    ('Phony Post 2', 'https://foo.bar.com/987654', 'https://foo.bar.com/atom.xml'),
    ('Phony Post 3', 'https://another.site/1',     'https://another.site/feed.xml'),
    ('Phony Post 4', 'https://another.site/2',     'https://another.site/feed.xml'),
]

phony_reads = {
    # 'https://foo.bar.com/123321': True,
    # 'https://another.site/2': True,
}

# global state
# ============

state    = UiState['HOME']
username = None
password = None

# ui routines
# ===========

def cmd_home():
    global state
    global username
    global password
    print('(1) Home\n')
    username = input('Username: ')
    password = input('Password: ')
    # TODO: actually authenticate
    print('')
    state = UiState['ALL']

def cmd_unread():
    global state
    print('(2) Unread Posts\n')
    # TODO: should sync from service
    count = 0
    urls = []
    for i in range(0, len(phony_posts)):
        post = phony_posts[i]
        if post[1] in phony_reads:
            continue
        count += 1
        print('{}: [ ] {}: {}'.format(count, post[0], post[1],))
        urls.append(post[1])
    if i > 0:
        print('')
    while True:
        cmd = input('open [1-{}], quit [q], all posts [a], read posts [r], add feed [+], remove feed [-]: '.format(count))
        print('')
        if   cmd == 'q': state = UiState['EXIT']; return
        elif cmd == 'a': state = UiState['ALL']; return
        elif cmd == 'r': state = UiState['READ']; return
        elif cmd == '+': state = UiState['ADD']; return
        elif cmd == '-': state = UiState['REMOVE']; return
        try:
            choice = int(cmd)
            url = urls[choice-1]
            # webbrowser.open(url)
            # TODO: should sync to service
            phony_reads[url] = True
            return
        except:
            print('Invalid choice, try again.')

def cmd_read():
    global state
    print('(3) Read Posts\n')
    # TODO: should sync from service
    count = 0
    urls = []
    for i in range(0, len(phony_posts)):
        post = phony_posts[i]
        if post[1] not in phony_reads:
            continue
        count += 1
        print('{}: [{}] {}: {}'.format(count, 'r', post[0], post[1],))
        urls.append(post[1])
    if i > 0:
        print('')
    while True:
        cmd = input('open [1-{}], quit [q], all posts [a], unread posts [u], add feed [+], remove feed [-]: '.format(count))
        print('')
        if   cmd == 'q': state = UiState['EXIT']; return
        elif cmd == 'a': state = UiState['ALL']; return
        elif cmd == 'u': state = UiState['UNREAD']; return
        elif cmd == '+': state = UiState['ADD']; return
        elif cmd == '-': state = UiState['REMOVE']; return
        try:
            choice = int(cmd)
            url = urls[choice-1]
            # webbrowser.open(url)
            # TODO: should sync to service
            phony_reads[url] = True
            return
        except:
            print('Invalid choice, try again.')

def cmd_all():
    global state
    print('(4) All Posts\n')
    # TODO: should sync from service
    i = 0
    while i < len(phony_posts):
        i += 1
        post = phony_posts[i-1]
        print('{}: [{}] {}: {}'.format(i,
              'r' if post[1] in phony_reads else ' ',
              post[0], post[1],))
    if i > 0:
        print('')
    while True:
        cmd = input('open [1-{}], quit [q], read posts [r], unread posts [u], add feed [+], remove feed [-]: '.format(i))
        print('')
        if   cmd == 'q': state = UiState['EXIT']; return
        elif cmd == 'r': state = UiState['READ']; return
        elif cmd == 'u': state = UiState['UNREAD']; return
        elif cmd == '+': state = UiState['ADD']; return
        elif cmd == '-': state = UiState['REMOVE']; return
        try:
            choice = int(cmd)
            url = phony_posts[choice-1][1]
            # webbrowser.open(url)
            # TODO: should sync to service
            phony_reads[url] = True
            return
        except:
            print('Invalid choice, try again.')


def cmd_add():
    global state
    print('(5) Add Feed\n')
    print('Enter a feed title and address.')
    title = input('Feed Title: ')
    url = input('Feed Address: ')
    phony_feeds.append(url)
    print('')
    state = UiState['REMOVE']

def cmd_remove():
    global state
    print('(7) Remove Feed\n')
    count = 0
    for feed in phony_feeds:
        count += 1
        print('{}: {}'.format(count, feed))
    print('')
    while True:
        cmd = input('remove [1-{}], quit [q], all posts [a], read posts [r], unread posts [u], remove feed [-]: '.format(count))
        print('')
        if   cmd == 'q': state = UiState['EXIT']; return
        elif cmd == 'a': state = UiState['ALL']; return
        elif cmd == 'r': state = UiState['READ']; return
        elif cmd == 'u': state = UiState['UNREAD']; return
        elif cmd == '-': state = UiState['REMOVE']; return
        try:
            choice = int(cmd)
            url = phony_feeds[choice-1]
            yn = input('warning! are you sure you want to delete feed "{}"?\n Any psots from this feed will be deleted. [y/n]:'.format(url))
            if yn == 'n':
                print("ok, nothing was deleted.")
                return
            elif yn == 'y':
                print("proceeding...")
            del phony_feeds[choice-1]
            i = 0
            while i < len(phony_posts):
                if phony_posts[i][2] == url:
                    phony_posts.pop(i)
                else:
                    i += 1
            return
        except:
            print('Invalid choice, try again.')

def cmd_main():
    global state
    state = UiState['HOME']
    while True:
        if   state == UiState['HOME']:   cmd_home()
        elif state == UiState['UNREAD']: cmd_unread()
        elif state == UiState['READ']:   cmd_read()
        elif state == UiState['ALL']:    cmd_all()
        elif state == UiState['ADD']:    cmd_add()
        elif state == UiState['REMOVE']: cmd_remove()
        elif state == UiState['EXIT']:   break

cmd_main()

