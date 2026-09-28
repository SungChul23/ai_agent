'''
구동 환경 체크
'''

import sys
import platform

print(f'Python version: {sys.version}')
print(f'Platform: {platform.system()} {platform.release()}')

print("ready to run the application.")