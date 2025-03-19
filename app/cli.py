import cmd
import manage as mng
import time
import matplotlib.pyplot as plt

class Cli(cmd.Cmd):
    prompt = 'cli_shape: '

    def __init__(self):
        super().__init__()
        self.manager = mng.Manager()
    
    def do_help(self, arg = ''):
        '''
        Вывод возможных фигур и правил их создания
        help
        '''
        print('Доступные фигуры:')
        for name, cls in self.manager.shape_classes.items():
            print(f"  {name}: {cls.get_help()}")    
        
    def do_create(self, arg: str = ''):
        '''
        Создание фигуры. 
        create - пустой вызов выводит help 
        '''
        if not arg: 
            self.do_help()
            return
        
        args = arg.split()
        shape_type = args[0].lower()
        params = args[1:]
        
        try:
            shape = self.manager.create_shape(shape_type, params)
            self.manager.add_shape(shape)
            print(f'Создано: {shape}')
        except Exception as e:
            print(f'Ошибка: {e}')
            
    def do_delete(self, arg: str):
        '''
        Удаление по индексу.
        delete <idx> 
        '''
        try:
            index = int(arg)
            deleted = self.manager.delete_shape(index)
            print(f'Удалено: {deleted}')
        except (ValueError, IndexError) as e:
            print(f'Ошибка: {e}')
            
    def do_list(self, _):
        '''
        Вывод фигур
        list
        '''
        for i, shape in enumerate(self.manager.shapes):
            print(f'{i}: {shape}')

    def do_save(self, arg: str):
        '''
        Сохранение файлов в .json
        save <name>
        '''
        if not arg.endswith('.json'):
            arg += '.json'
            
        try:
            self.manager.save_to_file(arg)
            print(f'Сохранено {len(self.manager.shapes)} фигуры')
        except Exception as e:
            print(f'Ошибка: {e}')
            
    def do_load(self, arg: str):
        '''
        Загрузка из .jcon 
        load <name>
        '''
        old_len = len(self.manager.shapes)
        if not arg.endswith('.json'):
            arg += '.json'
        try:
            self.manager.load_from_file(arg)
            print(f'Загружено {len(self.manager.shapes) - old_len} фигуры')
        except Exception as e:
            print(f'Ошибка: {e}')
            
    def do_exit(self, _) -> bool:
        '''
        Выход с автоматическим сохранением
        '''
        print('До свидания!')
        if self.manager.shapes:
            current_time = time.localtime()
            formatted_time = time.strftime('%Y-%m-%d_%H-%M-%S', current_time)
            self.do_save(formatted_time)
            self.do_draw(f'--save {formatted_time}')
        return True

    #test    
    def do_draw(self, arg: str):
        '''
        Функция отрисовки фигур 
        draw - показ
        --save <name> - сохранение в файл
        --size <arg> - размер графика
        '''
        if not self.manager.shapes:
            print("Нет фигур для отрисовки")
            return
        
        save_path = None
        figsize = 8
        args = arg.split()
        
        if '--save' in args:
            idx = args.index('--save')
            save_path = args[idx+1]
            if not save_path.endswith('.png'):
                save_path += '.png'
            del args[idx:idx+2]
            
        if '--size' in args:
            idx = args.index('--size')
            figsize = int(args[idx+1])
            del args[idx:idx+2]

        fig, ax = plt.subplots(figsize=(figsize, figsize))
        ax.set_aspect('equal')
        ax.grid(True)
        
        for i, shape in enumerate(self.manager.shapes):
            shape.draw(ax)
            
        ax.autoscale()
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f'График сохранен в {save_path}')
        else:
            plt.show()
    
if __name__ == '__main__':
    Cli().cmdloop()
    
    