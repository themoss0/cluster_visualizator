from features.file.repositories.ifile_repository import IFileRepository


class FileRepository(IFileRepository):
    def __init__(self):
        pass

    def preset_lines(self, filename: str, extra_type: str='none'):
        points = []
        file = open(filename, 'r', encoding='utf-8')

        parts = file.readline()
        is_header = False  # По умолчанию мы считаем, что буквенного заголовка нет
        if len(parts) == 2:
            try:
                float(parts[0].replace(',','.'))
                float(parts[1].replace(',','.'))
            except ValueError:
                is_header = True
        else: 
            is_header = True      
        
        start: int = 1 if is_header else 0

        for line in file:
            star = []
            try:
                corr_line = line.replace(',', '.').split()
                if extra_type == 'planet':
                    x_pos = float(corr_line[0])
                    y_pos = float(corr_line[1])
                    planet_info = corr_line[2]
                    star = [x_pos, y_pos, planet_info]
                else:
                    x_pos = float(corr_line[0])
                    y_pos = float(corr_line[1])
                    star = [x_pos, y_pos]
            except ValueError as err:
                print(f'Ошибка предустановки строк: {err}')
            points.append(star)
        return points


    def load_data(self, filename: str):
        """Загружает точки из файла. Пропускает первую строку, если она не числовая"""

        lines = self._preset_lines(filename)
        
        # points: list = []
        # with open(filename, 'r', encoding='utf-8') as f:
        #     lines: list[str] = f.readlines()
        # if not lines:
        #     return points
        
        # Проверяем первую строку на наличие заголовка
        parts = lines[0]
        is_header = False  # По умолчанию мы считаем, что буквенного заголовка нет
        if len(parts) == 2:
            try:
                float(parts[0].replace(',','.'))
                float(parts[1].replace(',','.'))
            except ValueError:
                is_header = True
        else: 
            is_header = True

        start: int = 1 if is_header else 0

        for line in lines[start:]:
            if not line:
                continue
            try:
                if len(line) == 2:
                    x_str, y_str = line.split()
                else:
                    x_str, y_str, planet_str = splitted_line[0], splitted_line[1], splitted_line[2]
                    print('У меня пока нет возможности работать с планетами(')
                    break
            except Exception as err:
                print(f'Я пока не умею работать с планетами( {err}')
            x: float = float(x_str.replace(',','.')) 
            y: float = float(y_str.replace(',','.')) 
            points.append([x, y])
        return points
    

    def load_data_with_planet(self, filename):
        points = []
        file = open(filename, 'r', encoding='utf-8')
        for line in file:
            temp = line.replace(',','.').split()
            x_pos = float(temp[0])
            y_pos = float(temp[1])
            h = temp[2]
            points.append( ([x_pos, y_pos], h) )
