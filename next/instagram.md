### `INSTAGRAM_CLIENT_ID`

To set up Instagram authentication, you need to
[register your app](https://www.instagram.com/developer/clients/manage/).
When you do so, you’ll  be asked to provide a callback URL. You’ll want to
provide:

```
http://localhost:8002/accounts/instagram/login/callback/
http://DOMAIN.TLD/accounts/instagram/login/callback/
```

Remember to replace `DOMAIN.TLD` with your actual domain name.

When you’ve done that, you’ll be given a client ID, a secret, and a key. Save
the client ID in this variable, the secret in `INSTAGRAM_SECRET`, and the key
in `INSTAGRAM_KEY`.

### `INSTAGRAM_SECRET`

When you register your app, you’ll be given a secret. Save it in this variable.

### `INSTAGRAM_KEY`

When you register your app, you’ll be given a key. Save it in this variable.
