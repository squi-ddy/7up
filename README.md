# 7up Discord Bot
*A Discord Bot to play counting games!*

## Invite Link
Invite 7up to your Discord server using 
[this](https://discord.com/api/oauth2/authorize?client_id=995693780604817468&permissions=285615713344&scope=bot%20applications.commands)
link!

## Contributing
For type checking and code formatting with `format.sh`, install `requirements-dev.txt`. \
`requirements.txt` has the minimal packages required to run the bot.

If you want to implement a new counting game, simply implement all the functions in the
`CountingGame` ABC. 

## Running the Bot
### Using `docker-compose`
Make a `.env` file, and make sure `docker-compose.yml` points to it. \
`docker-compose up` should then run the bot.

### With Python
Make sure you have Python `3.10`. Install all the requirements in `requirements.txt`, 
then run the bot by running `main.py`.