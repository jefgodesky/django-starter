### `GOOGLE_CLIENT_ID`

To set up Google authentication, you need to
[register your app](https://console.developers.google.com/).
When you do so, you’ll  be asked to provide a callback URL. You’ll want to
provide:

```
http://localhost:8002/accounts/google/login/callback/
http://DOMAIN.TLD/accounts/google/login/callback/
```

Remember to replace `DOMAIN.TLD` with your actual domain name.

When you’ve done that, you’ll be given a client ID, a secret, and a key. Save
the client ID in this variable, the secret in `GOOGLE_SECRET`, and the key in
`GOOGLE_KEY`.

### `GOOGLE_SECRET`

When you register your app, you’ll be given a secret. Save it in this variable.

### `GOOGLE_KEY`

When you register your app, you’ll be given a key. Save it in this variable.
