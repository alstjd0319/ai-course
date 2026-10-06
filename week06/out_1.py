import re

def format_phone_number(phone_str):
    """
    입력된 문자열에서 숫자만 추출한 뒤, 
    표준적인 하이픈(-) 형식을 적용하여 반환합니다.
    """
    # 1. 숫자 이외의 모든 문자 제거 (공백, 하이픈, 괄호 등 제거)
    digits = re.sub(r'\D', '', phone_str)
    
    length = len(digits)

    # 2. 길이에 따른 포맷팅
    # 휴대폰 번호 (010-1234-5678 형식)
    if length == 11:
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    
    # 휴대폰 번호 (010-123-4567 형식 - 가운데 자리가 3자리인 경우)
    elif length == 10:
        # 010, 011 등 앞자리가 3자리인 경우를 가정
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    
    # 일반 전화번호 또는 지역번호 포함 (02-123-4567 또는 031-123-4567)
    elif length >= 9:
        # 서울(02)은 앞자리가 2자리이므로 예외 처리 필요할 수 있음
        if digits.startswith('02'):
            return f"{digits[:2]}-{digits[2:5]}-{digits[5:]}"
        else:
            # 그 외 지역번호(031, 051 등)는 3자리
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}" if length == 11 else f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"

    # 형식이 맞지 않으면 숫자만 반환하거나 에러 메시지 반환
    return digits

# --- 테스트 코드 ---
test_numbers = [
    "01012345678",          # 숫자만 있는 경우
    "010-1234-5678",        # 이미 하이픈이 있는 경우
    "010 1234 5678",        # 공백이 있는 경우
    "(010)12345678",        # 괄호가 있는 경우
    "021234567",            # 서울 지역번호 (02)
    "0311234567",           # 경기도 지역번호 (031)
    "010-123-4567"          # 가운데 3자리인 경우
]

print(f"{'원본':<15} | {'정리 후':<15}")
print("-" * 35)
for num in test_numbers:
    print(f"{num:<15} | {format_phone_number(num):<15}")
