![](https://github.com/dwnsdp/Smithy-PDA/blob/main/SmithyLogo.png?raw=true)

Smithy is a personal assistant, like Alexa, Google Assistant, or Siri but connecting to mostly FOSS services.
Smithy uses OpenAI tools to connect to any plugin you see fit. Though it comes with most plugins you will need out of the box.

How it works:
User asks a query
Smithy responds with JSON which contains a message, maybe an action, and a flag called continue
It sends the message to the User
It runs the action
If continue is true it feeds the output of the action back into smithy, else it gives the output to the user

Here are the addons I hope to create
- **Notes** - you configure a location containing .MD, or .TXT files.
	- Search: returns the whole note that the snippet was found in
	- Edit: Uses the LLM to find the note you means, then uses the LLM to return it, but with the edit made.
- **Tasks** - Integrates with CalDAV
	- Add: Uses the LLM to work out which of your lists you mean, unless there is only one
	- Complete: Uses the LLM to work out what task you need to tick off
	- Edit: Uses the LLM to work out what task you mean, then replaces
- **Calendar** - Integrates with CalDAV
	- Add: Takes Title, start time, end time, all day, etc...
	- Remove: Uses the LLM to work out what event you mean
	- Edit: Uses the LLM to work out what event you mean, then replaces
- **Remind** - Integrates with CalDAV - makes a new calendar of it's own called Reminders and then is basically just calendar events
	- Add
	- Remove
	- Edit
- **Timers** - stores a list of times to go off. notifies the client when a time is reached
	- Add
	- Remove
- **Time** - returns the current time
- **Weather** - returns the current weather, given a location
- **News** - returns top headlines from an RSS feed of your choice
- **Maps** - Integrates with Open Street Maps
	- Search: searches around the clients location for a certain thing, like pub, etc. When done gives a ping that you should be able to click and it will open in your default map app.
- **Whatsapp** - uses **pywhatkit**
	- Send: asks the LLM which contact you mean then sends the message
	- Check: if no arguments returns all unread messages. if an argument is given checks messages from that contact (using the LLM work out what contact you mean)
- **Contacts** - Uses CardDAV
	- Details: gets all details about a contact.
- **Web Search** - searches the web
- **URL** - curls a URL
