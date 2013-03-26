from pattern import web


class AskMetafilterPost(object):
  def __init__(self, title=None, source=None, timestamp=None, comments=None):
    """An Ask Metafilter post."""
    self.title = title              # Post title (plaintext).
    self.source = source            # Post HTML content.
    self.timestamp = timestamp      # When the post was made.
    self.comments = comments or []  # List of comments.

  def plaintext(self):
    return plaintext(self.source)

  @staticmethod
  def _parse_from_html(html_str):
    html_str = decode_utf8(html_str)
    post = AskMetafilterPost()
    html = BeautifulSoup.BeautifulSoup(html_str)
    # Title
    h1 = html.find('h1', attrs={'class': 'posttitle'})
    post.title = h1.contents[0]
    # Timestamp
    # There seem to be at least two styles; First we try to parse
    # as the early style.
    date_str = u"%s" % (h1.next,)
    time_str = u"%s" % (h1.find('span', attrs={'class': 'smallcopy'}).next)
    time_str = time_str.replace("&nbsp;", "")
    timestamp_str = date_str + " " + time_str.strip()
    # 'December 8, 2003  1:28 PM  '
    try:
      timestamp = datetime.datetime.strptime(timestamp_str, "%B %d, %Y  %I:%M %p")
      post.timestamp = timestamp
    except ValueError:
      timestamp_str = unicode(h1.find('span', attrs={'class': 'smallcopy'}).contents[0])
      timestamp_str = timestamp_str.replace("&nbsp;", "").strip()
      timestamp = datetime.datetime.strptime(timestamp_str, "%B %d, %Y %I:%M %p")
      post.timestamp = timestamp
    # Question
    div = h1.findNextSibling('div', attrs={'class': 'copy'})
    c = u""
    for item in div.contents:
      c = c + u"%s" % (item,)
      if isinstance(item, BeautifulSoup.Tag) and item.name == u'div':
        break
    post.source = c
    # Comments
    for div in html.findAll('div', attrs={'class': lambda c: c and (c == u'comments' or c == u'comments best')}):
      if div.find('span', attrs={'class': 'smallcopy'}):
        post.comments.append(AskMetafilterComment._parse_from_html(div))
    return post


class AskMetafilterComment(object):
    def __init__(self, source=None, best_answer=False):
        self.source = source
        self.best_answer = best_answer

    def plaintext(self):
        return plaintext(self.source)

    @staticmethod
    def _parse_from_html(div):
        c = u""
        for item in div.contents:
            if isinstance(item, BeautifulSoup.Tag) and item.name == u"span" and item['class'] == u"smallcopy":
                break
            c = c + u"%s" % (item,)
        comment = AskMetafilterComment()
        comment.source = c
        comment.best_answer = (set(div['class'].split()) == set([u'comments', u'best']))
        span = div.find('span', attrs={'class': 'smallcopy'})
        return comment


def strip_between(a, b, string):
    """ Removes anything between (and including) string a and b inside the given string.
    """
    p = "%s.*?%s" % (a, b)
    p = re.compile(p, re.DOTALL | re.I)
    return re.sub(p, "", string)

def strip_javascript(html):
    return strip_between("<script.*?>", "</script>", html)
def strip_inline_css(html):
    return strip_between("<style.*?>", "</style>", html)
def strip_comments(html):
    return strip_between("<!--", "-->", html)
def strip_forms(html):
    return strip_between("<form.*?>", "</form>", html)


def plaintext(html, keep=[], replace=blocks, linebreaks=2, indentation=False):
  """ Returns a string with all HTML tags removed.
      Content inside HTML comments, the <style> tag and the <script> tags is removed.
      - keep        : a list of tags to keep. Element attributes are stripped.
                      To preserve attributes a dict of (tag name, [attribute])-items can be given.
      - replace     : a dictionary of (tag name, (replace_before, replace_after))-items.
                      By default, block-level elements are followed by linebreaks.
      - linebreaks  : the maximum amount of consecutive linebreaks,
      - indentation : keep left line indentation (tabs and spaces)?
  """
  if not keep.__contains__("script"):
    html = strip_javascript(html)
  if not keep.__contains__("style"):
    html = strip_inline_css(html)
  if not keep.__contains__("form"):
    html = strip_forms(html)
  if (not keep.__contains__("comment") and
      not keep.__contains__("!--")):
    html = strip_comments(html)
  html = html.replace("\r", "\n")
  html = strip_tags(html, exclude=keep, replace=replace)
  html = decode_entities(html)
  html = collapse_spaces(html, indentation)
  html = collapse_tabs(html, indentation)
  html = collapse_linebreaks(html, linebreaks)
  html = html.strip()
  return html
