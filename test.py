import hashlib

def truncate_hash(input_string, iterations, truncate_length):
    for _ in range(iterations):
        # 计算MD5哈希
        hash_object = hashlib.md5(input_string.encode())
        # 获取完整的哈希值
        full_hash = hash_object.hexdigest()
        # 截取哈希值的前部分
        input_string = full_hash[:-truncate_length]
    return input_string

# 原始字符串
original_string = "ZWJlYjBkNWM0YmU1NTFlNQ=="
# 迭代次数
iterations = 50
# 每次截取的字符长度
truncate_length = 16

# 调用函数并打印最终结果
final_truncate_hash = truncate_hash(original_string, iterations, truncate_length)
print(final_truncate_hash)