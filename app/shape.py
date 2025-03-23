from __future__ import annotations
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as MplCircle, Polygon as MplPolygon, Ellipse as MplEllipse

class Shape(ABC):
    @abstractmethod
    def to_dict(self) -> dict[str, any]:
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, any]) -> Shape:
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def parse_args(args: list[str]) -> dict[str, any]:
        return NotImplementedError
    
    @staticmethod
    @abstractmethod
    def get_help() -> str:
        return NotImplementedError
    
    
class Point(Shape):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def to_dict(self) -> dict[str, any]:
        return {
            'type': 'point',
            'x': self.x,
            'y': self.y
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, any]) -> Point:
        return cls(
            data['x'],
            data['y']
        )
        
    @staticmethod
    def parse_args(args: list[str]) -> dict[str, any]:
        if len(args) != 2:
            raise ValueError('Небходимо 2 параметра: x y')
        return {'x': float(args[0]), 'y': float(args[1])}
    
    @staticmethod
    def get_help() -> str:
        return "Числовое значение по оси x и по оси y"
    
    #test
    def draw(self, ax: plt.Axes):
        ax.scatter(self.x, self.y, label = f'{self.__repr__}')
        
    
    def __eq__(self, other: Point) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self) -> str:
        return f'Point (x={self.x}, y={self.y})'

class Segment(Shape):
    def __init__(self, start: Point, end: Point):
        if start == end:
            raise ValueError('Start point и end start не должны быть равны')
        self.start = start
        self.end = end

    def to_dict(self) -> dict[str, any]:
        return {
            'type': 'segment',
            'start': self.start.to_dict(),
            'end': self.end.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, any]) -> Segment:
        return cls(
            start = Point.from_dict(data['start']),
            end = Point.from_dict(data['end']),
        )
        
    @staticmethod
    def parse_args(args: list[str]) -> dict[str, any]:
        if len(args) != 4:
            raise ValueError('Укажите значение 2 точек по х, y для отрезка. Формат: x1 y1 x2 y2 ')
        return {
            'start': Point(float(args[0]), float(args[1])),
            'end': Point(float(args[2]), float(args[3]))
        }
    
    @staticmethod
    def get_help() -> str:
        return 'Значения точек start, end. x_start y_start x_end y_end'
    
    #test
    def draw(self, ax: plt.Axes):
        ax.plot(
            [self.start.x, self.end.x],
            [self.start.y, self.end.y],
            label = f'{self.__repr__}'
            )

    def __repr__(self):
        return f'Segment (start={self.start}, end={self.end})'  

class Circle(Shape):
    def __init__(self, center: Point, radius: float):
        if radius <= 0:
            raise ValueError('Значение радиуса должно быть больше 0') 
        self.center = center
        self.radius = radius
    
    def to_dict(self) -> dict[str, any]:
        return {
            'type': 'circle',
            'center': self.center.to_dict(),
            'radius': self.radius
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, any]) -> Circle:
        return cls(
            center=Point.from_dict(data['center']),
            radius=data['radius']
        )

    @staticmethod
    def parse_args(args: list[str]) -> dict[str, any]:
        if len(args) != 3:
            raise ValueError("Нужно 3 параметра: для центральной точки x1 y1 и radius")
        return {
            'center': Point(float(args[0]), float(args[1])),
            'radius': float(args[2])
        }
    
    @staticmethod
    def get_help() -> str:
        return 'Центральная точка, радиус. x_center y_center radius'
    
    #test
    def draw(self, ax: plt.Axes):
        patch = MplCircle(
            (self.center.x, self.center.y), 
            self.radius,
            fill=False,
            label = f'{self.__repr__}'
        )
        ax.add_patch(patch)

    def __repr__(self):
        return f'Circle (center point={self.center}, radius={self.radius})'  


class Polygon(Shape):
    def __init__(self, vertices: list[Point]):
        if len(vertices) < 3:
            raise ValueError('Передано меньше 3-х точек')
        self.vertices = vertices
        
    def to_dict(self) -> dict[str, any]:
        return {
            'type': 'polygon',
            'vertices': [v.to_dict() for v in self.vertices],
            'name': self.name
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, any]) -> Polygon:
        return cls(
            vertices=[Point.from_dict(v) for v in data['vertices']],
        )

    @staticmethod
    def parse_args(args: list[str]) -> dict[str, any]:
        if len(args) % 2 != 0:
            raise ValueError('Нечетное количество координат. Нужны пары x y')
        
        points = []
        set_points = set()
        for i in range(0, len(args), 2):
            try:
                x = float(args[i])
                y = float(args[i+1])
                point = Point(x, y)
                if point in set_points:
                    raise ValueError(f'Точка {point} уже добавлена. Точки должны быть уникальными')
                points.append(point)
                set_points.add(point)
            except IndexError:
                raise ValueError('Некорректные координаты точки')
            except ValueError:
                raise ValueError('Координаты должны быть числами')
            
        return {'vertices': points}
            
    def get_help() -> str:
        return 'x1 y1 x2 y2 x3 y3 ... (минимум 3 точки)'

    def draw(self, ax: plt.Axes, color: str = 'green') -> None:
        coordinates = [(p.x, p.y) for p in self.vertices]
        patch = MplPolygon(
            coordinates,
            closed=True,
            fill=False,
            edgecolor=color,
            label = f'{self.__repr__}'
        )
        ax.add_patch(patch)

    def __repr__(self):
        return f'Polygon (vertices={self.vertices})'

class Oval(Shape):
    def __init__(self, center: Point, width: float, height: float):
        if width <= 0 or height <= 0:
            raise ValueError("Ширина и высота должны быть больше нуля")
        self.center = center
        self.width = width
        self.height = height

    def to_dict(self) -> dict[str, any]:
        return {
            'type': 'oval',
            'center': self.center.to_dict(),
            'width': self.width,
            'height': self.height
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, any]) -> Oval:
        return cls(
            center=Point.from_dict(data['center']),
            width=data['width'],
            height=data['height']
        )

    @staticmethod
    def parse_args(args: list[str]) -> dict[str, any]:
        if len(args) != 4:
            raise ValueError("Нужно 4 параметра: center_x center_y width height")
        return {
            'center': Point(float(args[0]), float(args[1])),
            'width': float(args[2]),
            'height': float(args[3])
        }
    
    @staticmethod
    def get_help() -> str:
        return "center_x center_y width height"

    def draw(self, ax: plt.Axes):
        patch = MplEllipse(
            (self.center.x, self.center.y),
            width=self.width,
            height=self.height,
            fill=False,
            label=f'{self.__repr__()}'
        )
        ax.add_patch(patch)

    def __repr__(self):
        return f"Oval(center={self.center}, width={self.width}, height={self.height})"
