import pytest

from rpcclient.darwin.consts import NSStringEncoding


@pytest.mark.darwin
def test_method_by_method_name(client):
    NSString = client.objc_get_class('NSString')
    ascii_encoding = NSStringEncoding.NSASCIIStringEncoding
    str1 = NSString.stringWithCString_encoding_('Taylor Swift', ascii_encoding).objc_symbol
    assert str1.cStringUsingEncoding_(ascii_encoding).peek_str() == 'Taylor Swift'
    assert str1.length == len('Taylor Swift')
    assert str1.lowercaseString().cStringUsingEncoding_(ascii_encoding).peek_str() == 'taylor swift'
    assert str1.uppercaseString().cStringUsingEncoding_(ascii_encoding).peek_str() == 'TAYLOR SWIFT'


@pytest.mark.darwin
def test_calling_property(client):
    d = client.symbols.objc_getClass('NSMutableDictionary').objc_call('new').objc_symbol
    # call method
    d.setObject_forKey_(client.cf('value'), client.cf('key'))
    # call property
    assert '{\n    key = value;\n}' == d.description.py
