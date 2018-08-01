import ctypes

import pytest

from vi import Vi


# noinspection PyMissingOrEmptyDocstring,PyTypeChecker
class TestVI(object):
    """Test class for VI -> ctypes conversion."""

    def test_array_uint8(self):
        assert Vi.array_uint8(255)
        assert Vi.array_uint8(255, 255)
        with pytest.raises(ValueError) as e:
            Vi.array_uint8('')
        Vi.log_vi.error(e)

    def test_array_float(self):
        assert Vi.array_float(255)
        assert Vi.array_float(255, 255)
        with pytest.raises(ValueError) as e:
            Vi.array_float('')
        Vi.log_vi.error(e)

    def test_char(self):
        assert Vi.char(255)
        default = Vi.char('')
        assert default.value == b''
        assert isinstance(default.value, bytes)

    def test_uint8(self):
        assert Vi.uint8(0).value == 0
        default = Vi.uint8('')
        assert default.value == 0
        assert isinstance(default, type(ctypes.c_ubyte(0)))

    def test_int16(self):
        assert Vi.int16(0).value == 0
        default = Vi.int16('')
        assert default.value == 0
        assert isinstance(default, type(ctypes.c_short(0)))

    def test_uint16(self):
        assert Vi.uint16(0).value == 0
        default = Vi.uint16('')
        assert default.value == 0
        assert isinstance(default, type(ctypes.c_ushort(0)))

    def test_int32(self):
        assert Vi.int32(0).value == 0
        default = Vi.int32('')
        assert default.value == 0
        assert isinstance(default, type(ctypes.c_long(0)))

    def test_uint32(self):
        assert Vi.uint32(0).value == 0
        default = Vi.uint32('')
        assert default.value == 0
        assert isinstance(default, type(ctypes.c_ulong(0)))

    def test_real64(self):
        assert Vi.real64(0).value == 0
        default = Vi.real64('')
        assert default.value == 0
        assert isinstance(default, type(ctypes.c_double(0)))

    def test_boolean(self):
        assert Vi.boolean(0).value == 0
        assert Vi.boolean(False).value == 0
        assert Vi.boolean(Vi.FALSE).value == 0
        assert Vi.boolean(1).value == 1
        assert Vi.boolean(True).value == 1
        assert Vi.boolean(Vi.TRUE).value == 1
        default = Vi.boolean('')
        assert default.value == 0
        assert isinstance(default, type(ctypes.c_ushort(0)))

    def test_object(self):
        assert Vi.object(0).value == 0
        default = Vi.object('')
        assert default.value == 0
        assert isinstance(default, type(ctypes.c_ulong(0)))

    def test_session(self):
        assert Vi.session(0).value == 0
        assert Vi.session(Vi.NULL).value == 0
        default = Vi.session('')
        assert default.value == 0
        assert isinstance(default, type(ctypes.c_ulong(0)))

    def test_status(self):
        assert Vi.status(0).value == 0
        default = Vi.status('')
        assert default.value == 0
        assert isinstance(default, type(ctypes.c_long(0)))

    def test_string(self):
        assert Vi.string(255, b'abcdefghijklmnopqrstuvwxyz1234567890').value == b'abcdefghijklmnopqrstuvwxyz1234567890'

    def test_rsrc(self):
        assert Vi.rsrc(255, b'abcdefghijklmnopqrstuvwxyz1234567890').value == b'abcdefghijklmnopqrstuvwxyz1234567890'
        assert Vi.rsrc(255, 'abcdefghijklmnopqrstuvwxyz1234567890').value == b'abcdefghijklmnopqrstuvwxyz1234567890'
        with pytest.raises(ValueError) as e:
            Vi.rsrc(0, b'1')
        Vi.log_vi.error(e)
        with pytest.raises(ValueError) as e:
            # defaults to 512 len char array
            Vi.rsrc('', b'1' * 513)
        Vi.log_vi.error(e)
        with pytest.raises(TypeError) as e:
            Vi.rsrc('', 1)
        Vi.log_vi.error(e)
