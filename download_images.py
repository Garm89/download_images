import requests
import concurrent.futures
import time
import os
import argparse

# Функция для скачивания изображения по URL-адресу и сохранения на диск
def download_image(url):
    try:
        
        response = requests.get(url)
        response.raise_for_status()  # Проверяем статус ответа
        
        # Получаем название файла из URL-адреса
        filename = url.split("/")[-1]
        
        start_time = time.time()

        with open(filename, "wb") as file:
            file.write(response.content)
        
        print(f"Изображение {filename} успешно скачано")
        total_time = time.time() - start_time
        print(f"Время скачивания {filename}: {total_time} секунд")
    except Exception as e:
        print(f"Ошибка при скачивании изображения по URL-адресу {url}: {e}")

# Функция для многопоточного подхода
def multi_threaded(urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, urls)

# Функция для многопроцессорного подхода
def multi_process(urls):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(download_image, urls)

# Функция для асинхронного подхода
import aiohttp
import asyncio

async def download_image_async(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Проверяем статус ответа
                
                # Получаем название файла из URL-адреса
                filename = url.split("/")[-1]
                
                start_time = time.time()

                with open(filename, "wb") as file:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        file.write(chunk)
                
                print(f"Изображение {filename} успешно скачано")
                total_time = time.time() - start_time
        print(f"Время скачивания {filename}: {total_time} секунд")
    except aiohttp.ClientError as e:
        print(f"Error downloading image from URL {url}: {e}")


async def async_approach(urls):
    tasks = []
    
    for url in urls:
        task = asyncio.create_task(download_image_async(url))
        tasks.append(task)
    
    await asyncio.gather(*tasks)

# Функция для скачивания изображений с использованием выбранного подхода
def download_images(urls, approach):
    start_time = time.time()
    
    if approach == "threaded":
        multi_threaded(urls)
    elif approach == "process":
        multi_process(urls)
    elif approach == "async":
        asyncio.run(async_approach(urls))
    
    total_time = time.time() - start_time
    print(f"Общее время выполнения программы: {total_time} секунд")

# Получаем список URL-адресов из аргументов командной строки
def get_urls_from_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+", help="Список URL-адресов для скачивания")
    args = parser.parse_args()
    return args.urls

# Главная функция
def main():
    urls = get_urls_from_command_line()
    approach = "async" # указать метод скачивания: threaded (многопоточный), process (многопроцессорный) или async (асинхронный)
    download_images(urls, approach)

if __name__ == "__main__":
    main()