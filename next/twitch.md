### `TWITCH_CLIENT_ID`

To set up Twitch authentication, you need to
[register your app](http://dev.twitch.tv/console). When you do so, you’ll be
asked to provide a callback URL. You’ll want to provide:

```
http://localhost:8002/accounts/twitch/login/callback/
http://DOMAIN.TLD/accounts/twitch/login/callback/
```

Remember to replace `DOMAIN.TLD` with your actual domain name.

When you’ve done that, you’ll be given a client ID, a secret, and a key. Save
the client ID in this variable, the secret in `TWITCH_SECRET`, and the key in
`TWITCH_KEY`.

### `TWITCH_SECRET`

When you register your app, you’ll be given a secret. Save it in this variable.

### `TWITCH_KEY`

When you register your app, you’ll be given a key. Save it in this variable.
