from map import export_tileset
import os

def save_as_tmx(map_, path):
	tileset = map_.tileset
	tile_w, tile_h = tileset[0].get_size()
	
	dir_name, base_name = os.path.split(path)
	base_name, _ = os.path.splitext(base_name)

	tw, th = map_.get_size()
	tileset_surf = export_tileset(tileset, '%s/%s.png' % (dir_name, base_name))
	tileset_width, tileset_height = tileset_surf.get_size()

	res = ('<?xml version="1.0" encoding="UTF-8"?>\n'
	'<map version="1.0" orientation="orthogonal" width="%d" height="%d" tilewidth="%d" tileheight="%d">\n'
	' <tileset firstgid="1" name="tiles" tilewidth="%d" tileheight="%d">\n'
	'  <image source="%s.png" width="%d" height="%d"/>\n'
	' </tileset>\n') % (tw, th, tile_w, tile_h, 
						tile_w, tile_h, base_name, tileset_width, tileset_height)

	res += (' <layer name="layer 0" width="%d" height="%d">\n'
	'  <data>\n') % (tw, th)
	
	i = 0
	for row in map_.map:
		for tile in row:
			t_id = tile.id_ + 1
			if tile.hflip:
				t_id += 0x80000000
			if tile.vflip:
				t_id += 0x40000000            
			res += '   <tile gid="%d"/>\n' % t_id
			i += 1
	
	res += ('  </data>\n'
	' </layer>\n')
	
	res += '</map>\n'
	
	with open('%s/%s.tmx' % (dir_name, base_name), 'w') as f:
		f.write(res)
