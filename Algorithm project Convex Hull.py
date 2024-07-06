import tkinter as tk
import math

CW = -1
CCW = 1
COLLINEAR = 0

points = []

def orientation(p1, p2, p3):
    x1, y1, x2, y2, x3, y3 = *p1, *p2, *p3
    d = (y3-y1)*(x2-x1) - (y2-y1)*(x3-x1)
    canvas.create_line(*p2,*p3,fill='yellow',tags='del')
    canvas.update()
    canvas.delete('del')
    canvas.update()
    if d > 0:
        return 1
    elif d < 0:
        return -1
    else:
        return 0
      

def dist(p1, p2):
    x1, y1, x2, y2 = *p1, *p2
    return math.sqrt((y2-y1)**2 + (x2-x1)**2)
  
# graham scan
def polar_angle(p1, p2):
    if p1[1] == p2[1]:
        return -math.pi
    dy = p1[1]-p2[1]
    dx = p1[0]-p2[0]
    return math.atan2(dy, dx)

def graham_scan():
    root.title("Graham Scan")
    canvas.unbind("<Button-1>")
    canvas.delete("hull")
    p0 = max(points, key=lambda point: point[1])
    points.sort(key=lambda p: (polar_angle(p0, p), dist(p0, p)))
    hull = []
    lines = []
    for i in range(len(points)):
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], points[i]) == CW:
            hull.pop()
            line = lines.pop()
            canvas.delete(line)
        if(len(hull)>=1):
            lines.append(canvas.create_line(*hull[-1],points[i],fill='green',tags="hull"))
            canvas.update()
        hull.append(points[i])
    for line in lines:
        canvas.itemconfig(line, fill="red")
    canvas.create_line(*hull[0],*hull[-1],fill="red",tags="hull")
    canvas.update()

    canvas.bind("<Button-1>", draw_point)
    return hull

# brute force
def on_convex_hull(p, q):
    # Check if p-q is on the convex hull of points
    for r in points:
        if r != p and r != q and orientation(p, q, r) < 0:
            return False
    return True

def brute_force():
    root.title("Brute Force")
    canvas.unbind("<Button-1>")
    canvas.delete('hull')
    hull = []
    n = len(points)

    for i in range(n):
        for j in range(n):
            if j==i:
                continue
            canvas.create_line(*points[i],*points[j],fill='green',tags='temporary')
            canvas.update()
            if on_convex_hull(points[i], points[j]):
                hull.append(points[i])
                hull.append(points[j])
                canvas.create_line(*points[i],*points[j],fill='red',tags='hull')
                canvas.update()
            canvas.delete('temporary')
            canvas.update()

    canvas.bind("<Button-1>", draw_point)
    return hull

#gift wrapping
def gift_wrapping():
    root.title("Package Wrap")
    canvas.unbind("<Button-1>")
    canvas.delete('hull')
    on_hull = max(points, key=lambda point: point[1])
    hull = []
    while True:
        hull.append(on_hull)
        next_point = points[0]
        #drawing temporary hull line
        canvas.create_line(*next_point,*hull[-1],fill='green',tags='temp')
        canvas.update()

        for point in points:
            o = orientation(on_hull, next_point, point)
            if next_point == on_hull or o == 1 or (o == 0 and dist(on_hull, point) > dist(on_hull, next_point)):
                next_point = point
                canvas.delete('temp')
                canvas.update()
                canvas.create_line(*next_point,*hull[-1],fill='green',tags='temp')
                canvas.update()
        on_hull = next_point
        canvas.delete('temp')
        canvas.create_line(*on_hull,*hull[-1],fill = 'red',tags='hull')
        canvas.update()
        if on_hull == hull[0]:
            break
    canvas.bind("<Button-1>", draw_point)
    return hull

# quick elimination
def in_rectangle(p1, p2, p3, p4, point):
    return (
        orientation(p1, p2, point) > 0 and
        orientation(p2, p3, point) > 0 and
        orientation(p3, p4, point) > 0 and
        orientation(p4, p1, point) > 0
    )

def quick_elimination():
    root.title("Quick Elimination")
    canvas.unbind("<Button-1>")
    canvas.delete('hull')
    if len(points) < 4:
        return points

    # Phase 1: Compute Rectangle (R)
    xmax = max(points, key = lambda p: (p[0],p[1]))
    xmin = min(points, key = lambda p: (p[0],p[1]))
    ymax = max(points, key = lambda p: (p[1],p[0]))
    ymin = min(points, key = lambda p: (p[1],p[0]))
    rectangle = [xmin,ymin,xmax,ymax]
    for i in range(3):
        canvas.create_line(*rectangle[i],*rectangle[i+1],fill='blue',tags='rectangle')
    canvas.create_line(*rectangle[0],*rectangle[-1],fill='blue',tags='rectangle')
    canvas.update()

    # Phase 2: Eliminate Points Inside R
    remaining_points = []
    remaining_points = [point for point in points if not in_rectangle(rectangle[0],rectangle[1],rectangle[2],rectangle[3], point)]

    # Phase 3: Find Convex Hull of Remaining Points
    on_hull = max(remaining_points, key=lambda point: point[1])
    hull = []
    while True:
        hull.append(on_hull)
        next_point = remaining_points[0]
        #drawing temporary hull line
        canvas.create_line(*next_point,*hull[-1],fill='green',tags='temp')
        canvas.update()

        for point in remaining_points:
            o = orientation(on_hull, next_point, point)
            if next_point == on_hull or o == 1 or (o == 0 and dist(on_hull, point) > dist(on_hull, next_point)):
                next_point = point
                canvas.delete('temp')
                canvas.update()
                canvas.create_line(*next_point,*hull[-1],fill='green',tags='temp')
                canvas.update()
        on_hull = next_point
        canvas.delete('temp')
        canvas.create_line(*on_hull,*hull[-1],fill = 'red',tags='hull')
        canvas.update()
        if on_hull == hull[0]:
            break
    canvas.delete('rectangle')

    canvas.bind("<Button-1>", draw_point)
    return hull

#Monotone Chain algorithm
def monotone_chain():
    root.title("Monotone Chain")
    canvas.unbind("<Button-1>")
    canvas.delete("hull")
    # There must be at least 3 points
    if (len(points) < 3):
        return points
 
    # Initialize Result
    hull = []
 
    # Find the leftmost point
    left = 0
    for i in range(1, len(points)):
        if (points[i][0] < points[left][0]):
            left = i
 
    p = left
    q = 0
    while (True):
        hull.append(points[p])
 
        q = (p + 1) % len(points)
 
        for i in range(0, len(points)):
            if (orientation(points[p], points[i], points[q]) == CCW):
                q = i
        canvas.create_line(*points[p],*points[q],fill = 'red',tags='hull')
        p = q
        
        # While we don't come to first point
        if (p == left):
            break
    canvas.bind("<Button-1>", draw_point)
    return hull

#draw point function
def draw_point(event):
    """Function to draw a point on the canvas at the mouse click location."""
    x, y = event.x, event.y
    canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black", outline="black", tags="points")
    points.append((x, y))

# Create the main Tkinter window
root = tk.Tk()
root.title("Convex Hull Visualization")

# Create a canvas to draw points and convex hull
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack(pady=10)
canvas.bind("<Button-1>", draw_point)

# Create a button to start the Jarvis March algorithm step by step
button1 = tk.Button(root, text="Run Package Wrap", command=gift_wrapping)
button1.pack(side=tk.LEFT)

button2 = tk.Button(root,text='Run Graham Scan',command=graham_scan)
button2.pack(side = tk.LEFT)

button3 = tk.Button(root,text='Run Brute Force',command=brute_force)
button3.pack(side=tk.LEFT)

button4 = tk.Button(root,text='Run Quick Elimination',command=quick_elimination)
button4.pack(side=tk.LEFT)

button5 = tk.Button(root, text="Run Monotone Chain", command=monotone_chain)
button5.pack(side=tk.LEFT)

# Run the Tkinter event loop
root.mainloop()