## Designing Flask-API for interfacing netconf device and Web-UI
Let's say we want to write a netconf task list (config and operation) application and we want to design a web service for it. The first thing to do is to decide what is the root URL to access this service. We could expose this service as:

```
http://[hostname]/api/v1.0/config
```
and
```
http://[hostname]/api/v1.0/operation
```

| **HTTP Method** | **URI**                              | **Action**  |
| --------------- |:------------------------------------:| :---------: |
| GET             | http://[hostname]/api/v1.0/config... | ........... |
| GET             | http://[hostname]/api/v1.0/config... | ........... |
| PUT             | http://[hostname]/api/v1.0/config... | ........... |

And with this we are basically done with the design part of our web service. All that is left is to implement it!

## Todo:
- [ ] Define scope scenario for automation
- [ ] Define YANG model for each device
- [ ] API Service
- [ ] Web-UI