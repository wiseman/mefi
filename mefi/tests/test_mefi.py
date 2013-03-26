import json
import os.path
import unittest

from mefi import mefi


MEFI_POSTS = [
  'ask-84133',
  'ask-85690',
  'ask-86070',
  'ask-111271',
  'ask-154202'
  ]


def post_paths():
  this_dir = os.path.dirname(__file__)
  for f in MEFI_POSTS:
    yield (os.path.join(this_dir, f + '.html'),
           os.path.join(this_dir, f + '.json'))


class TestParsing(unittest.TestCase):
  def test_parse(self):
    self.maxDiff = None
    for input_path, truth_path in post_paths():
      with open(input_path, 'rb') as html_file:
        post = mefi.AskMetafilterPost.from_html(html_file.read())
      with open(truth_path, 'rb') as truth_file:
        truth = json.loads(truth_file.read())
      self.assertEqual(post.title, truth['title'])
      self.assertEqual(repr(post.timestamp), truth['timestamp'])
      self.assertEqual(post.source, truth['source'])
      self.assertEqual(post.plaintext(), truth['plaintext'])
      self.assertEqual(len(post.comments), len(truth['comments']))
      for pc, tc in zip(post.comments, truth['comments']):
        self.assertEqual(pc.source, tc['source'])
        self.assertEqual(pc.plaintext(), tc['plaintext'])
        self.assertEqual(pc.best_answer, tc['best_answer'])
