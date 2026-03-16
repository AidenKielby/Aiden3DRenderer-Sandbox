
embed_w = embed.winfo_width()
embed_h = embed.winfo_height()
renderer = Renderer3D(width=embed_w, height=embed_h, title="My 3D Renderer")
renderer.render_type = renderer_type.MESH

obj = obj_loader.get_obj("dragon.obj", 0, scale=1)
renderer.vertices_faces_list.append(obj)
renderer.set_texture_for_raster("dragon_21.1.png")
