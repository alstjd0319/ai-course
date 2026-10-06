import re

def format_phone_number(phone_str):
    # 1. 숫자만 남기기 (정규표현식 사용)
    digits = re.sub(r'\D', '', phone_str)
    
    # 2. 길이에 따라 하이픈 삽입
    length = len(digits)
    
    if length == 11:  # 010-1234-5678 형식
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    elif length == 10: # 02-123-4567 또는 010-123-4567 형식
        # 앞자리가 02(서울)인 경우와 01x인 경우를 구분할 수 있지만, 
        # 보통 3-3-4 또는 3-4-4 구조로 처리합니다.
        if digits.startswith('02'):
            return f"{digits[:2]}-{digits[2:5]}-{digits[5:]}"
        else:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif length == 8:  # 1234-5678 형식 (지역번호 제외 시)
        return f"{digits[:4]}-{digits[4:]}"
    else:
        return digits  # 형식이 맞지 않으면 숫자만 반환

# 테스트
test_numbers = ["01012345678", "010-1234-5678", "010 1234 5678", "021234567", "0101234567"]
for num in test_numbers:
    print(f"{num}  =>  {format_phone_number(num)}")
