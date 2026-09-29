# Der Die Das – iPad app (TestFlight)

The app is the website bundled into a native iPad app with Capacitor, so it works offline and plays sound
even with the silent switch on. Every push that changes the site (`index.html`, `audio/`, `img/`, `data/`)
or `app/` builds a new version and uploads it to TestFlight automatically (`.github/workflows/testflight.yml`).

Bundle ID: `com.ohadnissim.derdiedas`

## One-time setup

1. **Register the bundle ID** – developer.apple.com → Certificates, IDs & Profiles → Identifiers → + → App IDs → App →
   Bundle ID (explicit) `com.ohadnissim.derdiedas`, description "Der Die Das". No extra capabilities needed.
2. **Create the app** – appstoreconnect.apple.com → Apps → + → New App: iOS, a name (must be unique on the
   App Store, e.g. "Mila – der die das"), language German, the bundle ID above, SKU `derdiedas`.
3. **API key** – App Store Connect → Users and Access → Integrations → App Store Connect API → Team Keys → +,
   name "GitHub", access **Admin** (needed so the build server can create the signing certificate).
   Download the `.p8` file (only possible once) and note the **Key ID** and the **Issuer ID** shown above the list.
4. **Team ID** – developer.apple.com → Account → Membership details → Team ID.
5. **GitHub secrets** – this repo → Settings → Secrets and variables → Actions → New repository secret:
   `APPLE_TEAM_ID`, `ASC_KEY_ID`, `ASC_ISSUER_ID`, and `ASC_KEY_P8` (open the .p8 in TextEdit and paste all of it,
   including the BEGIN/END lines).
6. **Run it** – Actions → TestFlight → Run workflow. About 10–15 minutes later the build shows up in
   App Store Connect → TestFlight (Apple needs a few more minutes to process it).
7. **Testers** – TestFlight → Internal Testing → + → group "Family", add yourself (and anyone else on the team),
   and turn on automatic distribution. On the iPad install the TestFlight app, sign in with that Apple ID, install.
   With TestFlight's automatic updates on, every new build lands on the iPad by itself.

## Building on the Mac instead

No Node or npm needed: the Xcode project has a "Copy website" build step that copies `index.html`, `audio/`, `img/`
and `data/` from the top of the repo into the app on every build.

```sh
git clone https://github.com/ohadnissim/DerDieDas.git
open DerDieDas/app/ios/App/App.xcodeproj
```
In Xcode: App target → Signing & Capabilities → tick "Automatically manage signing" and pick your team.
Then set the device to "Any iOS Device (arm64)", Product ▸ Archive → Distribute App → App Store Connect → Upload.
For later updates: `git pull` in the folder, raise the build number (App target → General → Build), archive again.
