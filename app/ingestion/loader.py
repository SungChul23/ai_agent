'''
- 메타데이터와 본문(규정) 분리
'''
from pathlib import Path
import yaml

def load_markdown(path: Path):
    '''
    parameters
        - path : 원소스 (*.md)의 실제 경로
    returns
        - meta 데이터(yaml -> dict 형태등)
        - body 본문 규정 데이터(텍스트, 문자열)
    '''
    # 1. markdown 전체를 읽은 후 yaml 프런트 포멧터 존재하는제 체크 (---)
    text = path.read_text(encoding='utf-8')
    #print( text )
    # 2. 구분자 체크 (---)
    if not text.startswith('---'):
        # 메타 데이터가 없는 규정집 문서임
        return {}, text
    # 3. "---" 최대 2회만 분할
    _, meta, body = text.split('---', 2)
    #print( meta )
    #print( '-'*30 )
    #print( body )
    
    # 4. 반환 (dict, text)
    # yaml.safe_load() => 키:값 ... => 안정하게 파싱 => dict 반환
    return yaml.safe_load(meta) or {}, body.strip()