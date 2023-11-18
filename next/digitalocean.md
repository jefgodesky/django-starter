### `DIGITALOCEAN_CLIENT_ID`

To set up Digital Ocean authentication, you need to
[register your app](https://cloud.digitalocean.com/settings/applications).
When you do so, you’ll  be asked to provide a callback URL. You’ll want to
provide:

```
http://localhost:8002/accounts/digitalocean/login/callback/
http://DOMAIN.TLD/accounts/digitalocean/login/callback/
```

Remember to replace `DOMAIN.TLD` with your actual domain name.

When you’ve done that, you’ll be given a client ID, a secret, and a key. Save
the client ID in this variable, the secret in `DIGITALOCEAN_SECRET`, and the
key in `DIGITALOCEAN_KEY`.

### `DIGITALOCEAN_SECRET`

When you register your app, you’ll be given a secret. Save it in this variable.

### `DIGITALOCEAN_KEY`

When you register your app, you’ll be given a key. Save it in this variable.
