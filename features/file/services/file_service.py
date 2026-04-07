from features.file.repositories.ifile_repository import IFileRepository


class FileService:
    def __init__(self, file_repository: IFileRepository):
        self.file_repository = file_repository

    def load_data(self, filename: str):
        """
        Загружает точки из файла. Пропускает первую строку, если она не числовая.
        
        Аргументы:
        - filename: Название файла.
        """
        return self.file_repository.load_data(filename=filename)