import feedparser, re
from feed_to_json import json_handle
feedparser.SANITIZE_HTML = False

SOUNDCLOUD = 0
YOUTUBE = 1

def parse_feed(url):
  feed = feedparser.parse(url)
  objs = []
  for entry in feed.entries:
    obj = {}
    if entry.content is not None and entry.content[0] is not None:
      if "soundcloud" in entry.content[0].value and "iframe" in entry.content[0].value:
        match = re.search(r'tracks%2F(.*?)&amp;', entry.content[0].value)
        obj['player_id'] = SOUNDCLOUD
        obj['title'] = entry.title
        obj['pub_date'] = entry.published;
        if match:
          obj['song_id'] = match.group(1).split('/')[0]
        else:
          match = re.search(r'tracks/(.*?)&', entry.content[0].value)
          if match:
            obj['song_id'] = match.group(1).split('/')[0]
      elif "youtube" in entry.content[0].value:
        obj['player_id'] = YOUTUBE
        obj['title'] = entry.title
        if "embed" in entry.content[0].value:
          youtube_id = entry.content[0].value.split('embed/')[1].split('?')[0].split('"')[0]
        else:
          match = re.search(r'v=(.*?)">',entry.content[0].value)
          if match:
            youtube_id = match.group(1)
        if youtube_id:
          obj['song_id'] = youtube_id
        obj['pub_date'] = entry.published;
      if obj != {} and 'song_id' in obj:
        objs.append(obj)
  return objs


if __name__ == "__main__":
  url = "http://thekollection.com/feed/" 
  parse_feed(url)
