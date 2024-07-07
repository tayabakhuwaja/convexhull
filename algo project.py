import tkinter as tk

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class LineIntersectionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Line Intersection Checker - Tkinter Example")

        self.points = []
        self.lines = []
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("Cross Product")
        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="light blue")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.label_var = tk.StringVar()
        self.label = tk.Label(self.master, textvariable=self.label_var, font=("Helvetica", 14))
        self.label.pack()

        # Dropdown menu for selecting the algorithm
        algorithm_menu = tk.OptionMenu(self.master, self.algorithm_var, "Cross Product", "Slope", "Parametric")
        algorithm_menu.pack()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        point = Point2D(x, y)
        self.points.append(point)
        self.draw_point(point)

        if len(self.points) == 2:
            self.label_var.set("Checking intersection...")
            self.master.update_idletasks()  # Update the label text

            algorithm = self.algorithm_var.get()

            if algorithm == "Cross Product":
                intersection = self.check_intersections_cross(self.points[0], self.points[1])
            elif algorithm == "Slope":
                intersection = self.check_intersections_slope(self.points[0], self.points[1])
            elif algorithm == "Parametric":
                intersection = self.check_intersections_parametric(self.points[0], self.points[1])
            else:
                intersection = False

            if intersection:
                self.label_var.set("Lines intersect!")
            else:
                self.label_var.set("Lines do not intersect.")

            self.draw_line(self.points[0], self.points[1])
            self.points = []  # Clear the points list after drawing a line

    def draw_point(self, point):
        x, y = point.x, point.y
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")

    def draw_line(self, point1, point2):
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        line_id = self.canvas.create_line(x1, y1, x2, y2, fill="blue")
        self.lines.append((point1, point2, line_id))

    def check_intersections_cross(self, new_point1, new_point2):
        for line in self.lines[:-1]:
            intersect = self.do_lines_intersect_cross(new_point1, new_point2, line[0], line[1])
            if intersect:
                return True
        return False

    def check_intersections_slope(self, new_point1, new_point2):
        for i in range(len(self.lines) - 1):
            for j in range(i + 1, len(self.lines)):
                line1 = self.lines[i]
                line2 = self.lines[j]
                intersect = self.do_lines_intersect_slope(new_point1, new_point2, line1[0], line1[1])
                if intersect:
                    return True
                intersect = self.do_lines_intersect_slope(new_point1, new_point2, line2[0], line2[1])
                if intersect:
                    return True
        return False

    def check_intersections_parametric(self, new_point1, new_point2):
        for i in range(len(self.lines) - 1):
            for j in range(i + 1, len(self.lines)):
                line1 = self.lines[i]
                line2 = self.lines[j]
                intersect = self.do_lines_intersect_parametric(new_point1, new_point2, line1[0], line1[1])
                if intersect:
                    return True
                intersect = self.do_lines_intersect_parametric(new_point1, new_point2, line2[0], line2[1])
                if intersect:
                    return True
        return False

    def do_lines_intersect_cross(self, p1, q1, p2, q2):
        def orientation(p, q, r):
            val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
            if val == 0:
                return 0
            return 1 if val > 0 else 2

        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and self.on_segment(p1, p2, q1):
            return True
        if o2 == 0 and self.on_segment(p1, q2, q1):
            return True
        if o3 == 0 and self.on_segment(p2, p1, q2):
            return True
        if o4 == 0 and self.on_segment(p2, q1, q2):
            return True

        return False

    def do_lines_intersect_slope(self, p1, q1, p2, q2):
        def cross_product(v1, v2):
            return v1.x * v2.y - v1.y * v2.x

        def subtract_points(v1, v2):
            return Point2D(v1.x - v2.x, v1.y - v2.y)

        def orientation(p, q, r):
            val = cross_product(subtract_points(q, p), subtract_points(r, q))
            if val == 0:
                return 0
            return 1 if val > 0 else 2

        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and self.on_segment(p1, p2, q1):
            return True
        if o2 == 0 and self.on_segment(p1, q2, q1):
            return True
        if o3 == 0 and self.on_segment(p2, p1, q2):
            return True
        if o4 == 0 and self.on_segment(p2, q1, q2):
            return True

        return False



 def parametric_intersect(p1, q1, p2, q2):
    def orientation(p, q, r):
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
        if val == 0:
            return 0
        return 1 if val > 0 else 2

    def on_segment(p, q, r):
        return min(p.x, q.x) <= r.x <= max(p.x, q.x) and min(p.y, q.y) <= r.y <= max(p.y, q.y)

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    # Check for intersection using parametric method
    denominator = (q1.y - p1.y) * (q2.x - p2.x) - (q1.x - p1.x) * (q2.y - p2.y)
    if denominator == 0:
        return False
        
    # Calculate parameters for intersection points
    t = ((p2.x - p1.x) * (q2.y - p2.y) - (p2.y - p1.y) * (q2.x - p2.x)) / denominator
    u = ((p1.x - q1.x) * (q2.y - p2.y) - (p1.y - q1.y) * (q2.x - p2.x)) / denominator
    
    # Check if intersection points lie within the line segments
    if 0 <= t <= 1 and 0 <= u <= 1:
        return True
    
    return False

def main():
    root = tk.Tk()
    app = LineIntersectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
