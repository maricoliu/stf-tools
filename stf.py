#coding: utf-8
import requests
import json

STF_URL = 'https://stf.example.org'  #config your stf url

class STF():
    '''
    stf doc: https://github.com/openstf/stf/blob/master/doc/API.md#devices
    '''

    def __init__(self, token=None):
        self.token = token

        if not self.token:
            raise Exception('token can not be None.')

    def devices(self):
        '''
        Returns all STF devices information (including disconnected or otherwise inaccessible devices).
        :return: (list)
        '''
        url = STF_URL + '/api/v1/devices'
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        try:
            response = requests.get(url=url, headers=headers, verify=False).json()
        except Exception, e:
            raise Exception(e)

        devices = []
        for device in response['devices']:
            device_info = {
                'model': device.get('model'),
                'manufacturer': device.get('manufacturer'),
                'serial': device.get('serial'),
                'ready': device.get('ready'),
                'using': device.get('using'),
                'remoteConnect': device.get('remoteConnect'),
                'remoteConnectUrl': device.get('remoteConnectUrl')
            }
            devices.append(device_info)
        return devices

    def device(self, serial):
        '''
        Returns information about a specific device.
        :param serial: (str) device serial
        :return: (dict)
        '''
        url = STF_URL + '/api/v1/devices/' + serial
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        try:
            response = requests.get(url=url, headers=headers, verify=False).json()
        except Exception, e:
            raise Exception(e)
        device = response['device']
        device_info = {
            'model': device.get('model'),
            'manufacturer': device.get('manufacturer'),
            'serial': device.get('serial'),
            'ready': device.get('ready'),
            'using': device.get('using'),
            'remoteConnect': device.get('remoteConnect'),
            'remoteConnectUrl': device.get('remoteConnectUrl')
        }
        return device_info

    def use_device(self, serial):
        '''
        Attempts to add a device under the authenticated user's control.
        This is analogous to pressing "Use" in the UI.
        :param serial: (str) device serial
        :return: (dict)
        '''
        url = STF_URL + '/api/v1/user/devices'
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        payload = {
            'serial': serial
        }
        try:
            requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
        except Exception, e:
            raise Exception(e)


    def stop_use_device(self, serial):
        '''
        Removes a device from the authenticated user's device list.
        This is analogous to pressing "Stop using" in the UI.
        :param serial: (str) device serial
        :return: (dict)
        '''
        url = STF_URL + '/api/v1/user/devices/' + serial
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        try:
            requests.delete(url=url, headers=headers, verify=False)
        except Exception, e:
            raise Exception(e)


    def connect_device(self, serial):
        '''
        Allows you to retrieve the remote debug URL (i.e. an adb connectable address) for a device the authenticated user controls.

        Note that if you haven't added your ADB key to STF yet, the device may be in unauthorized state after connecting to it for the first time.
        We recommend you make sure your ADB key has already been set up properly before you start using this API.
        You can add your ADB key from the settings page, or by connecting to a device you're actively using in the UI and responding to the dialog that appears.
        :param serial: (str) device serial
        :return: (str) remoteConnectUrl
        '''
        url = STF_URL + '/api/v1/user/devices/{serial}/remoteConnect'.format(serial=serial)
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        try:
            response = requests.post(url, headers=headers, verify=False).json()
            if response['success']:
                return response['remoteConnectUrl']
            else:
                print 'Device is not owned by you or is not available'
                return None
        except Exception, e:
            raise Exception(e)


    def disconnect_device(self, serial):
        '''
        Disconnect a remote debugging session.
        :param serial: (str) device serial
        :return:
        '''
        url = STF_URL + '/api/v1/user/devices/{serial}/remoteConnect'.format(serial=serial)
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        try:
            response = requests.delete(url=url, headers=headers, verify=False).json()
            if response['success']:
                print 'Device remote disconnected successfully'
                return True
            else:
                print 'Device is not owned by you or is not available'
                return False
        except Exception, e:
            raise Exception(e)


if __name__ == '__main__':
    import time
    token = 'xx-xxxx-xx'
    
    stf = STF(token)
    devices =  stf.devices()

    serial = 'NX529J'
    stf.use_device(serial)

    #device_info = stf.device(serial)
    #remote_connect_url = device_info['remoteConnectUrl']

    remote_connect_url = stf.connect_device(serial)
    print remote_connect_url
    stf.connect_device(serial)
    time.sleep(10)
    stf.disconnect_device(serial)
    stf.stop_use_device(serial)


