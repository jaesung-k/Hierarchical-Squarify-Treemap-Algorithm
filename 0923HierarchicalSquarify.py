"""
    Args:
        R: Boundary rectangle for treemap diagram
        V: List of number values
        S: Am side
    Returns:
        R: Treemap as list of rectangles
"""

from Rhino.Geometry import *
import rhinoscriptsyntax as rs
import scriptcontext as sc

# START Squarify code by tomeido
def normalize_sizes(sizes, dx, dy):
    total_size = sum(sizes)
    total_area = dx * dy
    sizes = map(float, sizes)
    sizes = map(lambda size: size * total_area / total_size, sizes)
    return list(sizes)

#def shorter(dx,dy):
#    if dx>=dy:
#        return dy
#    if dx<dy:
#        return dx

def rectanglerow_0(sizes, x, y, dx, dy, iter):
    covered_area = sum(sizes)
    width = covered_area / dy
    rects = []
    for size in sizes:
        rects.append({'x': x, 'y': y, 'dx': width, 'dy': size / width})
        y += size / width
    print("rectanglerow_1")
    return rects

def rectanglerow_1(sizes, x, y, dx, dy, iter):
    covered_area = sum(sizes)
    width = covered_area / dy
    rects = []
    for size in sizes:
        rects.append({'x': x+dx-width, 'y': y, 'dx': width, 'dy': size / width})
        y += size / width
    print("rectanglerow_2")
#    print(rects)
    return rects

def rectanglecol_0(sizes, x, y, dx, dy, iter):
    covered_area = sum(sizes)
    height = covered_area / dx
    rects = []
    for size in sizes:
        rects.append({'x': x, 'y': y, 'dx': size / height, 'dy': height})
        x += size / height
    print("rectanglecol_1")
    return rects

def rectanglecol_1(sizes, x, y, dx, dy, iter):
    covered_area = sum(sizes)
    height = covered_area / dx
    rects = []
    for size in sizes:
        rects.append({'x': x, 'y': y+dy-height, 'dx': size / height, 'dy': height})
        x += size / height
    print("rectanglecol_2")
#    print(rects)
    return rects

def rectangle(sizes, x, y, dx, dy, iter):
    if dx>=dy and S[iter] == 0:
        return rectanglerow_0(sizes, x, y, dx, dy, iter)
    elif dx<dy and S[iter] == 0:
        return rectanglecol_0(sizes, x, y, dx, dy, iter)
    elif dx>=dy and S[iter] == 1:
        return rectanglerow_1(sizes, x, y, dx, dy, iter)
    else:
        return rectanglecol_1(sizes, x, y, dx, dy, iter)

def leftrectanglerow_0(sizes, x, y, dx, dy, iter):
    covered_area = sum(sizes)
    width = covered_area / dy
    leftover_x = x + width
    leftover_y = y
    leftover_dx = dx - width
    leftover_dy = dy
    print("leftrectanglerow_1")
    return (leftover_x, leftover_y, leftover_dx, leftover_dy, iter)

def leftrectanglerow_1(sizes, x, y, dx, dy, iter):
    covered_area = sum(sizes)
    width = covered_area / dy
    leftover_x = x
    leftover_y = y
    leftover_dx = dx - width
    leftover_dy = dy
    print("leftrectanglerow_2")
#    print(leftover_x, leftover_y, leftover_dx, leftover_dy)
    return (leftover_x, leftover_y, leftover_dx, leftover_dy, iter)

def leftrectanglecol_0(sizes, x, y, dx, dy, iter):
    covered_area = sum(sizes)
    height = covered_area / dx
    leftover_x = x
    leftover_y = y + height
    leftover_dx = dx
    leftover_dy = dy - height
    print("leftrectanglecol_1")
    return (leftover_x, leftover_y, leftover_dx, leftover_dy, iter)

def leftrectanglecol_1(sizes, x, y, dx, dy, iter):
    covered_area = sum(sizes)
    height = covered_area / dx
    leftover_x = x
    leftover_y = y
    leftover_dx = dx
    leftover_dy = dy - height
    print("leftrectanglecol_2")
#    print(leftover_x, leftover_y, leftover_dx, leftover_dy)
    return (leftover_x, leftover_y, leftover_dx, leftover_dy, iter)

def leftrectangle(sizes, x, y, dx, dy, iter):
    if dx>=dy and S[iter] == 0:
        return leftrectanglerow_0(sizes, x, y, dx, dy, iter)
    elif dx<dy and S[iter] == 0:
        return leftrectanglecol_0(sizes, x, y, dx, dy, iter)
    elif dx>=dy and S[iter] == 1:
        return leftrectanglerow_1(sizes, x, y, dx, dy, iter)
    else:
        return leftrectanglecol_1(sizes, x, y, dx, dy, iter)

#def worst_ratio(sizes, x, y, dx, dy):
#    return max([max(rect['dx'] / rect['dy'], rect['dy'] / rect['dx']) for rect in rectangle(sizes, x, y, dx, dy)])

def squarify(sizes, x, y, dx, dy, iter):
    iter += 1
    print(iter)
    sizes = list(map(float, sizes))

    if len(sizes) == 0:
        return []
    
    if len(sizes) == 1:
        return rectangle(sizes, x, y, dx, dy)
    
    i = 1
    while i < len(sizes) and str(sizes[i-1]) == str(sizes[i]):
        i += 1
        
    current = sizes[:i]
    remaining = sizes[i:]
    
    (leftover_x, leftover_y, leftover_dx, leftover_dy, iter) = leftrectangle(current, x, y, dx, dy, iter)
    return rectangle(current, x, y, dx, dy, iter) + squarify(remaining, leftover_x, leftover_y, leftover_dx, leftover_dy, iter)
# END Squarify code by tomeido

if not R:
    raise ValueError("Input R failed to collect data")

if type(R) == Rectangle3d:
    icount = 0
    rectangles = []
    sizes_normalized = normalize_sizes(V, R.X.Length, R.Y.Length)
    index=sizes_normalized
    squarified = squarify(sizes_normalized, R.X.Min, R.Y.Min, R.X.Length, R.Y.Length, icount)
    
    for square in squarified:
        origin = Point3d(square['x'], square['y'], 0)
        rectangle_plane = Plane(origin, Vector3d(1,0,0), Vector3d(0,1,0))
        rectangle = Rectangle3d(rectangle_plane, square['dx'], square['dy'])
        rectangles.append(rectangle)
    
    transform = Transform.ChangeBasis(R.Plane, Plane(Point3d(0,0,0), Vector3d(1,0,0), Vector3d(0,1,0)))
    [a.Transform(transform) for a in rectangles]
    
    R = rectangles
    
else:
    raise TypeError("Input R must be a rectangle")

