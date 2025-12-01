import math
import json

class point_3D():
    _next_point_id = 1  #Local variable to point_3D class, allows each new point_3D object to have a unique id
    
    def __init__(self, x_pos, y_pos, z_pos, point_id: int = None):  #Init, gices point 3D coord system, gives an ID if not already assigned, gives list of triangle ids that is part of
        self.coord = [x_pos, y_pos, z_pos]
        if point_id is None:
            self.point_id = point_3D._next_point_id
            point_3D._next_point_id += 1
        else:
            self.point_id = point_id
            if point_id >= point_3D._next_point_id:
                point_3D._next_point_id = point_id + 1
        self.triangle_id = []

    def move_point(self, dx, dy, dz): #Moves point by specified distances
        self.coord[0] += dx
        self.coord[1] += dy
        self.coord[2] += dz

    def move_point_to(self, x_pos, y_pos, z_pos): #Moves point to exact location
        self.coord = [x_pos, y_pos, z_pos]

    def delete_point(self): #Deletes point
        self.coord = None

    def scale(self, sx, sy, sz, origin=None): #Scales each coord by different amount
        if origin is None:
            origin = [0, 0, 0]
        if self.coord is not None:
            self.coord[0] = origin[0] + (self.coord[0] - origin[0]) * sx
            self.coord[1] = origin[1] + (self.coord[1] - origin[1]) * sy
            self.coord[2] = origin[2] + (self.coord[2] - origin[2]) * sz

    def scale_uniform(self, factor, origin=None): #Scales each coord by same amount
        self.scale(factor, factor, factor, origin)

    def rotate_x(self, angle_degrees, origin=None): # rotates x_pos about an origin by specified degree
        if self.coord is None:
            return
        if origin is None:
            origin = [0, 0, 0]
        
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        y = self.coord[1] - origin[1]
        z = self.coord[2] - origin[2]
        
        new_y = y * cos_a - z * sin_a
        new_z = y * sin_a + z * cos_a
        
        self.coord[1] = new_y + origin[1]
        self.coord[2] = new_z + origin[2]
    
    def rotate_y(self, angle_degrees, origin=None): # rotates y_pos about an origin by specified degree
        if self.coord is None:
            return
        if origin is None:
            origin = [0, 0, 0]
        
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        x = self.coord[0] - origin[0]
        z = self.coord[2] - origin[2]
        
        new_x = x * cos_a + z * sin_a
        new_z = -x * sin_a + z * cos_a
        
        self.coord[0] = new_x + origin[0]
        self.coord[2] = new_z + origin[2]
    
    def rotate_z(self, angle_degrees, origin=None): # rotates z_pos about an origin by specified degree
        if self.coord is None:
            return
        if origin is None:
            origin = [0, 0, 0]
        
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        x = self.coord[0] - origin[0]
        y = self.coord[1] - origin[1]
        
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        
        self.coord[0] = new_x + origin[0]
        self.coord[1] = new_y + origin[1]

    def equals(self, other, tolerance=1e-9):  #Checks if two point objects area in the same location
        if self.coord is None or other.coord is None:
            return False
        return (abs(self.coord[0] - other.coord[0]) < tolerance and
                abs(self.coord[1] - other.coord[1]) < tolerance and
                abs(self.coord[2] - other.coord[2]) < tolerance)

    def return_point(self):  #Prints the points attributes
        if self.coord == None:
            print("Point Deleted")
        else:
            print("x=" + str(self.coord[0]) + " y=" + str(self.coord[1]) + " z=" + str(self.coord[2]) + " Point ID=" + str(self.point_id))

    @classmethod    #Class method, not object method, resets id counter
    def reset_id_counter(cls, start=1):
        cls._next_point_id = start


class triangle(): 
    _next_triangle_id = 1  #Local variable to triangle class, allows each new triangle object to have a unique id
    
    def __init__(self, p1: point_3D, p2: point_3D, p3: point_3D, triangle_id: int = None): #Init, defines triangle by 3 point objects, gives id if not ddefined, gives each point that is in
        self.vertices = [p1, p2, p3]                                                       # it its triangle ID, creates rectagnle ID list, every rectange's id the triangle is part of will be added
        if triangle_id is None:
            self.triangle_id = triangle._next_triangle_id
            triangle._next_triangle_id += 1
        else:
            self.triangle_id = triangle_id
            if triangle_id >= triangle._next_triangle_id:
                triangle._next_triangle_id = triangle_id + 1
        
        for vertex in self.vertices:
            if self.triangle_id not in vertex.triangle_id:
                vertex.triangle_id.append(self.triangle_id)
        
        self.rectangle_id = []

    def equals(self, other, tolerance=1e-9):  #Checks if triangle object is repeated
        self_coords = set()
        other_coords = set()
        
        for v in self.vertices:
            if v.coord is not None:
                self_coords.add((round(v.coord[0]/tolerance), 
                                round(v.coord[1]/tolerance), 
                                round(v.coord[2]/tolerance)))
        
        for v in other.vertices:
            if v.coord is not None:
                other_coords.add((round(v.coord[0]/tolerance), 
                                 round(v.coord[1]/tolerance), 
                                 round(v.coord[2]/tolerance)))
        
        return self_coords == other_coords

    def return_triangle(self):     #Returns, attributes of the triangle, along with attributes of every point that makes it up
        print("Triangle ID = " + str(self.triangle_id))  
        for i in range(0, 3):
            print("----------------")
            print("Point " + str(i+1) + ":\n")
            self.vertices[i].return_point()
            print("----------------")




    @classmethod  #Rests id counter
    def reset_id_counter(cls, start=1):
        cls._next_triangle_id = start


class rectangle():
    _next_rectangle_id = 1 #Local variable to rectangle class, allows each new rectangle object to have a unique id

    def __init__(self, t1, t2, rectangle_id: int = None): # Init, makes rectangle out of two triangles
        self.halves = [t1, t2]
        if rectangle_id is None:
            self.rectangle_id = rectangle._next_rectangle_id
            rectangle._next_rectangle_id += 1
        else:
            self.rectangle_id = rectangle_id
            if rectangle_id >= rectangle._next_rectangle_id:
                rectangle._next_rectangle_id = rectangle_id + 1
        
        for half in self.halves:
            if self.rectangle_id not in half.rectangle_id:
                half.rectangle_id.append(self.rectangle_id)
        
        self.cuboid_id = []

    def return_rectangle(self):  #Prints, attributes of rectangle, and objects that make it up
        print("Rectangle ID = " + str(self.rectangle_id))
        for i in range(0, 2):
            print("================")
            print("Triangle " + str(i+1) + ":\n")
            self.halves[i].return_triangle()
            print("================")

    @classmethod #Resets id
    def reset_id_counter(cls, start=1):
        cls._next_rectangle_id = start


class cuboid(): 
    _next_cuboid_id = 1 #Local variable to cuboid class, allows each new cuboid object to have a unique id

    def __init__(self, r1, r2, r3, r4, r5, r6, cuboid_id: int = None): #Init, defines cuboid of being made up of 6 rectangles, gives IDs
        self.faces = [r1, r2, r3, r4, r5, r6]
        if cuboid_id is None:
            self.cuboid_id = cuboid._next_cuboid_id
            cuboid._next_cuboid_id += 1
        else:
            self.cuboid_id = cuboid_id
            if cuboid_id >= cuboid._next_cuboid_id:
                cuboid._next_cuboid_id = cuboid_id + 1
        
        for face in self.faces:
            if self.cuboid_id not in face.cuboid_id:
                face.cuboid_id.append(self.cuboid_id)
 
    def get_all_points(self):   #Returns a list of all coordinates of points that make up the cuboid
        points = []
        point_coords = set()
        
        for rect in self.faces:
            for tri in rect.halves:
                for pt in tri.vertices:
                    coord_tuple = (pt.coord[0], pt.coord[1], pt.coord[2])
                    if coord_tuple not in point_coords:
                        points.append(pt)
                        point_coords.add(coord_tuple)
        
        return points
    
    def rotate_x(self, angle_degrees, origin=None): #Rotates every x point in cuboid
        points = self.get_all_points()
        for pt in points:
            pt.rotate_x(angle_degrees, origin)
    
    def rotate_y(self, angle_degrees, origin=None): #Rotates every y point in cuboid
        points = self.get_all_points()
        for pt in points:
            pt.rotate_y(angle_degrees, origin)
    
    def rotate_z(self, angle_degrees, origin=None): #Rotates every z point in cuboid
        points = self.get_all_points()
        for pt in points:
            pt.rotate_z(angle_degrees, origin)
    
    def rotate(self, x_angle=0, y_angle=0, z_angle=0, origin=None): #Rotates every x,y,z point in cuboid
        if x_angle != 0:
            self.rotate_x(x_angle, origin)
        if y_angle != 0:
            self.rotate_y(y_angle, origin)
        if z_angle != 0:
            self.rotate_z(z_angle, origin)

    def return_cuboid(self):   #Returns attributes of cuboid, and all attributes of objects that define it
        print("Cuboid ID = " + str(self.cuboid_id))
        for i in range(0, 6):
            print("~~~~~~~~~~~~~~~~~~")
            print("Rectangle " + str(i+1) + ":\n")
            self.faces[i].return_rectangle()
            print("~~~~~~~~~~~~~~~~~~")

    @classmethod  #Resets id
    def reset_id_counter(cls, start=1):
        cls._next_cuboid_id = start


class assembly():
    def __init__(self, name="Assembly"):  #Defined as list of cuboids
        self.name = name
        self.cuboids = []
        self.triangles = []
    
    def add_cuboid(self, cub):  #Adds a cuboid to list
        self.cuboids.append(cub)

    def add_triangle(self, tri):
        """Add a single triangle to the assembly."""
        self.triangles.append(tri)
    
    def add_face(self, points_list):
        """
        Creates and adds triangles from a list of 3 or 4 points (a face).
        Assumes points are in counter-clockwise order.
        """
        if len(points_list) == 3:
            # It's already a triangle
            self.add_triangle(triangle(*points_list))
        elif len(points_list) == 4:
            # It's a quad, split it into two triangles (p1,p2,p3) and (p1,p3,p4)
            p1, p2, p3, p4 = points_list
            t1 = triangle(p1, p2, p3)
            t2 = triangle(p1, p3, p4)
            self.add_triangle(t1)
            self.add_triangle(t2)
        else:
            print(f"Warning: add_face only supports 3 or 4 points. Got {len(points_list)}.")
    
    def get_all_triangles(self): #Adds all triangle objects in the assembly to a list
        all_triangles = list(self.triangles)
    
        for cub in self.cuboids:
            for rect in cub.faces:
                for tri in rect.halves:
                    all_triangles.append(tri)
    
        return all_triangles
def create_cuboid_from_dimensions(x_len, y_len, z_len, origin=(0, 0, 0)): #Given 3 lengths and a point, creates all points and faces of the cuboid.
    x0, y0, z0 = origin
    points = [
        point_3D(x0,        y0,        z0),
        point_3D(x0+x_len,  y0,        z0),
        point_3D(x0+x_len,  y0+y_len,  z0),
        point_3D(x0,        y0+y_len,  z0),
        point_3D(x0,        y0,        z0+z_len),
        point_3D(x0+x_len,  y0,        z0+z_len),
        point_3D(x0+x_len,  y0+y_len,  z0+z_len),
        point_3D(x0,        y0+y_len,  z0+z_len),
    ]

    faces = [
        (0, 1, 2, 3),  # bottom
        (4, 5, 6, 7),  # top
        (0, 1, 5, 4),  # front
        (2, 3, 7, 6),  # back
        (0, 3, 7, 4),  # left
        (1, 2, 6, 5)   # right
    ]

    rectangles = [] #Creates the rectangles, triangles and point objects that make up the cuboid.
    for f in faces:
        p1, p2, p3, p4 = [points[i] for i in f]
        t1 = triangle(p1, p2, p3)
        t2 = triangle(p1, p3, p4)
        r = rectangle(t1, t2)
        rectangles.append(r)

    cub = cuboid(*rectangles)
    return cub



def export_assembly_inp(assembly_obj, filename="shape.inp"):
    # This will now remove internal faces by default
    triangles = assembly_obj.get_all_triangles()
    num_triangles = len(triangles)


    with open(filename, "w") as f:  #Writes meta data at top of .inp file
        metadata = {
            "title": "Triangle file",
            "type": "poly",
            "x_label": "Position",
            "y_label": "Position",
            "data_label": "Position",
            "x_units": "m",
            "y_units": "m",
            "rgb": "0000ff",
            "data_units": "m",
            "x_len": 1,
            "y_len": num_triangles,
            "z_len": 1,
            "cols": "zxyzxyzxyzxy"
        }
        
        f.write("#oghma_csv " + json.dumps(metadata, separators=(',', ':')) + "*\n")
        
        for tri in triangles: #Writes the .inp file from the cordinates of the points of each triangle
            for pt in tri.vertices:
                z, x, y = pt.coord[2], pt.coord[0], pt.coord[1]
                f.write(f"{z:.6e} {x:.6e} {y:.6e}\n")
            
            z, x, y = tri.vertices[0].coord[2], tri.vertices[0].coord[0], tri.vertices[0].coord[1]
            f.write(f"{z:.6e} {x:.6e} {y:.6e}\n")
            f.write("\n")




if __name__ == "__main__":
    mirror_x = 118
    mirror_y = 84
    mirror_z = 4
    # Reset ID counters
    point_3D.reset_id_counter(1)
    triangle.reset_id_counter(1)
    rectangle.reset_id_counter(1)
    cuboid.reset_id_counter(1)

    # Create an assembly
    my_assembly = assembly("MyShape")

    cuboid9 = create_cuboid_from_dimensions(42.98, mirror_y, mirror_z)
    #cuboid9.rotate_y(-45, [6.5, 6.5, 49.09])
    my_assembly.add_cuboid(cuboid9)

    cuboid10 = create_cuboid_from_dimensions(46.83, 20.27, mirror_z, origin=(42.98, 0, 0))
    for point in cuboid10.get_all_points():
        point.return_point()
        if point.point_id == 12 or point.point_id == 16:
            point.move_point(0, 10.35, 0)
            point.return_point()


    
    #cuboid10.rotate_y(-45, [6.5, 6.5, 49.09])
    my_assembly.add_cuboid(cuboid10)

    cuboid11 = create_cuboid_from_dimensions(46.83, 20.27, mirror_z, origin=(42.98, 63.73, 0))
    for point in cuboid11.get_all_points():
        point.return_point()
        if point.point_id == 17 or point.point_id == 21:
            point.move_point(0, -10.35, 0)
            point.return_point()
    #cuboid11.rotate_y(-45, [6.5, 6.5, 49.09])
    my_assembly.add_cuboid(cuboid11)

    cuboid12 = create_cuboid_from_dimensions(28.19, mirror_y, mirror_z, origin=(89.81,0,0))
    #cuboid12.rotate_y(-45, [6.5, 6.5, 49.09])
    my_assembly.add_cuboid(cuboid12)

    cuboid13 = create_cuboid_from_dimensions(mirror_x, (mirror_y-43.46)/2, mirror_z, origin=(0,0,0))
    #cuboid13.rotate_y(-45, [6.5, 6.5, 49.09])
    my_assembly.add_cuboid(cuboid13)

    cuboid14 = create_cuboid_from_dimensions(mirror_x, (mirror_y-43.46)/2, mirror_z, origin=(0,2*mirror_y/3,0))
    #cuboid14.rotate_y(-45, [6.5, 6.5, 49.09])
    my_assembly.add_cuboid(cuboid14)

    cuboid15 = create_cuboid_from_dimensions(91.816, 20.72, mirror_z, origin=(0,0,0))
    #cuboid15.rotate_y(-45, [6.5, 6.5, 49.09])
    cuboid15.rotate_z(-12, [91.816, 0, 49.09])
    my_assembly.add_cuboid(cuboid15)

    cuboid16 = create_cuboid_from_dimensions(91.816, 20.72, mirror_z, origin=(0,2*mirror_y/3,0))
    #cuboid16.rotate_y(-45, [6.5, 6.5, 49.09])
    cuboid16.rotate_z(12, [91.816, 2*mirror_y/3, 49.09])
    my_assembly.add_cuboid(cuboid16)

    export_assembly_inp(my_assembly, "simple_hole.inp")

    


    """

    #Generate the 8 needed cuboids for simple design
    
    cuboid1 = create_cuboid_from_dimensions(83, 6.5, 49.09, origin=(0, 0, 0))
    my_assembly.add_cuboid(cuboid1)

    cuboid2 = create_cuboid_from_dimensions(6.5, 83, 49.09, origin=(0, 6.5, 0))
    my_assembly.add_cuboid(cuboid2)

    
    cuboid3 = create_cuboid_from_dimensions(83, 6.5, 49.09, origin=(0, 89.5, 0))
    my_assembly.add_cuboid(cuboid3)


    cuboid4 = create_cuboid_from_dimensions(6.5, 83, 49.09, origin=(76.5, 6.5, 0))
    my_assembly.add_cuboid(cuboid4)

    #cuboid5 = create_cuboid_from_dimensions(118, 84, 6.5)
    #cuboid5.rotate_y(-45, [6.5, 6.5, 49.09])
    #my_assembly.add_cuboid(cuboid5)

    
    cuboid6 = create_cuboid_from_dimensions(6.5, 6.5, 102, origin=(76.5, 0, 49.09))
    my_assembly.add_cuboid(cuboid6)

    cuboid7 = create_cuboid_from_dimensions(6.5, 6.5, 102, origin=(76.5, 89.5, 49.09))
    my_assembly.add_cuboid(cuboid7)

    cuboid8 = create_cuboid_from_dimensions(6.5, 83, 6.5, origin=(76.5, 6.5, 144.59))
    my_assembly.add_cuboid(cuboid8)
"""
    
