from freezelery import build_task

if __name__ == '__main__':

    task = build_task(10).apply_async()
    result = task.get()

    print(result)

