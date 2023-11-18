### `AUTH0_CLIENT_ID`

To set up Auth0 authentication, you need to
[register your app](https://manage.auth0.com/#/clients). When you do so, you’ll
be asked to provide a callback URL. You’ll want to provide:

```
http://localhost:8002/accounts/auth0/login/callback/
http://DOMAIN.TLD/accounts/auth0/login/callback/
```

Remember to replace `DOMAIN.TLD` with your actual domain name.

When you’ve done that, you’ll be given a client ID, a secret, and a key. Save
the client ID in this variable, the secret in `AUTH0_SECRET`, and the key in
`AUTH0_KEY`.

### `AUTH0_SECRET`

When you register your app, you’ll be given a secret. Save it in this variable.

### `AUTH0_KEY`

When you register your app, you’ll be given a key. Save it in this variable.

### `AUTH0_DOMAIN`

Specify the base URL for your Auth0 domain in this variable.
