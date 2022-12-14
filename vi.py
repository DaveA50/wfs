# -*- coding: utf-8 -*-
"""Wrapper for interfacing with the Thorlabs Wavefront Sensor (WFS)."""
import ctypes

__version__ = '0.3.0'
__author__ = 'David Amrhein'
__email__ = 'davea50@gmail.com'


class Vi(object):
    """Container for ctypes conversion to Vi."""

    TRUE = 1
    FALSE = 0
    NULL = 0

    # noinspection PyCallingNonCallable, PyTypeChecker
    @staticmethod
    def array_uint8(x, y=None):
        """Create a 1 or 2 dimensional uint8 array with c_ubyte.

        Args:
            x (int): Size of array in X.
            y (int, optional): Size of array in Y.
        """
        if y is not None:
            return ((ctypes.c_ubyte * int(x)) * int(y))()
        else:
            return (ctypes.c_ubyte * int(x))()

    # noinspection PyCallingNonCallable, PyTypeChecker
    @staticmethod
    def array_float(x, y=None):
        """Create a 1 or 2 dimensional float array with c_float.

        Args:
            x (int): Size of array in X.
            y (int, optional): Size of array in Y.
        """
        if y is not None:
            return ((ctypes.c_float * int(x)) * int(y))()
        else:
            return (ctypes.c_float * int(x))()

    @staticmethod
    def char(n):
        """Create a char array of size n with create_string_buffer.

        Args:
            n (int): size of char array.
        """
        return ctypes.create_string_buffer(int(n))

    @staticmethod
    def uint8(n):
        """Create a uint with c_ubyte.

        Args:
            n (int): Binary8 unsigned char.
        """
        return ctypes.c_ubyte(int(n))

    @staticmethod
    def int16(n):
        """Create a int16 with c_short.

        Args:
            n (int): Binary16 short int.
        """
        return ctypes.c_short(int(n))

    @staticmethod
    def uint16(n):
        """Create a uint16 with c_ushort.

        Args:
            n (int): Binary16 unsigned short int.
        """
        return ctypes.c_ushort(int(n))

    @staticmethod
    def int32(n):
        """Create a int32 with c_long.

        Args:
            n (int): Binary32 long int.
        """
        return ctypes.c_long(int(n))

    @staticmethod
    def uint32(n):
        """Create a uint32 with c_ulong.

        Args:
            n (int): Binary32 unsigned long int.
        """
        return ctypes.c_ulong(int(n))

    @staticmethod
    def real64(n):
        """Create a real64 with c_double.

        Args:
            n (float): double, char*.
        """
        return ctypes.c_double(float(n))

    @staticmethod
    def boolean(n):
        """Create a boolean with Vi.uint16.

        Args:
            n (int): Vi.true or Vi.false.

        Returns:
            Vi.uint16(n)
        """
        if n is True:
            n = Vi.TRUE
        elif n is False:
            n = Vi.FALSE
        return Vi.uint16(int(n))

    @staticmethod
    def object(n):
        """Create an object with Vi.uint32.

        Args:
            n (int): Binary32 unsigned long int.

        Returns:
            Vi.uint32(n)
        """
        return Vi.uint32(n)

    @staticmethod
    def session(n):
        """Create a session with Vi.object.

        Args:
            n (int): Binary32 unsigned long int.

        Returns:
            Vi.object(n)
        """
        return Vi.object(n)

    @staticmethod
    def status(n):
        """Create a status with Vi.int32.

        Args:
            n (int): Binary32 long int.

        Returns:
            Vi.int32(n)
        """
        return Vi.int32(n)

    @staticmethod
    def string(n, s=b''):
        """Create a string with Vi.char.

        Args:
            n (int): size of char array.
            s (bytes): bytestring value.

        Returns:
            Vi.char(n).value = s
        """
        if isinstance(s, str):
            s = bytes(s.encode())
        str_buffer = Vi.char(n)
        str_buffer.value = s
        return str_buffer

    @staticmethod
    def rsrc(n, s=b''):
        """Create a resource with Vi.string.

        Args:
            n (int): size of char array.
            s (bytes): bytestring value.

        Returns:
            Vi.string(n, s)
        """
        return Vi.string(n, s)
