### `LINKEDIN_CLIENT_ID`

To set up LinkedIn authentication, you need to
[register your app](https://www.linkedin.com/secure/developer?newapp=).
**Make sure you register an OAuth 2.0 app, not an OAuth 1.0a app!**
When you do so, you’ll  be asked to provide a callback URL. You’ll want to
provide:

```
http://localhost:8002/accounts/linkedin/login/callback/
http://DOMAIN.TLD/accounts/linkedin/login/callback/
```

Remember to replace `DOMAIN.TLD` with your actual domain name.

When you’ve done that, you’ll be given a client ID, a secret, and a key. Save
the client ID in this variable, the secret in `LINKEDIN_SECRET`, and the key
in `LINKEDIN_KEY`.

### `LINKEDIN_SECRET`

When you register your app, you’ll be given a secret. Save it in this variable.

### `LINKEDIN_KEY`

When you register your app, you’ll be given a key. Save it in this variable.
