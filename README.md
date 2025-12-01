OghmaNano Mesh Generator
A Python Object-Oriented library for generating complex 3D geometries for drift-diffusion simulations.

1. What is this?
OghmaNano (formerly gpvdm) is a powerful tool for simulating solar cells and LEDs. However, creating complex 3D meshes for its internal finite-element solver can be tedious by hand.

This library allows researchers to define geometries using Python objects and programmatically export them to OghmaNano-compatible formats (shape.inp).

2. Why I built it
While working on my Level 4 reseach project at university, I needed to simulate a device in OghmaNano, however I could not import the CAD file, as that resulted in a mesh with too many trianlges, and therefore too much complexity. Manually defining thousands of vertices in the GUI was inefficient. I built this tool to:

Automate the mesh generation process.

Parameterize the geometry (e.g., "Change radius from 5nm to 10nm" with one variable).

Ensure validity by programmatically checking that meshes are "watertight" (required for optical simulations).

3. How it works (OOP Approach)
The project uses a hierarchical class structure:

Classes include a 3D point, a triangle, made up of 3 3D points, a rectangle, made up of 2 triangles, a cuboid, made up of 6 rectangles and an assembly class, which is a combination of all other shape objects.
Using these, any 3D shapes can be made, where every point is listed, and to export it as a mesh, every triangle in an assembly is defined.

There are also extra functions, such as create_cuboid_from_dimensions, that automates creating all the objects(points, triangles, rectangles) in a cuboid, given a starting origin and x,y,z lengths.
This allows for common shapes to be made quickly, whereas new shapes will have to be defined from scratch, or from multiple of these automated shapes pushed together.

There is finally a function that takes all the triangles inside an assembly and writes their coordinates in the correct format to a .inp file, which can then be imported to OghmaNano