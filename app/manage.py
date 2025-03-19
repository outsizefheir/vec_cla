import json
import shape as sh

class Manager: 
    def __init__(self):
        self.shapes: list[sh.Shape] = []
        self.shape_classes = self._get_shape_classes()
    
    def _get_shape_classes(self) -> dict[str, type[sh.Shape]]:
        return {cls.__name__.lower(): cls for cls in sh.Shape.__subclasses__()}
            
    def create_shape(self, shape_type: str, params: dict) -> sh.Shape:
        '''
        Метод для создания фигур
        '''
        if shape_type not in self.shape_classes:
            raise ValueError(f"Нет такой фигуры: {shape_type}")
        
        cls = self.shape_classes[shape_type]
        args = cls.parse_args(params)
        return cls(**args)

    def add_shape(self, shape: sh.Shape) -> None:
        '''
        Добавление фигуры в список
        '''
        self.shapes.append(shape)

    def delete_shape(self, index: int) -> sh.Shape:
        '''
        Удаление фигуры из списка
        '''
        if 0 <= index < len(self.shapes):
            return self.shapes.pop(index)
        raise IndexError('Индекс не найден')

    def save_to_file(self, filename: str) -> None:
        '''
        Сохранение в JSON-файл
        '''
        data = [shape.to_dict() for shape in self.shapes]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filename: str) -> None:
        '''
        Загрузка из JSON-файла
        '''
        with open(filename, 'r') as f:
            data = json.load(f)
        
        new_shapes = []
        for item in data:
            cls = self.shape_classes[item['type']]
            new_shapes.append(cls.from_dict(item))
        self.shapes.extend(new_shapes)