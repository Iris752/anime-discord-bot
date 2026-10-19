import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

JST = ZoneInfo('Asia/Tokyo')
WEEKDAYS = ['月', '火', '水', '木', '金', '土', '日']

def parse_time(value):
    hour, minute = map(int, value.split(':'))
    if not (0 <= hour <= 29 and 0 <= minute < 60):
        raise ValueError(f'Invalid broadcast time: {value}')
    return hour * 60 + minute

def main():
    webhook = os.environ.get('DISCORD_WEBHOOK_URL')
    if not webhook:
        raise RuntimeError('DISCORD_WEBHOOK_URL is missing')
    now = datetime.now(JST)
    # A 24:30 broadcast on Monday is Tuesday 00:30, but belongs to Monday's lineup.
    with Path(__file__).with_name('anime.json').open(encoding='utf-8') as f:
        entries = json.load(f)
    today = sorted((e for e in entries if e.get('enabled', False) and e.get('weekday') == now.weekday() and e.get('time')), key=lambda e: parse_time(e['time']))
    date_label = f'{now:%Y/%m/%d}（{WEEKDAYS[now.weekday()]}）'
    if today:
        lines = []
        for e in today:
            parse_time(e['time'])
            title = str(e['title']).replace('@', '＠')
            station = str(e.get('station', '未設定')).replace('@', '＠')
            url = str(e.get('url', ''))
            lines.append(f"**{e['time']}｜{title}**\n放送局・配信：{station}" + (f'\n{url}' if url.startswith('https://') else ''))
        body = '\n\n'.join(lines)
    else:
        body = '本日登録されている放送予定はありません。'
    # Discord message limit is 2000 characters. Split on entry boundaries.
    chunks, current = [], ''
    for block in (body.split('\n\n') if today else [body]):
        if len(block) > 1750:
            raise ValueError('One anime entry is too long')
        if current and len(current) + len(block) + 2 > 1750:
            chunks.append(current)
            current = block
        else:
            current = f'{current}\n\n{block}' if current else block
    if current:
        chunks.append(current)
    for i, chunk in enumerate(chunks, 1):
        heading = f'📺 **本日のアニメ放送予定｜{date_label}**'
        if len(chunks) > 1:
            heading += f'（{i}/{len(chunks)}）'
        payload = {'content': f'{heading}\n\n{chunk}', 'allowed_mentions': {'parse': []}}
        request = Request(webhook, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), headers={'Content-Type': 'application/json', 'User-Agent': 'anime-discord-notifier/1.0'}, method='POST')
        with urlopen(request, timeout=20) as response:
            if response.status not in (200, 204):
                raise RuntimeError(f'Discord returned HTTP {response.status}')
    print(f'Sent {len(today)} entries for {date_label}')

if __name__ == '__main__':
    main()
