from features.file.repositories.ifile_repository import IFileRepository


class FileService:
    def __init__(self, file_repository: IFileRepository):
        self.file_repository = file_repository

    def preset_lines(self, filename: str, extra_type: str='none'):
        return self.file_repository.preset_lines(filename=filename, extra_type=extra_type)

    def load_data(self, filename: str):
        """
        Загружает точки из файла. Пропускает первую строку, если она не числовая.
        
        Аргументы:
        - filename: Название файла.
        """
        return self.file_repository.load_data(filename=filename)