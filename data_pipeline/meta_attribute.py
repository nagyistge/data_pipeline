# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from cached_property import cached_property

from data_pipeline._avro_payload import _AvroPayload


class MetaAttribute(object):
    """Messages flowing through data pipeline have a ability to contain an
    additional array of avro encoded payloads under the “meta” key.
    These avro encoded payloads are known as Meta Attributes within the
    data pipeline domain. Meta Attributes contains additional information
    about a particular message originating from a namespace and source.

    For example for messages coming from metrics source within yelp_web_metric
    namespace, we could include the web request itself as one of the
    Meta Attribute in that message.

    This is an base class to define a meta attribute. It serves 2 purposes:
    1. To define a new MetaAttribute, you need to inherit from this class
    and call the constructor of this class with `schema_id` and `payload_data`

    **Examples**:

        class ExampleMetaAttribute(MetaAttribute):

            def __init__(self, param1, param2):
                payload_data = {
                    "param1": param1,
                    "param2": param2
                }

                super(ExampleMetaAttribute, self).__init__(
                    schema_id=schema_id,
                    payload_data=payload_data
                )


    2. Create a MetaAttribute object from serialized MetaAttribute payload.

    **Examples**:

        MetaAttribute(schema_id=schema_id, payload=payload)

    Args:
        schema_id (int): Identifies the schema used to encode the payload.
        payload (bytes): Avro-encoded meta attribute - encoded with schema identified
            by `schema_id`. Either `payload` or `payload_data` must be
            provided but not both.
        payload_data (dict): The contents of meta attribute, which will be
            encoded with schema identified by `schema_id`.  Either `payload` or
            `payload_data` must be provided but not both.
        dry_run (boolean): When set to True, MetaAttribute will return a string
            representation of the payload, instead of the avro encoded MetaAttribute.
            Defaults to False.
    """

    def __init__(
        self,
        schema_id,
        payload=None,
        payload_data=None,
        dry_run=False
    ):
        self._avro_payload = _AvroPayload(
            schema_id=schema_id,
            payload=payload,
            payload_data=payload_data,
            dry_run=dry_run
        )

    @property
    def payload(self):
        return self._avro_payload.payload

    @property
    def payload_data(self):
        return self._avro_payload.payload_data

    @cached_property
    def schema_id(self):
        return self._avro_payload.schema_id

    @property
    def avro_repr(self):
        return {
            'schema_id': self.schema_id,
            'payload': self.payload
        }

    def _asdict(self):
        """ Helper method for simplejson encoding in the Tailer
        """
        return {
            'schema_id': self.schema_id,
            'payload_data': self.payload_data
        }

    def __repr__(self):
        return '{}'.format(self._asdict())
