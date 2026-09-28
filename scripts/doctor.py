'''
개발환경 체크용
- 추후 필요시 계속 추가 가능
'''


import shutil
import sys

# 체크할 명령어 리스트
commands = ['python',  'git', 'aws', 'docker', 'docker-compose'] 

print(f'Python version: {sys.version}')
for command in commands:
    if shutil.which(command) is None:
        print(f'{command} is not installed.')
    else:
        print(f'{command} is installed.')
        
