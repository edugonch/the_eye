# the_eye

An Event has a category, a name and a payload of data (the payload can change according to which event an Application is sending)
  Structure for this:
   
  "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
  "category": "page interaction",
  "name": "pageview",
  "data": {
    xxxxxxx
  },
  "timestamp": "2021-01-01 09:15:27.243860"
}
Different types of Events (identified by category + name) can have different validations for their payloads
An Event is associated to a Session

Events in a Session should be sequential and ordered by the time they occurred
Add a timestamp to event creation

The Application sending events is responsible for generating the Session identifier
Session indentifyer commes from the client

Applications should be recognized as "trusted clients" to "The Eye"
CORS

Appllications can send events for the same session
Not too clear here ....
