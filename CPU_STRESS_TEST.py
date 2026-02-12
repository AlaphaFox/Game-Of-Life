import multiprocessing
def calculate(n):
   result = 0
   for i in range(n):
       result += i
   return result
if __name__ == '__main__':
   num_processes = multiprocessing.cpu_count() # 获取CPU核心数量
   pool = multiprocessing.Pool(processes=num_processes)
   tasks = [100000000] * num_processes # 设置任务数量
   results = pool.map(calculate, tasks) # 并行执行任务
   pool.close()
   pool.join()
   print(results) # 打印结果