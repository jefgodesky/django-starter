### `PATREON_CLIENT_ID`

To set up Patreon authentication, you need to
[register your app](https://www.patreon.com/portal/registration/register-clients).
When you do so, you’ll  be asked to provide a callback URL. You’ll want to
provide:

```
http://localhost:8002/accounts/patreon/login/callback/
http://DOMAIN.TLD/accounts/patreon/login/callback/
```

Remember to replace `DOMAIN.TLD` with your actual domain name.

When you’ve done that, you’ll be given a client ID, a secret, and a key. Save
the client ID in this variable, the secret in `PATREON_SECRET`, and the key in
`PATREON_KEY`.

### `PATREON_SECRET`

When you register your app, you’ll be given a secret. Save it in this variable.

### `PATREON_KEY`

When you register your app, you’ll be given a key. Save it in this variable.
