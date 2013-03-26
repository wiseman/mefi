import datetime

import BeautifulSoup
from pattern import web


def _is_tag(element, tagname):
  return isinstance(element, BeautifulSoup.Tag) and element.name == tagname


def _post_title(h1_element):
  # The title consists of everything up to the first <br>.
  title = u''
  for element in h1_element.contents:
    if _is_tag(element, 'br'):
      return title
    else:
      title += web.plaintext(unicode(element))


def _has_class(classname):
  def class_filter(c):
    return c and classname in c.split()
  return class_filter


class AskMetafilterPost(object):
  def __init__(self, title=None, source=None, timestamp=None, comments=None):
    """An Ask Metafilter post."""
    self.title = title              # Post title (plaintext).
    self.source = source            # Post HTML content.
    self.timestamp = timestamp      # When the post was made.
    self.comments = comments or []  # List of comments.

  def plaintext(self):
    return web.plaintext(self.source)

  @staticmethod
  def from_html(html):
    post = AskMetafilterPost()
    dom = BeautifulSoup.BeautifulSoup(html)
    # Title
    h1 = dom.find('h1', attrs={'class': 'posttitle'})
    post.title = _post_title(h1)
    # Timestamp
    # There seem to be at least two styles; First we try to parse
    # as the early style.
    date_str = unicode(h1.next)
    time_str = unicode(
      h1.find('span', attrs={'class': _has_class('smallcopy')}).next)
    time_str = time_str.replace('&nbsp;', '')
    timestamp_str = date_str + ' ' + time_str.strip()
    # 'December 8, 2003  1:28 PM  '
    try:
      timestamp = datetime.datetime.strptime(
        timestamp_str, '%B %d, %Y  %I:%M %p')
      post.timestamp = timestamp
    except ValueError:
      timestamp_str = unicode(
        h1.find('span', attrs={'class': _has_class('smallcopy')}).contents[0])
      timestamp_str = timestamp_str.replace('&nbsp;', '').strip()
      timestamp = datetime.datetime.strptime(
        timestamp_str, '%B %d, %Y %I:%M %p')
      post.timestamp = timestamp
    # Question
    div = h1.findNextSibling('div', attrs={'class': _has_class('copy')})
    c = u''
    for item in div.contents:
      c += unicode(item)
      if _is_tag(item, 'div'):
        break
    post.source = c
    # Comments
    for div in dom.findAll('div', attrs={'class': _has_class('comments')}):
      if div.find('span', attrs={'class': _has_class('smallcopy')}):
        post.comments.append(AskMetafilterComment.from_html(div))
    return post


class AskMetafilterComment(object):
  def __init__(self, source=None, best_answer=False):
    self.source = source
    self.best_answer = best_answer

  def plaintext(self):
    return web.plaintext(self.source)

  @staticmethod
  def from_html(div):
    c = u''
    for item in div.contents:
      if _is_tag(item, 'span') and 'smallcopy' in item['class'].split():
        break
      c += unicode(item)
    comment = AskMetafilterComment()
    comment.source = c
    comment.best_answer = (
      set(div['class'].split()) == set([u'comments', u'best']))
    return comment
