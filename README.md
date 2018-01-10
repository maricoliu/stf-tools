# stf-tools
This a python util allows you to reserve and release any STF device

## STF

[STF]: https://github.com/openstf/stf
[STF API]: https://github.com/openstf/stf/blob/master/doc/API.md

STF project and api document are avaliable from below:

*STF github: <https://github.com/openstf/stf>  

*STF API: <https://github.com/openstf/stf/blob/master/doc/API.md>


## Usage
According to STF API, you need get token firstly. If you don't know how to get token, please refer to [Authentication]. 

[Authentication]: https://github.com/openstf/stf/blob/master/doc/API.md#authentication
``` python	
#coding: utf-8
from stf_tools import STF
	
# Your STF's url, like: https://stf.example.org
STF_URL = ""
```

### Example Code
#### Basic usage
Get all the devices information on the STF
```python	
serial = 'NX529J'
token = 'xx-xxx-xx'
stf = STF(token)
devices =  stf.devices()
print devices
```

Get specific devices information on the STF
```python	
device_info = stf.device(serial)
print device_info['remoteConnectUrl']
```

Use a device. This is analogous to pressing "Use" in the UI.
```python	
stf.use_device(serial)
```

Retrieve the remote debug URL
```python	
remote_connect_url = stf.connect_device(serial)
print remote_connect_url
```

Disconnect a remote debugging session.
```python	
stf.disconnect_device(serial)
```

Stop use device. This is analogous to pressing "Stop using" in the UI.
```python	
stf.stop_use_device(serial)
```
