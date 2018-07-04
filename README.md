# 概要
TLに流れてきたモチに反応するbotです
Twitter→ [@mochimochi__bot](https://twitter.com/mochimochi__bot)

具体的な機能は

- タイムラインに流れてきた「モチ」「もち」「ﾓﾁ」に対していいねをつけ、リプライを送ります
- 自分に対するメンションにはモチが含まれていなくても反応します
- 定期的にモチモチツイートをします
- 自動でフォローバックをします

# 仕組み
Heroku上にデプロイして動かしています
実際に稼働しているのは`main.py`です
中身は
- `mochi_stream.py`でタイムラインを取得→反応
- `regular_tweet.py`で定期ツイート
- `auto_follow.py`で自動フォロバ