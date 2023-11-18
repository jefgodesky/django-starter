### `REDDIT_CLIENT_ID`

To set up Reddit authentication, you need to
[register your app](https://www.reddit.com/prefs/apps/).
When you do so, you’ll  be asked to provide a callback URL. You’ll want to
provide:

```
http://localhost:8002/accounts/reddit/login/callback/
http://DOMAIN.TLD/accounts/reddit/login/callback/
```

Remember to replace `DOMAIN.TLD` with your actual domain name.

When you’ve done that, you’ll be given a client ID, a secret, and a key. Save
the client ID in this variable, the secret in `REDDIT_SECRET`, and the key in
`REDDIT_KEY`.

### `REDDIT_SECRET`

When you register your app, you’ll be given a secret. Save it in this variable.

### `REDDIT_KEY`

When you register your app, you’ll be given a key. Save it in this variable.

### `REDDIT_USERNAME`

Save your Reddit username in this variable.
