### `APPLE_CLIENT_ID`

To set up Apple authentication, you need to
[register your app](https://developer.apple.com/account/resources/certificates/list).
When you do so, you’ll be asked to provide a callback URL. You’ll want to provide:

```
http://localhost:8002/accounts/apple/login/callback/
http://DOMAIN.TLD/accounts/apple/login/callback/
```

Remember to replace `DOMAIN.TLD` with your actual domain name.

When you’ve done that, you’ll be given a service identifier, a key ID, and a
member ID or app ID. Save the serivce identifier in this variable, the key ID in
`APPLE_SECRET`, and the prefix of your app ID in `APPLE_KEY`.

### `APPLE_SECRET`

When you register your app, you’ll be given a “key ID.” Save that in this
variable.

### `APPLE_KEY`

When you register your app, you’ll be given a member ID or app ID. You should
be able to find it below your name, in the top right corner of the page, or as
the prefix of your app ID. Save that in this variable.

### `APPLE_CERTIFICATE_KEY`

Besides registering your app, you also need to
[create a private key](https://developer.apple.com/account/resources/authkeys/list).
This will be a long, cryptographic block. Remember, to write multi-line tet to
an environment variable like this, you’ll need to:

- Use double quotes at the beginning and end of the key.
- Use a backslash at the end of each line, followed by an actual line break.

It should look something like this:

```
APPLE_CERTIFICATE_KEY="-----BEGIN PRIVATE KEY-----\
s3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr\
3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3\
c3ts3cr3t\
-----END PRIVATE KEY-----\
"
```
