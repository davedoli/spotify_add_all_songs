# Python script to add liked songs and saved albums in one playlist

Remember when spotify had the amazing idea of changing the behavior of saving albums. Instead of adding those songs in the album to liked songs, it stopped doing that. Not only did it ruin everyone's library organization, but also means that as you shuffle through your liked songs, you'll never hear the songs that are in saved albums.\
\
This scripts fixes that problem by adding all the songs from all your saved albums, with all the songs in your liked songs playlist into one playlist.
1. Create an spotify developer account.
2. Create an app in the spotify developer dashboard
3. Add a Redirect URI to the app settings, I just used http://127.0.0.1:9090 for example
4. Create a credentials.yaml that contains your client ID, client secret, the Redirected URI, and your spotify user ID(found in the app you created)
5. run script, and you'll find a playlist of all your saved songs in one playlist!

