import pytest

from vi import Vi


# noinspection PyMissingOrEmptyDocstring,PyTypeChecker
class TestVI(object):
    """Test class for VI -> ctypes conversion."""

    def test_array_uint8(self):
        assert Vi.array_uint8(255)
        assert Vi.array_uint8(255, 255)
        with pytest.raises(ValueError):
            Vi.array_uint8('')

    def test_array_float(self):
        assert Vi.array_float(255)
        assert Vi.array_float(255, 255)
        with pytest.raises(ValueError):
            Vi.array_float('')

    def test_char(self):
        assert Vi.char(255)
        with pytest.raises(ValueError):
            assert Vi.char('')

    def test_uint8(self):
        assert Vi.uint8(0).value == 0
        with pytest.raises(ValueError):
            assert Vi.uint8('')

    def test_int16(self):
        assert Vi.int16(0).value == 0
        with pytest.raises(ValueError):
            assert Vi.int16('')

    def test_uint16(self):
        assert Vi.uint16(0).value == 0
        with pytest.raises(ValueError):
            assert Vi.uint16('')

    def test_int32(self):
        assert Vi.int32(0).value == 0
        with pytest.raises(ValueError):
            assert Vi.int32('')

    def test_uint32(self):
        assert Vi.uint32(0).value == 0
        with pytest.raises(ValueError):
            assert Vi.uint32('')

    def test_real64(self):
        assert Vi.real64(0).value == 0
        with pytest.raises(ValueError):
            assert Vi.real64('')

    def test_boolean(self):
        assert Vi.boolean(0).value == 0
        assert Vi.boolean(False).value == 0
        assert Vi.boolean(Vi.FALSE).value == 0
        assert Vi.boolean(1).value == 1
        assert Vi.boolean(True).value == 1
        assert Vi.boolean(Vi.TRUE).value == 1
        with pytest.raises(ValueError):
            assert Vi.boolean('')

    def test_object(self):
        assert Vi.object(0).value == 0
        with pytest.raises(ValueError):
            assert Vi.object('')

    def test_session(self):
        assert Vi.session(0).value == 0
        assert Vi.session(Vi.NULL).value == 0
        with pytest.raises(ValueError):
            assert Vi.session('')

    def test_status(self):
        assert Vi.status(0).value == 0
        with pytest.raises(ValueError):
            assert Vi.status('')

    def test_string(self):
        assert Vi.string(255, b'abcdefghijklmnopqrstuvwxyz1234567890').value == b'abcdefghijklmnopqrstuvwxyz1234567890'
        with pytest.raises(ValueError):
            # string longer than allocated buffer
            Vi.string(0, b'1')
        with pytest.raises(ValueError):
            Vi.string('', 1)

    def test_rsrc(self):
        assert Vi.rsrc(255, b'abcdefghijklmnopqrstuvwxyz1234567890').value == b'abcdefghijklmnopqrstuvwxyz1234567890'
        assert Vi.rsrc(255, 'abcdefghijklmnopqrstuvwxyz1234567890').value == b'abcdefghijklmnopqrstuvwxyz1234567890'
        with pytest.raises(ValueError):
            # string longer than allocated buffer
            Vi.rsrc(0, b'1')
        with pytest.raises(ValueError):
            Vi.rsrc('', 1)
