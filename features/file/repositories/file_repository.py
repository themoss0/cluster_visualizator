from features.file.repositories.ifile_repository import IFileRepository


class FileRepository(IFileRepository):
    def __init__(self):
        pass

    def load_data(self, filename: str):
        """Загружает точки из файла. Пропускает первую строку, если она не числовая"""
        points: list = []
        with open(filename, 'r', encoding='utf-8') as f:
            lines: list[str] = f.readlines()
        if not lines:
            return points
        
        # Проверяем первую строку на наличие заголовка
        first: str = lines[0].strip()
        parts: list[str] = first.split()
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
            line = line.strip()
            if not line:
                continue
            x_str, y_str = line.split()
            x: float = float(x_str.replace(',','.')) 
            y: float = float(y_str.replace(',','.')) 
            points.append([x, y])
        return points