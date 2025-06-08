import os
import sys

def check_and_fix_null_bytes(directory):
    """检查并修复目录中所有Python文件的空字节"""
    fixed_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                try:
                    # 读取文件内容
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    
                    # 检查是否存在空字节
                    if b'\x00' in content:
                        # 移除空字节
                        new_content = content.replace(b'\x00', b'')
                        
                        # 写回文件
                        with open(file_path, 'wb') as f:
                            f.write(new_content)
                            
                        fixed_files.append(file_path)
                        print(f"已修复文件: {file_path}")
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")
    
    return fixed_files

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "naruto_battle_system"
    
    print(f"开始检查目录: {directory}")
    fixed_files = check_and_fix_null_bytes(directory)
    
    if fixed_files:
        print(f"已修复 {len(fixed_files)} 个文件:")
        for file in fixed_files:
            print(f"- {file}")
    else:
        print("未发现包含空字节的文件") 