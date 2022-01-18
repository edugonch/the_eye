# the_eye

An Event has a category, a name and a payload of data (the payload can change according to which event an Application is sending)
  Structure for this:
   {
    category: string,
    name: string,
    payload: {}
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
