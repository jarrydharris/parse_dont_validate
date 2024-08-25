from main import Metadata, MetadataParser


class TestParseMetadata__apply:
    def it_should_update_fields_given_matching_keys(self):
        
        
        with open("./simple_key_value.csv", "r") as fp:
            metadata: Metadata = MetadataParser().parse_text_io(fp)

        assert metadata.key_1 == "value_1"
        assert metadata.key_2 == "value_2"

    