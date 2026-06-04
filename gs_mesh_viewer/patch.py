content = open('gs_mesh_viewer.html').read()

old = """  if (splatViewer) splatViewer.update();
  renderer.render(threeScene, camera);
  if (splatViewer) splatViewer.render();"""

new = """  if (splatViewer) {
    splatViewer.update();
    splatViewer.render();
  } else {
    renderer.render(threeScene, camera);
  }"""

content = content.replace(old, new)
open('gs_mesh_viewer.html', 'w').write(content)
print("Done")
