import inspect
import collections


def print_your_name(*args):
    for arg in args:
        print(arg)


def main():
    print_your_name('Jack black')


if __name__ == '__main__':
    main()
