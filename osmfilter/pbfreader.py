#
import sys, zlib, struct, itertools

from collections import namedtuple

import osmfilter.osmformat_pb2 as osmformat_pb2
import osmfilter.fileformat_pb2 as fileformat_pb2






if sys.version_info.major >= 3:
    from itertools import accumulate
elif sys.version_info.major == 2 and sys.version_info.minor >= 7:
    # itertools.accumulate is not available in python 2.7
    import operator

    def accumulate(iterable, func=operator.add):
        'Return running totals'
        it = iter(iterable)
        total = next(it)
        yield total
        for element in it:
            total = func(total, element)
            yield total
else:
    raise RuntimeError('Unsupported python version')



def decode_strmap(primitive_block):
    '''Decodes the bytes in the stringtable of `primitive_block` to UTF-8.'''
    return tuple(s.decode('utf8') for s in primitive_block.stringtable.s)


def iter_blocks(file):
    '''Iterates tuples `(offset, header)` for each block in the `file`.'''
    ofs = 0
    while True:
        file.seek(ofs)
        data = file.read(4)
        if len(data) < 4:
            return
        header_size, = struct.unpack('>I', data)
        header = fileformat_pb2.BlobHeader()
        header.ParseFromString(file.read(header_size))
        ofs += 4 + header_size
        yield ofs, header
        ofs += header.datasize


def read_blob(file, ofs, header):
    '''Read and decompress a openstreetmap blob from `file`.'''
    file.seek(ofs)
    blob = fileformat_pb2.Blob()
    blob.ParseFromString(file.read(header.datasize))
    if blob.raw:
        return blob.raw
    elif blob.zlib_data:
        return zlib.decompress(blob.zlib_data)
    else:
        raise ValueError('lzma blob not supported')


def parse_tags(strmap, keys_vals):
    tags = {}
    is_value = False
    for idx in keys_vals:
        if idx == 0:
            yield tags
            tags = {}
        elif is_value:
            tags[key] = strmap[idx]
            is_value = False
        else:
            key = strmap[idx]
            is_value = True


def iter_nodes(block, strmap, group):
    dense = group.dense
    if not dense:
        raise ValueError('Only dense nodes are supported')
    granularity = block.granularity or 100
    lat_offset = block.lat_offset or 0
    lon_offset = block.lon_offset or 0
    coord_scale = 0.000000001
    id = lat = lon = tag_pos = 0
    for did, dlat, dlon, tags in zip(
            dense.id, dense.lat, dense.lon,
            parse_tags(strmap, dense.keys_vals)):
        id += did
        lat += coord_scale * (lat_offset + granularity * dlat)
        lon += coord_scale * (lon_offset + granularity * dlon)
        yield (id, tags, (lon, lat))


def iter_ways(block, strmap, group):
    for way in group.ways:
        tags = {
            strmap[k]: strmap[v]
            for k, v in zip(way.keys, way.vals)
        }
        refs = tuple(accumulate(way.refs))
        yield way.id, refs, tags


def iter_relations(block, strmap, group):
    namemap = {}
    for relation in group.relations:
        tags = {
            strmap[k]: strmap[v]
            for k, v in zip(relation.keys, relation.vals)
        }
        refs = tuple(accumulate(relation.memids))
        members = [
            (
                ref,
                namemap.setdefault(
                    rel_type, osmformat_pb2.Relation.MemberType.Name(rel_type)),
                strmap[sid]
            )
            for ref, rel_type, sid in zip(
                    refs, relation.types, relation.roles_sid)
        ]

        yield relation.id, members, tags


Node = namedtuple('Node', ('id', 'tags', 'lonlat'))
Way = namedtuple('Way', ('id', 'tags', 'refs'))
Relation = namedtuple('Relation', ('id', 'tags', 'members'))


def read_entries(block):
    strmap = decode_strmap(block)
    for group in block.primitivegroup:
        for id, tags, lonlat in iter_nodes(block, strmap, group):
            yield Node(id, tags, lonlat)

        for id, refs, tags in iter_ways(block, strmap, group):
            yield Way(id, tags, refs)

        for id, members, tags in iter_relations(block, strmap, group):
            yield Relation(id, tags, members)


def read_pbf(file):
    for ofs, header in iter_blocks(file):
        block = osmformat_pb2.PrimitiveBlock()
        block.ParseFromString(read_blob(file, ofs, header))
        yield header, read_entries(block)


def file_query(file):
    if type(file) is str:
        file = open(file, 'rb')

    def query(query_func, *args, **kwargs):
        for header, entries in read_pbf(file):
            for entry in entries:
                if query_func(entry, *args, **kwargs):
                    yield entry

    return query


def filter_file_block(filename, ofs, header, filter_func, args, kwargs):
    with open(filename, 'rb') as file:
        entries = osmformat_pb2.PrimitiveBlock()
        entries.ParseFromString(read_blob(file, ofs, header))
        return [
            entry
            for entry in read_entries(entries)
            if filter_func(entry, *args, **kwargs)
        ]


def pool_file_query(pool, file):
    if type(file) is str:
        file = open(file, 'rb')

    blocks = [(file.name, ofs, header) for ofs, header in iter_blocks(file)]

    def query(query_func, *args, **kwargs):
        entry_lists = pool.starmap(filter_file_block, [
            block + (query_func, args, kwargs) for block in blocks
        ])
        return itertools.chain(*(entries for entries in entry_lists))

    return query
