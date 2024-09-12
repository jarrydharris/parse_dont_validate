from main import Metadata, MetadataParser, InvalidUpdateError
import pytest

@pytest.fixture
def metadata() -> Metadata:
    return Metadata("a", "b")


class TestParseMetadata__parse_text_io:

    def should_update_fields_given_matching_keys(self, metadata):
        with open("./testcases/simple_key_value.csv", "r") as fp:
            MetadataParser(fp).parse_text_io(metadata)

        assert metadata.key_1 == "value_1"
        assert metadata.key_2 == "value_2"

    def should_raise_invalid_update_error_given_invalid_key(self, metadata):
        with open("./testcases/invalid_key_value.csv", "r") as fp, pytest.raises(InvalidUpdateError):
            MetadataParser(fp).parse_text_io(metadata)

    def should_ignore_out_of_format_lines(self, metadata):
        with open("./testcases/simple_key_value_with_oof_line.csv", "r") as fp:
            MetadataParser(fp).parse_text_io(metadata)

    def should_raise_invalid_update_error_if_fields_are_missing(self, metadata):
        with open("./testcases/missing_expected_field.csv", "r") as fp, pytest.raises(InvalidUpdateError):
            MetadataParser(fp).parse_text_io(metadata)


