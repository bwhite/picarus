# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='picarus_search.proto',
  package='',
  serialized_pb='\n\x14picarus_search.proto\"\x91\x04\n\x0bSearchIndex\x12\x0c\n\x04name\x18\x01 \x02(\t\x12;\n\x0e\x66\x65\x61ture_format\x18\x02 \x01(\x0e\x32\x16.SearchIndex.SerFormat:\x0bJSON_IMPORT\x12\x0f\n\x07\x66\x65\x61ture\x18\x03 \x02(\x0c\x12\x38\n\x0bhash_format\x18\x04 \x01(\x0e\x32\x16.SearchIndex.SerFormat:\x0bJSON_IMPORT\x12\x0c\n\x04hash\x18\x05 \x02(\x0c\x12:\n\rmetric_format\x18\x06 \x01(\x0e\x32\x16.SearchIndex.SerFormat:\x0bJSON_IMPORT\x12\x0e\n\x06metric\x18\x07 \x02(\x0c\x12\x14\n\x0c\x66\x65\x61ture_dims\x18\x08 \x02(\x05\x12\x10\n\x08id_bytes\x18\t \x02(\x05\x12\x12\n\nhash_bytes\x18\n \x02(\x05\x12>\n\x0cindex_format\x18\x0b \x01(\x0e\x32\x18.SearchIndex.IndexFormat:\x0ePLANAR_HASH_ID\x12\x15\n\rcreation_time\x18\x0c \x01(\x01\x12\x10\n\x08part_num\x18\r \x01(\x05\x12\x11\n\tnum_parts\x18\x0e \x01(\x05\x12\r\n\x05index\x18\x0f \x01(\x0c\"(\n\tSerFormat\x12\x0f\n\x0bJSON_IMPORT\x10\x00\x12\n\n\x06PICKLE\x10\x01\"!\n\x0bIndexFormat\x12\x12\n\x0ePLANAR_HASH_ID\x10\x00')



_SEARCHINDEX_SERFORMAT = descriptor.EnumDescriptor(
  name='SerFormat',
  full_name='SearchIndex.SerFormat',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='JSON_IMPORT', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='PICKLE', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=479,
  serialized_end=519,
)

_SEARCHINDEX_INDEXFORMAT = descriptor.EnumDescriptor(
  name='IndexFormat',
  full_name='SearchIndex.IndexFormat',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='PLANAR_HASH_ID', index=0, number=0,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=521,
  serialized_end=554,
)


_SEARCHINDEX = descriptor.Descriptor(
  name='SearchIndex',
  full_name='SearchIndex',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='name', full_name='SearchIndex.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='feature_format', full_name='SearchIndex.feature_format', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='feature', full_name='SearchIndex.feature', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='hash_format', full_name='SearchIndex.hash_format', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='hash', full_name='SearchIndex.hash', index=4,
      number=5, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='metric_format', full_name='SearchIndex.metric_format', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='metric', full_name='SearchIndex.metric', index=6,
      number=7, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='feature_dims', full_name='SearchIndex.feature_dims', index=7,
      number=8, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='id_bytes', full_name='SearchIndex.id_bytes', index=8,
      number=9, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='hash_bytes', full_name='SearchIndex.hash_bytes', index=9,
      number=10, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='index_format', full_name='SearchIndex.index_format', index=10,
      number=11, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='creation_time', full_name='SearchIndex.creation_time', index=11,
      number=12, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='part_num', full_name='SearchIndex.part_num', index=12,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='num_parts', full_name='SearchIndex.num_parts', index=13,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='index', full_name='SearchIndex.index', index=14,
      number=15, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SEARCHINDEX_SERFORMAT,
    _SEARCHINDEX_INDEXFORMAT,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=25,
  serialized_end=554,
)

_SEARCHINDEX.fields_by_name['feature_format'].enum_type = _SEARCHINDEX_SERFORMAT
_SEARCHINDEX.fields_by_name['hash_format'].enum_type = _SEARCHINDEX_SERFORMAT
_SEARCHINDEX.fields_by_name['metric_format'].enum_type = _SEARCHINDEX_SERFORMAT
_SEARCHINDEX.fields_by_name['index_format'].enum_type = _SEARCHINDEX_INDEXFORMAT
_SEARCHINDEX_SERFORMAT.containing_type = _SEARCHINDEX;
_SEARCHINDEX_INDEXFORMAT.containing_type = _SEARCHINDEX;
DESCRIPTOR.message_types_by_name['SearchIndex'] = _SEARCHINDEX

class SearchIndex(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SEARCHINDEX
  
  # @@protoc_insertion_point(class_scope:SearchIndex)

# @@protoc_insertion_point(module_scope)
