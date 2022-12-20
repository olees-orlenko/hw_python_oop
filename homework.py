from dataclasses import asdict, dataclass
from typing import Dict, ClassVar, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_H: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self):
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * (self.duration * self.MIN_IN_H))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: ClassVar[float] = 0.029
    CM_IN_M: ClassVar[int] = 100
    KMH_IN_MSEC: ClassVar[float] = 0.278

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC)
                    ** 2
                    / self.height
                    * self.CM_IN_M)
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight)
                * self.duration
                * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: int
    count_pool: int
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.1
    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MULTIPLIER = 2

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_MULTIPLIER
                * self.weight
                * self.duration)


TRAINING_TYPE: Dict[str, Type[Training]] = {'SWM': Swimming,
                                            'RUN': Running,
                                            'WLK': SportsWalking}

WORKOUT_TYPE_ERROR: str = 'Такой тренировки {} не существует'


def read_package(workout_type: str, data: List[str]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAINING_TYPE:
        raise KeyError(WORKOUT_TYPE_ERROR.format(workout_type))

    return TRAINING_TYPE[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
