import pandas as pd
import polars as pl
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
import numpy as np
import math
from IPython.display import HTML

class Branch:
    def __init__(self, start, end, angle):
        self.start = start
        self.end = end
        self.angle = angle

    def length(self):
        return math.sqrt((self.end[0] - self.start[0]) ** 2 + (self.end[1] - self.start[1]) ** 2)

    def next_left(self, generation, branch_ratio, branch_angle, pertubation):
        length = self.length() * branch_ratio ** generation
        angle = self.angle + branch_angle
        angle = angle * pertubation
        end = [self.end[0] + length * np.cos(angle), self.end[1] + length * np.sin(angle)]
        return Branch(start=self.end, end=end, angle=angle)

    def next_mid(self, generation, branch_ratio, branch_angle, pertubation):
        length = self.length() * branch_ratio ** generation
        angle = self.angle
        angle = angle * pertubation
        end = [self.end[0] + length * np.cos(angle), self.end[1] + length * np.sin(angle)]
        return Branch(start=self.end, end=end, angle=angle)

    def next_right(self, generation, branch_ratio, branch_angle, pertubation):
        length = self.length() * branch_ratio ** generation
        angle = self.angle - branch_angle
        angle = angle * pertubation
        end = [self.end[0] + length * np.cos(angle), self.end[1] + length * np.sin(angle)]
        return Branch(start=self.end, end=end, angle=angle)

def pertubation(level, depth):
    if (level > 3):
        return random.uniform(1 - level / (4 * depth), 1 + level / (4 * depth))
    else:
        return random.uniform(0.7, 1.2)

def score_split(probability, data):
    if (len(data) < 6):
        return [data, {}]
    selected_items = {}
    retained_items = {}
    for key, value in data.items():
        if random.random() < probability:
            selected_items[key] = value
        else:
            retained_items[key] = value
    return [selected_items, retained_items]

BASE_WIDTH = 1
BASE_LEN = 1

class Tree:
    def __init__(self, start_angle):
        self.open_branches = {}
        self.closed_branches = {}
        self.open_but_grown = {}
        self.open_branches[''] = Branch([0, 0], [0, BASE_LEN], start_angle)

    def get_closed_lines(self, ax):
        result = []
        for k, v in self.closed_branches.items():
            result = result + ax.plot([v.start[0], v.end[0]], [v.start[1], v.end[1]], color='brown', linewidth=BASE_WIDTH)
        return result

    def get_open_lines(self, ax, percent):
        result = []
        for k, v in self.open_branches.items():
            direction = (v.end[0] - v.start[0], v.end[1] - v.start[1])
            scaled = (direction[0] * percent, direction[1] * percent)
            result = result + ax.plot([v.start[0], v.start[0] + scaled[0]], [v.start[1], v.start[1] + scaled[1]], color='green', linewidth=BASE_WIDTH)
        return result

    def get_open_but_grown_lines(self, ax):
        result = []
        for k, v in self.open_but_grown.items():
            result = result + ax.plot([v.start[0], v.end[0]], [v.start[1], v.end[1]], color='green', linewidth=BASE_WIDTH)
        return result

    def draw(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        self.get_closed_lines(ax)
        self.get_open_lines(ax, 1)
        plt.show()

    def next(self, branch_ratio, branch_angle, pertub_fn, score):
        next_open = {}
        split = score_split(score, self.open_branches | self.open_but_grown)
        for k, v in split[0].items():
            pertubation = pertub_fn(len(k) + 1)
            next_open[k + '0'] = v.next_left(len(k), branch_ratio, branch_angle, pertubation)
            pertubation = pertub_fn(len(k) + 1)
            next_open[k + '1'] = v.next_mid(len(k), branch_ratio, branch_angle, pertubation)
            pertubation = pertub_fn(len(k) + 1)
            next_open[k + '2'] = v.next_right(len(k), branch_ratio, branch_angle, pertubation)
        self.closed_branches = self.closed_branches | split[0]
        self.open_but_grown = split[1]
        self.open_branches = next_open           

class TreeUpdater:
    def __init__(self, depth, frames_per_update, branch_ratio, branch_angle, pertub_fn):
        self.depth = depth
        self.frames_per_update = frames_per_update
        self.branch_ratio = branch_ratio
        self.branch_angle = branch_angle
        self.pertub_fn = pertub_fn

class TreeAnimation:
    def __init__(self, tree, updater, scores):
        self.fig, self.ax = plt.subplots()
        self.tree = tree
        self.updater = updater
        self.scores = scores
        self.current_score = 0

    def clear_plot(self):
        self.ax.cla()

    def init_animation(self):
        self.clear_plot()
        result = self.tree.get_closed_lines(self.ax) + self.tree.get_open_lines(self.ax, 1)
        return result

    def update_animation(self, frame):
        self.clear_plot()
        remainder = frame % self.updater.frames_per_update
        result = []
        if (remainder == 0):
            self.tree.next(self.updater.branch_ratio, self.updater.branch_angle, self.updater.pertub_fn, self.scores[self.current_score])
            self.current_score = self.current_score + 1
        result = self.tree.get_closed_lines(self.ax) + self.tree.get_open_lines(self.ax, remainder / self.updater.frames_per_update)
        result = result + self.tree.get_open_but_grown_lines(self.ax)
        return result

    def animate(self):
        frames = self.updater.depth * self.updater.frames_per_update
        ani = animation.FuncAnimation(self.fig, self.update_animation, frames=frames,
                                      init_func=self.init_animation, blit=True)
        return ani
    
df_data = (
    pl.read_csv('restricted_data.csv')
    .with_columns(import_export_diff=pl.col('import_export_diff') * pl.when(pl.col('import_export_diff_flag')).then(1).otherwise(-1) + np.random.normal(0, .5, size=44640))
    .with_columns(stored_energy_time_diff=pl.col('stored_energy_time_diff') * pl.when(pl.col('import_export_diff_flag')).then(1).otherwise(-1) + np.random.normal(0, .5, size=44640))
    .select(
        'DeviceID',
        ((pl.col('import_export_diff') - pl.min('import_export_diff')) / (pl.max('import_export_diff') - pl.min('import_export_diff'))).alias('import_export_diff'),
        ((pl.col('stored_energy_time_diff') - pl.min('stored_energy_time_diff')) / (pl.max('stored_energy_time_diff') - pl.min('stored_energy_time_diff'))).alias('stored_energy_time_diff'),
        # ((pl.col('import_fulfillment') - pl.min('import_fulfillment')) / (pl.max('import_fulfillment') - pl.min('import_fulfillment'))).alias('import_fulfillment'),
        # ((pl.col('export_fulfillment') - pl.min('export_fulfillment')) / (pl.max('export_fulfillment') - pl.min('export_fulfillment'))).alias('export_fulfillment'),
    )
    .with_columns(test_column=(pl.col('import_export_diff') + pl.col('stored_energy_time_diff')) / 3)
    .with_columns(test_column_2=(pl.col('import_export_diff') + pl.col('stored_energy_time_diff'))  / 2)
)

df_data.head()

def get_widths(col):
    result = []
    for id, vals in enumerate(df_data.filter(pl.col('DeviceID') == 'OM1').drop(['DeviceID']).limit(175).iter_rows()):
        result.append(vals[col])
    return result

def get_scores():
    result = []
    a_items = get_widths(0)
    b_items = get_widths(1)
    c_items = get_widths(2)
    d_items = get_widths(3)
    for a, b, c, d in zip(a_items, b_items, c_items, d_items):
        result.append((a + b + c + d) / 4)
    return result

def smooth_array(arr, n=13):
    smoothed_arr = np.copy(arr)
    length = len(arr)
    
    for i in range(length):
        start_idx = max(0, i - n)
        end_idx = min(length, i + n + 1)
        smoothed_arr[i] = np.mean(arr[start_idx:end_idx])
    
    return smoothed_arr


def generate_root(angle, length, start_x=0, start_y=0, width=1.0, num_points=100):
    angle_rad = np.deg2rad(angle)

    t = np.linspace(0, length, num_points)
    phase_shift = np.random.uniform(0, 2 * np.pi)
    sine_wave = np.sin(t * np.pi / length * np.random.uniform(0.75, 2.0) + phase_shift)

    taper = np.linspace(width, 0, num_points)

    x_coords = start_x + taper * np.sin(angle_rad) * sine_wave
    y_coords = start_y - t * np.cos(angle_rad)

    y_coords[0] = start_y
    x_smooth = smooth_array(x_coords)

    x_smooth -= x_smooth[0]

    return x_smooth, y_coords

SCALING_FACTOR = .995

class Root:
    def __init__(self, angle, length, start, width, points, data):
        self.angle = angle
        self.length = length
        self.start = start
        self.width = width
        self.points = points
        self.generated = self.generate(data)

    def generate(self, data):
        result = generate_root(self.angle, self.length, self.start[0], self.start[1], self.width, self.points)
        lists = list(zip(result[0].tolist(), result[1].tolist()))
        x_shift = [(x + self.start[0], y) for x, y in lists]
        result = []
        i = 0
        for coord, width in zip(x_shift, data):
            result.append((coord[0], coord[1], 4 * width * (SCALING_FACTOR ** i)))
            i += 1
        return result

    def get_lines(self, ax, count):
        points = self.generated
        result = []
        last = points[0]
        for (x, y, w) in points[1:count]:
            result = result + ax.plot([last[0], x], [last[1], y], color='brown', linewidth=w)
            last = (x, y, w)
        return result

def gen_roots(n):
    angles = np.linspace(-45, 45, n, endpoint=False) + np.random.randint(-5, 5, n)
    result = []
    i = 0
    for angle in angles:
        length = BASE_LEN * 2 + np.random.randint(-2, 2)
        result.append(Root(angle, length, (0, 0), BASE_WIDTH, 175, get_widths(i)))
        i = i + i
    return result

class RootAndTreeAnimation:
    def __init__(self, tree, roots):
        self.tree = tree
        self.roots = roots

    def init_animation(self):
        result = self.tree.init_animation()
        return result

    def update_animation(self, frame):
        result = self.tree.update_animation(frame)
        frames = self.tree.updater.depth * self.tree.updater.frames_per_update * 16
        count = frame
        if (frame < frames / 512):
            count = int(frame / 512)
        if (frame < frames / 256):
            count = int(frame / 256)
        if (frame < frames / 128):
            count = int(frame / 128)
        if (frame < frames / 64):
            count = int(frame / 64)
        if (frame < frames / 32):
            count = int(frame / 32)
        if (frame < frames / 16):
            count = int(frame / 16)
        if (frame < frames / 8):
            count = int(frame / 8)
        if (frame < frames / 4):
            count = int(frame / 4)
        if (frame < frames / 2):
            count = int(frame / 2)
        for root in self.roots:
            result = result + root.get_lines(self.tree.ax, count) 
        return result

    def animate(self):
        frames = self.tree.updater.depth * self.tree.updater.frames_per_update
        ani = animation.FuncAnimation(self.tree.fig, self.update_animation, frames=frames,
                                      init_func=self.init_animation, blit=True)
        return ani
    
tree = Tree(np.pi / 2)
depth = 7
updater = TreeUpdater(depth, 50, 0.9, np.pi / 6, lambda x: pertubation(x, depth))
anim_tree = TreeAnimation(tree, updater, get_scores())
root_and_tree = RootAndTreeAnimation(anim_tree, gen_roots(4))
ani = root_and_tree.animate()
plt.show()