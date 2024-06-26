class Cache(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_hits = 0
        self.cache_refs = 0

    def __getitem__(self, key):
        self.cache_hits += 1
        return super().__getitem__(key)


def time_interval(interval: float):
    if interval < 0.001:
        return "{:10.3f} µs".format(interval * 1e6)
    elif interval < 1.0:
        return "{:10.3f} ms".format(interval * 1e3)
    else:
        return "{:10.3f} s".format(interval)


def func_name(func) -> str:
    return str(func).split(" ")[1]


def timer(func):
    import time

    # time.time() -> Segundos
    def wrapper(*wrapped_func_args):
        start_time = time.time()
        result = func(*wrapped_func_args)
        end_time = time.time()

        print(f"{func_name(func)} tomó: {time_interval(end_time-start_time)}")
        return result

    return wrapper


registro_tiempo: dict[str, float] = {}


def method_total_timer(func):
    def wrapper(self, *wrapped_func_args):
        start_time = time.time()
        result = func(*wrapped_func_args)
        end_time = time.time()

        registro_tiempo[func_name(func)] = registro_tiempo.get(func_name(func), 0) + (
            end_time - start_time
        )
        return result

    return wrapper


def total_timer(func):
    def wrapper(*wrapped_func_args):
        start_time = time.time()
        result = func(*wrapped_func_args)
        end_time = time.time()

        registro_tiempo[func_name(func)] = registro_tiempo.get(func_name(func), 0) + (
            end_time - start_time
        )
        return result

    return wrapper


def mostrar_tiempos_ejecución(indent: int = 0):
    print(" Tiempos de ejecución de cada función:")

    print(
        "".join(
            (
                f"     {func_name}: {time_interval(tiempo)}\n"
                for func_name, tiempo in registro_tiempo.items()
            )
        )
    )
