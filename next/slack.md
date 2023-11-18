### `SLACK_CLIENT_ID`

To set up Slack authentication, you need to
[register your app](https://api.slack.com/apps/new). When you do so, you’ll  be
asked to provide a callback URL. You’ll want to provide:

```
http://localhost:8002/accounts/slack/login/callback/
http://DOMAIN.TLD/accounts/slack/login/callback/
```

Remember to replace `DOMAIN.TLD` with your actual domain name.

When you’ve done that, you’ll be given a client ID, a secret, and a key. Save
the client ID in this variable, the secret in `SLACK_SECRET`, and the key in
`SLACK_KEY`.

### `SLACK_SECRET`

When you register your app, you’ll be given a secret. Save it in this variable.

### `SLACK_KEY`

When you register your app, you’ll be given a key. Save it in this variable.
