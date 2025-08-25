from abc import abstractmethod, ABC


class IImportExtractor(ABC):

    @abstractmethod
    def extract(self, files: dict[str, str]) -> dict[str, str]:
        pass
