# discord-wait-list-bot

## Summary

This is a bot to create a waitlist for a discord server. 

The bot allows users to refer other users with a `/refer`. Once a user has been referred and they have joined the server, the bot will give them the proper role. 

The server must be configured so the default role users have gives them access to only a few channels (role 1). Another role must be configured to allow full access to the server (role 2). The bot will move referred users from role 1 to role 2 after they join the server.


## Details

- The bot has 2 commands:
1. `/refer $USERNAME` which adds $USERNAME to the waitlist 
    - A confirmation message is printed with the entered username after the user has been added
2. `/check_wl` which can be used to see the current wait list
    - This command is set up to be used by users of a specific role.

A cron job will run periodically to check members of the server to see if they are on the wait list. If they are, the user is given a role and removed from the waitlist. 

The waitlist is saved to a file that is updated everytime someone is added or removed and the file is loaded up when the bot boots up so if it goes down, the list is safe.

## To Do:
1. Only check users in the server who do not currently have the relevant role
2. Instead of checking users in the server, check the wait list and see if users from the wait list have joined yet.
3. Add a cron job to prune wait list of old referrals
4. Create permanent log of when referrals are made and when they are accepted
  - Likely possible to view from the server audit logs but this could make the data more easily accessible
