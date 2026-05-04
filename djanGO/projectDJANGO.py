"""
=============================================================
  Стоматологический центр «Dental Prestige» — ООП на Python
=============================================================
"""

from datetime import date, datetime
from typing import Optional
from enum import Enum


# ─────────────────────────────────────────────
#  Перечисление статусов записи
# ─────────────────────────────────────────────

class AppointmentStatus(Enum):
    WAITING = "ожидает"
    ACTIVE = "активен"
    DONE = "завершён"
    CANCELED = "отменён"


# ─────────────────────────────────────────────
#  Базовый класс Person
# ─────────────────────────────────────────────

class Person:
    """Базовый класс для всех людей в системе."""

    def __init__(self, person_id: int, name: str, phone: str, email: str):
        self._id = person_id
        self._name = name
        self._phone = phone
        self._email = email

    # ── Свойства ──────────────────────────────
    @property
    def id(self) -> int:  return self._id

    @property
    def name(self) -> str:  return self._name

    @property
    def phone(self) -> str:  return self._phone

    @property
    def email(self) -> str:  return self._email

    def initials(self) -> str:
        """Возвращает инициалы: 'Алина Сейтова' → 'АС'"""
        parts = self._name.split()
        return "".join(p[0].upper() for p in parts[:2])

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id}, name='{self._name}')"


# ─────────────────────────────────────────────
#  Класс Patient (наследует Person)
# ─────────────────────────────────────────────

class Patient(Person):
    """Пациент клиники."""

    def __init__(self, person_id: int, name: str, phone: str,
                 email: str, birth_year: int, notes: str = ""):
        super().__init__(person_id, name, phone, email)
        self._birth_year = birth_year
        self._notes = notes
        self._appointments = []  # список Appointment

    # ── Свойства ──────────────────────────────
    @property
    def birth_year(self) -> int: return self._birth_year

    @property
    def notes(self) -> str: return self._notes

    @notes.setter
    def notes(self, value: str): self._notes = value

    @property
    def age(self) -> int:
        return date.today().year - self._birth_year

    @property
    def appointments(self) -> list:
        return list(self._appointments)

    # ── Методы ────────────────────────────────
    def add_appointment(self, appointment) -> None:
        self._appointments.append(appointment)

    def appointment_count(self) -> int:
        return len(self._appointments)

    def info(self) -> str:
        return (f"Пациент: {self._name} | Возраст: {self.age} л. "
                f"| Телефон: {self._phone} | Записей: {self.appointment_count()}"
                + (f" | Заметки: {self._notes}" if self._notes else ""))


# ─────────────────────────────────────────────
#  Класс Doctor (наследует Person)
# ─────────────────────────────────────────────

class Doctor(Person):
    """Врач клиники."""

    def __init__(self, person_id: int, name: str, phone: str,
                 email: str, specialization: str):
        super().__init__(person_id, name, phone, email)
        self._specialization = specialization

    @property
    def specialization(self) -> str: return self._specialization

    def info(self) -> str:
        return f"Врач: {self._name} | Специализация: {self._specialization} | Email: {self._email}"


# ─────────────────────────────────────────────
#  Класс Service
# ─────────────────────────────────────────────

class Service:
    """Стоматологическая услуга."""

    def __init__(self, service_id: int, name: str, price: int, duration_min: int):
        self._id = service_id
        self._name = name
        self._price = price
        self._duration_min = duration_min

    @property
    def id(self) -> int: return self._id

    @property
    def name(self) -> str: return self._name

    @property
    def price(self) -> int: return self._price

    @property
    def duration_min(self) -> int: return self._duration_min

    def __str__(self) -> str:
        return f"{self._name} — {self._price:,} ₸ ({self._duration_min} мин.)"


# ─────────────────────────────────────────────
#  Класс Appointment
# ─────────────────────────────────────────────

class Appointment:
    """Запись пациента на приём к врачу."""

    def __init__(self, appt_id: int, patient: Patient, doctor: Doctor,
                 service: Service, appt_date: str, appt_time: str):
        self._id = appt_id
        self._patient = patient
        self._doctor = doctor
        self._service = service
        self._date = appt_date  # формат "YYYY-MM-DD"
        self._time = appt_time  # формат "HH:MM"
        self.__status = AppointmentStatus.WAITING

    # ── Свойства ──────────────────────────────
    @property
    def id(self) -> int:
        return self._id

    @property
    def patient(self) -> Patient:
        return self._patient

    @property
    def doctor(self) -> Doctor:
        return self._doctor

    @property
    def service(self) -> Service:
        return self._service

    @property
    def date(self) -> str:
        return self._date

    @property
    def time(self) -> str:
        return self._time

    @property
    def status(self) -> AppointmentStatus:
        return self.__status

    # ── Методы управления статусом ────────────
    def confirm(self) -> None:
        if self.__status == AppointmentStatus.WAITING:
            self.__status = AppointmentStatus.ACTIVE
            print(f"✅ Запись #{self._id} подтверждена.")
        else:
            print(f"⚠️  Нельзя подтвердить запись со статусом «{self.__status.value}».")

    def complete(self) -> None:
        if self.__status in (AppointmentStatus.WAITING, AppointmentStatus.ACTIVE):
            self.__status = AppointmentStatus.DONE
            print(f"✅ Приём #{self._id} завершён.")
        else:
            print(f"⚠️  Нельзя завершить запись со статусом «{self.__status.value}».")

    def cancel(self) -> None:
        if self.__status != AppointmentStatus.DONE:
            self.__status = AppointmentStatus.CANCELED
            print(f"❌ Запись #{self._id} отменена.")
        else:
            print("⚠️  Нельзя отменить завершённый приём.")

    def info(self) -> str:
        return (f"[#{self._id}] {self._date} {self._time} | "
                f"{self._patient.name} → {self._doctor.name} | "
                f"{self._service.name} | Статус: {self.__status.value}")

    def __str__(self) -> str:
        return self.info()


# ─────────────────────────────────────────────
#  Главный класс Clinic
# ─────────────────────────────────────────────

class Clinic:
    """Стоматологическая клиника — центральный агрегатор всей логики."""

    def __init__(self, name: str):
        self._name = name
        self._patients = {}  # id → Patient
        self._doctors = {}  # id → Doctor
        self._services = {}  # id → Service
        self._appointments = {}  # id → Appointment
        self._counter = 1

    # ── Внутренний счётчик ────────────────────
    def _next_id(self) -> int:
        uid = self._counter
        self._counter += 1
        return uid

    # ── Пациенты ──────────────────────────────
    def add_patient(self, name: str, phone: str, email: str,
                    birth_year: int, notes: str = "") -> Patient:
        p = Patient(self._next_id(), name, phone, email, birth_year, notes)
        self._patients[p.id] = p
        print(f"➕ Добавлен пациент: {p.name}")
        return p

    def remove_patient(self, patient_id: int) -> bool:
        if patient_id in self._patients:
            name = self._patients[patient_id].name
            del self._patients[patient_id]
            print(f"🗑  Пациент удалён: {name}")
            return True
        print(f"⚠️  Пациент #{patient_id} не найден.")
        return False

    def get_patient(self, patient_id: int) -> Optional[Patient]:
        return self._patients.get(patient_id)

    @property
    def patients(self) -> list:
        return list(self._patients.values())

    # ── Врачи ─────────────────────────────────
    def add_doctor(self, name: str, phone: str, email: str,
                   specialization: str) -> Doctor:
        d = Doctor(self._next_id(), name, phone, email, specialization)
        self._doctors[d.id] = d
        print(f"➕ Добавлен врач: {d.name} ({d.specialization})")
        return d

    def get_doctor(self, doctor_id: int) -> Optional[Doctor]:
        return self._doctors.get(doctor_id)

    @property
    def doctors(self) -> list:
        return list(self._doctors.values())

    # ── Услуги ────────────────────────────────
    def add_service(self, name: str, price: int, duration_min: int) -> Service:
        s = Service(self._next_id(), name, price, duration_min)
        self._services[s.id] = s
        print(f"➕ Добавлена услуга: {s.name} — {s.price:,} ₸")
        return s

    def remove_service(self, service_id: int) -> bool:
        if service_id in self._services:
            name = self._services[service_id].name
            del self._services[service_id]
            print(f"🗑  Услуга удалена: {name}")
            return True
        return False

    @property
    def services(self) -> list:
        return list(self._services.values())

    # ── Записи на приём ───────────────────────
    def book(self, patient_id: int, doctor_id: int, service_id: int,
             appt_date: str, appt_time: str) -> Optional[Appointment]:
        patient = self._patients.get(patient_id)
        doctor = self._doctors.get(doctor_id)
        service = self._services.get(service_id)

        if not all([patient, doctor, service]):
            print("⚠️  Один из объектов (пациент/врач/услуга) не найден.")
            return None

        appt = Appointment(self._next_id(), patient, doctor,
                           service, appt_date, appt_time)
        self._appointments[appt.id] = appt
        patient.add_appointment(appt)
        print(f"📅 Запись создана: {patient.name} → {doctor.name} | {appt_date} {appt_time}")
        return appt

    def get_appointment(self, appt_id: int) -> Optional[Appointment]:
        return self._appointments.get(appt_id)

    @property
    def appointments(self) -> list:
        return list(self._appointments.values())

    # ── Фильтры ───────────────────────────────
    def appointments_today(self) -> list:
        today = date.today().isoformat()
        return [a for a in self._appointments.values() if a.date == today]

    def appointments_by_doctor(self, doctor_id: int) -> list:
        return [a for a in self._appointments.values()
                if a.doctor.id == doctor_id]

    def appointments_by_status(self, status: AppointmentStatus) -> list:
        return [a for a in self._appointments.values() if a.status == status]

    # ── Статистика ────────────────────────────
    def revenue(self) -> int:
        """Суммарная выручка по завершённым приёмам."""
        return sum(a.service.price for a in self._appointments.values()
                   if a.status == AppointmentStatus.DONE)

    def stats(self) -> dict:
        return {
            "пациентов": len(self._patients),
            "врачей": len(self._doctors),
            "услуг": len(self._services),
            "всего записей": len(self._appointments),
            "сегодня": len(self.appointments_today()),
            "выручка (₸)": self.revenue(),
        }

    # ── Отчёт ─────────────────────────────────
    def print_stats(self) -> None:
        print(f"\n{'=' * 50}")
        print(f"  {self._name} — Статистика")
        print(f"{'=' * 50}")
        for key, val in self.stats().items():
            print(f"  {key:<20}: {val:>10,}" if isinstance(val, int)
                  else f"  {key:<20}: {val}")
        print(f"{'=' * 50}\n")

    def print_schedule(self, target_date: Optional[str] = None) -> None:
        target = target_date or date.today().isoformat()
        appts = [a for a in self._appointments.values() if a.date == target]
        appts.sort(key=lambda a: a.time)
        print(f"\n📅 Расписание на {target}:")
        if not appts:
            print("  Нет записей.")
            return
        for a in appts:
            print(f"  {a.time}  {a.patient.name:<25} → {a.doctor.name:<20} | {a.service.name}")

    def __str__(self) -> str:
        return f"Клиника «{self._name}»: {len(self._patients)} пациентов, {len(self._doctors)} врачей"


# ─────────────────────────────────────────────
#  Демонстрация
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Создаём клинику
    clinic = Clinic("Dental Prestige")

    # Добавляем врачей
    d1 = clinic.add_doctor("Алина Сейтова", "+7 777 000 01", "a.s@dp.kz", "Терапевт")
    d2 = clinic.add_doctor("Марат Бекенов", "+7 777 000 02", "m.b@dp.kz", "Хирург")
    d3 = clinic.add_doctor("Жанна Нурланова", "+7 777 000 03", "z.n@dp.kz", "Ортодонт")

    # Добавляем услуги
    s1 = clinic.add_service("Отбеливание", 25_000, 60)
    s2 = clinic.add_service("Лечение кариеса", 15_000, 45)
    s3 = clinic.add_service("Удаление зуба", 12_000, 30)
    s4 = clinic.add_service("Установка брекетов", 80_000, 90)
    s5 = clinic.add_service("Чистка ультразвуком", 8_000, 40)

    # Добавляем пациентов
    p1 = clinic.add_patient("Айгерим Касымова", "+7 701 111 11", "a.k@mail.kz", 1990, "Аллергия на лидокаин")
    p2 = clinic.add_patient("Данияр Ахметов", "+7 702 222 22", "d.a@mail.kz", 1985)
    p3 = clinic.add_patient("Сауле Нурмаганбетова", "+7 703 333 33", "s.n@mail.kz", 1995, "Имплант на 36")
    p4 = clinic.add_patient("Тимур Джаксыбеков", "+7 704 444 44", "t.d@mail.kz", 2000)
    p5 = clinic.add_patient("Гульнара Омарова", "+7 705 555 55", "g.o@mail.kz", 1978, "Диабет II типа")

    today = date.today().isoformat()

    # Создаём записи
    print("\n--- Записи на приём ---")
    a1 = clinic.book(p1.id, d1.id, s1.id, today, "09:00")
    a2 = clinic.book(p2.id, d2.id, s3.id, today, "10:30")
    a3 = clinic.book(p3.id, d3.id, s4.id, today, "11:00")
    a4 = clinic.book(p4.id, d1.id, s2.id, today, "13:00")
    a5 = clinic.book(p5.id, d2.id, s5.id, today, "14:30")

    # Меняем статусы
    print("\n--- Изменение статусов ---")
    a1.confirm()
    a2.complete()
    a3.confirm()
    a4.confirm()
    a5.cancel()

    # Прошлая запись
    past = "2026-04-20"
    a6 = clinic.book(p1.id, d2.id, s3.id, past, "10:00")
    a6.complete()

    # Отчёты
    clinic.print_schedule()
    clinic.print_stats()

    # Детали пациента
    print("--- Информация о пациенте ---")
    print(p1.info())

    # Список услуг
    print("\n--- Услуги клиники ---")
    for svc in clinic.services:
        print(f"  • {svc}")

    # Выручка
    print(f"\n💰 Выручка клиники: {clinic.revenue():,} ₸")
    print(f"\n{clinic}")
