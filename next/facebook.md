### `FACEBOOK_CLIENT_ID`

To set up Facebook authentication, you need to
[create an app](https://developers.facebook.com/apps).
When you do so, you can leave **App Domains** blank, but you should add
`http://localhost:8002` and your actual domain (with HTTPS) to
**Website with Facebook Login**.

When you’ve done that, you’ll be given a client ID, a secret, and a key. Save
the client ID in this variable, the secret in `FACEBOOK_SECRET`, and the key in
`FACEBOOK_KEY`.

### `FACEBOOK_SECRET`

When you register your app, you’ll be given a secret. Save it in this variable.

### `FACEBOOK_KEY`

When you register your app, you’ll be given a key. Save it in this variable.
