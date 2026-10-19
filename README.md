# Discord アニメ放送通知BOT

日本時間の毎日12時に、`anime.json` に登録した当日放送アニメだけを Discord Webhook へ通知します。Python標準ライブラリのみ使用。

## 導入
1. GitHubでリポジトリを作成（公開・非公開どちらでも可）。このフォルダの内容を、`.github/workflows/daily.yml` を含めてアップロード。
2. Discordの通知先チャンネル → チャンネル設定 → 連携サービス → ウェブフック でURLを発行。
3. GitHubのリポジトリ → Settings → Secrets and variables → Actions → New repository secret。Nameを `DISCORD_WEBHOOK_URL`、SecretにWebhook URLを入力。
4. `anime.json` を実際の作品に書き換える。`weekday` は月曜=0、火曜=1、…日曜=6。`time` は24:30のような深夜表記も使用可能（前日の放送枠として扱う）。
5. Actions → Daily Anime Notification → Run workflow で手動テスト。成功すれば以降毎日12時頃に通知。

## 注意
- `anime.json` はサンプルです。実際の放送情報は自動取得しません。クール切り替え時に手動更新してください。
- 地上波・BS・配信で放送日時が異なります。登録した時刻・曜日に基づき通知します。
- GitHub Actions の定期実行は遅延・スキップの可能性があり、12:00ちょうどの保証はありません。
- Webhook URLをコードや公開リポジトリに書かないでください。
- 手動テストでもその日の投稿が実際に送信されます。


## 24作品の設定（2026-10-19）
24作品すべてを anime.json に登録済み。公式放送時刻を確認できた4作品のみ enabled=true。残り20作品は enabled=false とし、曜日・時間を確認後に設定してください。現在の実装は手動登録した放送枠の曜日通知で、休止・特番・配信限定作品の更新には自動追従しません。深夜24時以降は前日の放送枠として扱います。
