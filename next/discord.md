### `DISCORD_CLIENT_ID`

To set up Discord authentication, you need to
[register your app](https://discordapp.com/developers/applications/me).
When you do so, you’ll  be asked to provide a callback URL. You’ll want to
provide:

```
http://localhost:8002/accounts/discord/login/callback/
http://DOMAIN.TLD/accounts/discord/login/callback/
```

Remember to replace `DOMAIN.TLD` with your actual domain name.

When you’ve done that, you’ll be given a client ID, a secret, and a key. Save
the client ID in this variable, the secret in `DISCORD_SECRET`, and the key in
`DISCORD_KEY`.

### `DISCORD_SECRET`

When you register your app, you’ll be given a secret. Save it in this variable.

### `DISCORD_KEY`

When you register your app, you’ll be given a key. Save it in this variable.
