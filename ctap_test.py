# Script for testing correctness of CTAP2/CTAP1 security token

from __future__ import print_function, absolute_import, unicode_literals

from fido2.hid import CtapHidDevice, CTAPHID
from fido2.client import Fido2Client
from fido2.ctap import CtapError
from fido2.ctap1 import CTAP1
from fido2.ctap2 import *
from fido2.cose import *
from fido2.utils import Timeout
import sys,os,time
from random import randint
from binascii import hexlify
import array,struct,socket

# Set up a FIDO 2 client using the origin https://example.com


def ForceU2F(client,device):
    client.ctap = CTAP1(device)
    client.pin_protocol = None
    client._do_make_credential = client._ctap1_make_credential
    client._do_get_assertion = client._ctap1_get_assertion


class Packet(object):
    def __init__(self,data):
        self.data = data

    def ToWireFormat(self,):
        return self.data

    @staticmethod
    def FromWireFormat(pkt_size,data):
        return Packet(data)



class Tester():
    def __init__(self,):
        self.origin = 'https://examplo.org'

    def find_device(self,):
        dev = next(CtapHidDevice.list_devices(), None)
        if not dev:
            raise RuntimeError('No FIDO device found')
        self.dev = dev
        self.ctap = CTAP2(dev)

        # consume timeout error
        cmd,resp = self.recv_raw()

    def send_data(self, cmd, data):
        #print('<<', hexlify(data))
        if type(data) != type(b''):
            data = struct.pack('%dB' % len(data), *[ord(x) for x in data])
        with Timeout(1.0) as event:
            return self.dev.call(cmd, data,event)

    def send_raw(self, data, cid = None):
        if cid is None:
            cid = self.dev._dev.cid
        elif type(cid) != type(b''):
            cid = struct.pack('%dB' % len(cid), *[ord(x) for x in cid])
        if type(data) != type(b''):
            data = struct.pack('%dB' % len(data), *[ord(x) for x in data])
        self.dev._dev.InternalSendPacket(Packet(cid + data))

    def cid(self,):
        return self.dev._dev.cid

    def set_cid(self,cid):
        if type(cid) not in [type(b''), type(bytearray())]:
            cid = struct.pack('%dB' % len(cid), *[ord(x) for x in cid])
        self.dev._dev.cid = cid

    def recv_raw(self,):
        cmd,payload = self.dev._dev.InternalRecv()
        return cmd, payload

    def check_error(self,data,err=None):
        assert(len(data) == 1)
        if err is None:
            if data[0] != 0:
                raise CtapError(data[0])
        elif data[0] != err:
            raise ValueError('Unexpected error: %02x' % data[0])


    def test_hid(self,):
        print('Test idle')
        try:
            cmd,resp = self.recv_raw()
        except socket.timeout:
            print('Pass: Idle')

        print('Test init')
        r = self.send_data(CTAPHID.INIT, '\x11\x11\x11\x11\x11\x11\x11\x11')

        pingdata = os.urandom(100)
        try:
            r = self.send_data(CTAPHID.PING, pingdata)
            if (r != pingdata):
                raise ValueError('Ping data not echo\'d')
        except CtapError as e:
            print('100 byte Ping failed:', e)
            raise RuntimeError('ping failed')
        print('PASS: 100 byte ping')

        pingdata = os.urandom(7609)
        try:
            t1 = time.time() * 1000
            r = self.send_data(CTAPHID.PING, pingdata)
            t2 = time.time() * 1000
            delt = t2 - t1
            #if (delt < 140 ):
                #raise RuntimeError('Fob is too fast (%d ms)' % delt)
            if (delt > 555):
                raise RuntimeError('Fob is too slow (%d ms)' % delt)
            if (r != pingdata):
                raise ValueError('Ping data not echo\'d')
        except CtapError as e:
            print('7609 byte Ping failed:', e)
            raise RuntimeError('ping failed')
        print('PASS: 7609 byte ping')


        try:
            r = self.send_data(CTAPHID.WINK, '')
            assert(len(r) == 0)
        except CtapError as e:
            print('wink failed:', e)
            raise RuntimeError('wink failed')
        print('PASS: wink')

        try:
            r = self.send_data(CTAPHID.WINK, 'we9gofrei8g')
            raise RuntimeError('Wink is not supposed to have payload')
        except CtapError as e:
            assert(e.code == CtapError.ERR.INVALID_LENGTH)
        print('PASS: malformed wink')

        try:
            r = self.send_data(CTAPHID.CBOR, '')
            raise RuntimeError('Cbor is supposed to have payload')
        except CtapError as e:
            assert(e.code == CtapError.ERR.INVALID_LENGTH)
        print('PASS: no data cbor')

        try:
            r = self.send_data(CTAPHID.MSG, '')
            raise RuntimeError('MSG is supposed to have payload')
        except CtapError as e:
            assert(e.code == CtapError.ERR.INVALID_LENGTH)
        print('PASS: no data msg')

        try:
            r = self.send_data(CTAPHID.INIT, '\x11\x22\x33\x44\x55\x66\x77\x88')
        except CtapError as e:
            raise RuntimeError('resync fail: ', e)
        print('PASS: resync')

        try:
            r = self.send_data(0x66, '')
            raise RuntimeError('Invalid command did not return error')
        except CtapError as e:
            assert(e.code == CtapError.ERR.INVALID_COMMAND)
        print('PASS: invalid HID command')


        print('Sending packet with too large of a length.')
        self.send_raw('\x80\x1d\xba\x00')
        cmd,resp = self.recv_raw()
        self.check_error(resp, CtapError.ERR.INVALID_LENGTH)
        print('PASS: invalid length')

        print('Sending packets that skip a sequence number.')
        self.send_raw('\x81\x10\x00')
        self.send_raw('\x00')
        self.send_raw('\x01')
        self.send_raw('\x02')
        # skip 3
        self.send_raw('\x04')
        cmd,resp = self.recv_raw()
        self.check_error(resp, CtapError.ERR.INVALID_SEQ)
        cmd,resp = self.recv_raw()
        assert(cmd == 0xbf) # timeout
        print('PASS: invalid sequence')

        print('Resync and send ping')
        try:
            r = self.send_data(CTAPHID.INIT, '\x11\x22\x33\x44\x55\x66\x77\x88')
            pingdata = os.urandom(100)
            r = self.send_data(CTAPHID.PING, pingdata)
            if (r != pingdata):
                raise ValueError('Ping data not echo\'d')
        except CtapError as e:
            raise RuntimeError('resync fail: ', e)
        print('PASS: resync and ping')

        print('Send ping and abort it')
        self.send_raw('\x81\x10\x00')
        self.send_raw('\x00')
        self.send_raw('\x01')
        try:
            r = self.send_data(CTAPHID.INIT, '\x11\x22\x33\x44\x55\x66\x77\x88')
        except CtapError as e:
            raise RuntimeError('resync fail: ', e)
        print('PASS: interrupt ping with resync')

        print('Send ping and abort it with different cid, expect timeout')
        oldcid = self.cid()
        newcid = '\x11\x22\x33\x44'
        self.send_raw('\x81\x10\x00')
        self.send_raw('\x00')
        self.send_raw('\x01')
        self.set_cid(newcid)
        self.send_raw('\x86\x00\x08\x11\x22\x33\x44\x55\x66\x77\x88')  # init from different cid
        cmd,r = self.recv_raw()  # init response
        assert(cmd == 0x86)
        self.set_cid(oldcid)
        cmd,r = self.recv_raw()  # timeout response
        assert(cmd == 0xbf)

        print('PASS: resync and timeout')


        print('Test timeout')
        self.send_data(CTAPHID.INIT, '\x11\x22\x33\x44\x55\x66\x77\x88')
        t1 = time.time() * 1000
        self.send_raw('\x81\x10\x00')
        self.send_raw('\x00')
        self.send_raw('\x01')
        cmd,r = self.recv_raw()  # timeout response
        t2 = time.time() * 1000
        delt = t2 - t1
        assert(cmd == 0xbf)
        assert(r[0] == CtapError.ERR.TIMEOUT)
        assert(delt < 1000 and delt > 400)
        print('Pass timeout')

        print('Test not cont')
        self.send_data(CTAPHID.INIT, '\x11\x22\x33\x44\x55\x66\x77\x88')
        self.send_raw('\x81\x10\x00')
        self.send_raw('\x00')
        self.send_raw('\x01')
        self.send_raw('\x81\x10\x00')   # init packet
        cmd,r = self.recv_raw()  # timeout response
        assert(cmd == 0xbf)
        assert(r[0] == CtapError.ERR.INVALID_SEQ)
        print('PASS: Test not cont')

        print('Check random cont ignored')
        self.send_data(CTAPHID.INIT, '\x11\x22\x33\x44\x55\x66\x77\x88')
        self.send_raw('\x01\x10\x00')
        cmd,r = self.recv_raw()  # timeout response
        assert(cmd == 0xbf)
        assert(r[0] == CtapError.ERR.TIMEOUT)

        print('Check busy')
        t1 = time.time() * 1000
        self.send_data(CTAPHID.INIT, '\x11\x22\x33\x44\x55\x66\x77\x88')
        oldcid = self.cid()
        newcid = '\x11\x22\x33\x44'
        self.send_raw('\x81\x10\x00')
        self.set_cid(newcid)
        self.send_raw('\x81\x10\x00')
        cmd,r = self.recv_raw()  # busy response
        t2 = time.time() * 1000
        assert(t2-t1 < 100)
        assert(cmd == 0xbf)
        assert(r[0] == CtapError.ERR.CHANNEL_BUSY)

        self.set_cid(oldcid)
        cmd,r = self.recv_raw()  # timeout response
        assert(cmd == 0xbf)
        assert(r[0] == CtapError.ERR.TIMEOUT)
        print('PASS: busy')

        print('Check busy interleaved')
        cid1 = '\x11\x22\x33\x44'
        cid2 = '\x01\x22\x33\x44'
        self.set_cid(cid2)
        self.send_data(CTAPHID.INIT, '\x11\x22\x33\x44\x55\x66\x77\x88')
        self.set_cid(cid1)
        self.send_data(CTAPHID.INIT, '\x11\x22\x33\x44\x55\x66\x77\x88')
        self.send_raw('\x81\x00\x63')   # echo 99 bytes first channel

        self.set_cid(cid2)  # send ping on 2nd channel
        self.send_raw('\x81\x00\x63')
        self.send_raw('\x00')

        self.set_cid(cid1)              # finish 1st channel ping
        self.send_raw('\x00')

        self.set_cid(cid2)
        cmd,r = self.recv_raw()  # busy response
        assert(cmd == 0xbf)
        assert(r[0] == CtapError.ERR.CHANNEL_BUSY)

        self.set_cid(cid1)
        cmd,r = self.recv_raw()  # ping response
        assert(cmd == 0x81)
        assert(len(r) == 0x63)

        cmd,r = self.recv_raw()  # timeout
        assert(cmd == 0xbf)
        assert(r[0] == CtapError.ERR.TIMEOUT)
        print('PASS: busy interleaved')


        print('Test idle')
        try:
            cmd,resp = self.recv_raw()
        except socket.timeout:
            print('Pass: Idle')

        print('Test cid 0 is invalid')
        self.set_cid('\x00\x00\x00\x00')
        self.send_raw('\x86\x00\x08\x11\x22\x33\x44\x55\x66\x77\x88', cid = '\x00\x00\x00\x00')
        cmd,r = self.recv_raw()  # timeout
        assert(cmd == 0xbf)
        assert(r[0] == CtapError.ERR.INVALID_CHANNEL)
        print('Pass: cid 0')

        print('Test invalid broadcast cid use')
        self.set_cid('\xff\xff\xff\xff')
        self.send_raw('\x81\x00\x08\x11\x22\x33\x44\x55\x66\x77\x88', cid = '\xff\xff\xff\xff')
        cmd,r = self.recv_raw()  # timeout
        assert(cmd == 0xbf)
        assert(r[0] == CtapError.ERR.INVALID_CHANNEL)
        print('Pass: cid broadcast')


if __name__ == '__main__':
    t = Tester()
    t.find_device()
    t.test_hid()


