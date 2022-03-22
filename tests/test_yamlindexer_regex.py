from yamlindexer import YamlIndex
import pytest


@pytest.mark.xfail
def test_extract_key():
    # empty key
    assert YamlIndex._extract_key(': value') is None
    assert YamlIndex._extract_key('   : value') is None
    # non-quoted
    assert YamlIndex._extract_key('key: value') == 'key'
    assert YamlIndex._extract_key('key-with-dashes: value') == 'key-with-dashes'
    assert YamlIndex._extract_key('key_with_underscores: value') == 'key_with_underscores'
    assert YamlIndex._extract_key('key with spaces: value') == 'key with spaces'
    assert YamlIndex._extract_key('key with spaces  : value') == 'key with spaces'
    # double quoted
    assert YamlIndex._extract_key('"key": value') == 'key'
    assert YamlIndex._extract_key('"key-2": value') == 'key-2'
    # single quoted
    assert YamlIndex._extract_key('\'key\': value') == 'key'
    assert YamlIndex._extract_key('\'key-2\': value') == 'key-2'
    # reject non root
    assert YamlIndex._extract_key(' key: value') is None
    assert YamlIndex._extract_key('   "key": value') is None
    assert YamlIndex._extract_key(' \'key\': value') is None
    # reject comments
    assert YamlIndex._extract_key('#key: value') is None
    assert YamlIndex._extract_key('   #"key": value') is None
    assert YamlIndex._extract_key('# \'key\': value') is None
    # reject anchors
    assert YamlIndex._extract_key('<<: *anchor') is None
    assert YamlIndex._extract_key('  <<: *anchor') is None


@pytest.mark.xfail
def test_extract_value():
    # empty value
    assert YamlIndex._extract_value('key:') is None
    assert YamlIndex._extract_value('key:      ') is None
    # special chars
    assert YamlIndex._extract_value('key:  ±!"#$%&/()=?*+\'00987654321§\\|-_.:,; ') == '±!"#$%&/()=?*+\'00987654321§\\|-_.:,;'
    assert YamlIndex._extract_value('key:  ±!   "#$%&/()=?*+\'00987654321§\\|-_.:, ; ') == '±!   "#$%&/()=?*+\'00987654321§\\|-_.:, ;'
    # non-quoted
    assert YamlIndex._extract_value('key: value') == 'value'
    assert YamlIndex._extract_value('key:    value') == 'value'
    assert YamlIndex._extract_value('key: value-with-dashes') == 'value-with-dashes'
    assert YamlIndex._extract_value('key: value with spaces') == 'value with spaces'
    assert YamlIndex._extract_value('key: value with spaces   ') == 'value with spaces'
    # double quoted
    assert YamlIndex._extract_value('key: "value"') == 'value'
    assert YamlIndex._extract_value('key: "value-2"') == 'value-2'
    # single quoted
    assert YamlIndex._extract_value('key: \'value\'') == 'value'
    assert YamlIndex._extract_value('key: \'value-2\'') == 'value-2'
    # reject non-basic types / multiline
    assert YamlIndex._extract_value('key: ["a", "b"]') is None
    assert YamlIndex._extract_value('key:    {"a": "b"}') is None
    assert YamlIndex._extract_value('key: |') is None
    assert YamlIndex._extract_value('key: |-') is None
    assert YamlIndex._extract_value('key: | ') is None
    assert YamlIndex._extract_value('key: >') is None
    assert YamlIndex._extract_value('key: > ') is None
