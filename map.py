import pygame, numpy

hash_tiles = {}

def ignore_flips(tile_a, tile_b):
	hash_tiles[tile_a] = 42
	if (pygame.surfarray.pixels2d(tile_a) == pygame.surfarray.pixels2d(tile_b)).all():
		return (False, False)

def compute_hash(t):
	hash_tiles[t] = numpy.sum(pygame.surfarray.pixels2d(t).flatten())

def check_flips(tile_a, tile_b):
	if tile_b not in hash_tiles:
		compute_hash(tile_b)
	compute_hash(tile_a)
	if hash_tiles[tile_a] == hash_tiles[tile_b]:
		surfarray_a = pygame.surfarray.pixels2d(tile_a)
		surfarray_b = pygame.surfarray.pixels2d(tile_b)
		if (surfarray_a == surfarray_b).all():
			return (False, False)
		elif (surfarray_a[::-1, :] == surfarray_b).all():
			return (True, False)
		elif (surfarray_a[:, ::-1] == surfarray_b).all():
			return (False, True)
		elif (surfarray_a[::-1, ::-1] == surfarray_b).all():
			return (True, True)			


class PTile():
	def __init__(self, tileset, id_, hflip, vflip):
		self.tileset = tileset
		self.id_ = id_
		self.hflip = hflip
		self.vflip = vflip
	
	def __str__(self):
		res = "[Tile #%d" % self.id_
		if self.hflip:
			res += ", hflip"
		if self.vflip:
			res += ", vflip"
		res += "]"
		return res
	
	def __repr__(self):
		return str(self)


class PTiledMap():
	def __init__(self, map_, tileset):
		self.width = len(map_[0])
		self.height = len(map_)
		self.map = map_
		self.tileset = tileset

	def get_size(self):
		return (self.width, self.height)


	@staticmethod
	def from_surface(surf, size, compare_fun = ignore_flips, tileset = []):

		tile_w, tile_h = size

		w = surf.get_width()
		h = surf.get_height()
		
		tw, th = w // tile_w, h // tile_h
		
		map_ = []

		for y in range(th):
			map_row = []
			for x in range(tw):
				# print (x, y),
				tile = surf.subsurface((x * tile_w, y * tile_h, 
										tile_w, tile_h))
				
				if any(pygame.PixelArray(tile)):
					for i, candidate in enumerate(tileset):
						c = compare_fun(tile, candidate)
						if c:
							hf, vf = c
							map_row += [PTile(tileset, i, hf, vf)]
							break
					else:
						map_row += [PTile(tileset, len(tileset), False, False)]
						tileset += [tile]
			map_ += [map_row]

		nb_tiles = len(tileset)
		
		return PTiledMap(map_, tileset)


def tileset_to_surface(tileset, tiles_per_row = 16):
	if tileset == []:
		return None

	tile_width, tile_height = tileset[0].get_size()

	th = len(tileset) // tiles_per_row
	if tiles_per_row * th < len(tileset):
		th += 1
	
	surf = pygame.Surface((tiles_per_row * tile_width, th * tile_height), pygame.SRCALPHA)
	
	x = y = 0
	for tile in tileset:
		surf.blit(tile, (x, y))
		x += tile_width
		if x >= tiles_per_row * tile_width:
			x = 0
			y += tile_height

	return surf

def export_tileset(tileset, path, tiles_per_row = 16):
	surf = tileset_to_surface(tileset, tiles_per_row)
	if surf:
		pygame.image.save(surf, path)
	return surf


if __name__ == '__main__':
	from tmx import *
	
	image = pygame.image.load('test/test.png')

	tiled = PTiledMap.from_surface(image, (8, 8), check_flips)
	export_tileset(tiled.tileset, 'test/tileset.png')

	print (tiled.map)
	
	save_as_tmx(tiled, 'test/test_tmx.tmx')
	exit()
	
	tileset = []
	patterns = []
	for tile in tiled.tileset:
		t = PTiledMap.from_surface(tile, (8, 8), check_flips, tileset = patterns)
		tileset += [t.map]
	
	export_tileset(patterns, 'test/patterns.png')
	print (tileset)
