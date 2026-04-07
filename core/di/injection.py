from features.calculations.repositories.calculate_repository import CalculateRepository
from features.calculations.repositories.icalculate_repository import ICalculateRepository
from features.calculations.services.calculate_service import CalculateService
from features.file.repositories.file_repository import FileRepository
from features.file.services.file_service import FileService

container = {}

def load_dependencies() -> None:
    """Загрузка зависимостей/объектов классов сервисов и репозиториев"""
    file_repository_obj: FileRepository = FileRepository()
    container['file_service'] = FileService(file_repository=file_repository_obj)  

    calculate_repository_obj: ICalculateRepository = CalculateRepository()
    container['calculate_service'] = CalculateService(calculate_repository_obj)
    

def get_file_service() -> FileService:
    return container.get('file_service')

def get_calculate_service() -> CalculateService:
    return container.get('calculate_service')