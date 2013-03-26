import json
import sys

from mefi import mefi


def post_to_json(post):
  json_post = {}
  json_post['title'] = post.title
  json_post['timestamp'] = repr(post.timestamp)
  json_post['source'] = post.source
  json_post['plaintext'] = post.plaintext()
  json_post['comments'] = [comment_to_json(c) for c in post.comments]
  return json_post


def comment_to_json(comment):
  json_comment = {}
  json_comment['plaintext'] = comment.plaintext()
  json_comment['best_answer'] = comment.best_answer
  json_comment['source'] = comment.source
  return json_comment


def main(argv):
  for path in argv[1:]:
    with open(path, 'rb') as html_file:
      post = mefi.AskMetafilterPost.from_html(html_file.read())
    json_path = path.replace('.html', '.json')
    print 'Writing %s...' % (json_path,)
    with open(json_path, 'wb') as json_file:
      json_file.write(json.dumps(post_to_json(post), indent=4))


if __name__ == '__main__':
  main(sys.argv)
