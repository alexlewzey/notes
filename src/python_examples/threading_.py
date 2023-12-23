"""Testing out threading."""
from threading import Thread


def ask_user() -> None:
    user_input = input("name: ")
    print(f"hello {user_input}")


def complex_calc() -> list[float]:
    return [x**2 for x in range(10_000_000)]


def main():
    ask_user()
    complex_calc()


def main_multi():
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


thread1 = Thread(target=ask_user)
thread2 = Thread(target=complex_calc)

main()
main_multi()
