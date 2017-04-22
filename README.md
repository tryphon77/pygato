# pygatool
PYGAme TOOLset to generate ressources for games

Bibliothèque de petites fonctions pour faciliter la manipulation et la génération de ressources graphiques ou autres.

map.py : création et manipulation de cartes
	PTile : représente une tile avec ses attributs
		id_ : n° de la tile dans le tileset
		hflip : True s'il faut la flipper horizontalement
		vflip : idem verticalement

	PTiledMap : structure représentant une TiledMap
		tileset : liste de surfaces
		map : tableau de Tile représentant l'image

	from_surface(surface, size, find_flips = False) : renvoie une TiledMap

Exemple : à partir d'un png, générer une tiledmap sans répétition de 16x16, puis à partir du tileset, générer un deuxième tileset de patterns 8x8, sans répétition, en tenant compte des rotations

image = pygame.image.load('test/test.png')

tiled = PTiledMap.from_surface(image, (16, 16), ignore_flips)
export_tileset(tiled.tileset, 'test/tileset.png')

save_as_tmx(tiled, 'test/test_tmx.tmx')

tileset = []
patterns = []
for tile in tiled.tileset:
	t = PTiledMap.from_surface(tile, (8, 8), check_flips, tileset = patterns)
	tileset += [t.map]

export_tileset(patterns, 'test/patterns.png')

tmx.py : gestion de fichiers tmx
save_as_tmx(tiled_map, path) : sauvegarde une TiledMap ainsi que le tileset associé dans un fichier path.tmx et path.png (l'extension de path est ignorée)

