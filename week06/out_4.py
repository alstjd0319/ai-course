import re

def clean_phone_number(phone, mode='digits'):
    """
    전화번호를 정리하는 함수
    :param phone: 입력된 전화번호 (문자열)
    :param mode: 정리 방식 ('digits', 'hyphen', 'standard')
    :return: 정리된 전화번호 문자열
    """
    # 1. 숫자 이외의 모든 문자를 제거
    digits = re.sub(r'\D', '', phone)
    
    if mode == 'digits':
        # 방식 1: 숫자만 남기기 (예: 01012345678)
        return digits
    
    elif mode == 'hyphen':
        # 방식 2: 일반적인 하이픈 형식 (예: 010-1234-5678)
        if len(digits) == 10:  # 02-123-4567 또는 010-123-4567 형태
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        elif len(digits) == 11: # 010-1234-5678 형태
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return digits # 형식이 맞지 않으면 숫자만 반환
            
    elif mode == 'standard':
        # 방식 3: 02(서울) 등 지역번호 처리 포함 정규화
        # 02-123-4567 또는 010-1234-5678 등으로 변환
        if len(digits) == 9 and digits.startswith('02'):
            return f"{digits[:2]}-{digits[2:5]}-{digits[5:]}"
        elif len(digits) == 10:
            # 010-123-4567 혹은 02-1234-5678 구분
            if digits.startswith('02'):
                return f"{digits[:2]}-{digits[2:6]}-{digits[6:]}"
            else:
                return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        
        return digits

    return digits

# --- 테스트 코드 ---
test_numbers = [
    "010-1234-5678",
    "01012345678",
    "02.123.4567",
    "02 1234 5678",
    "(010) 1234 5678",
    "010-123-4567"
]

print(f"{'원본':<20} | {'숫자만':<15} | {'하이픈':<15} | {'표준형'}")
print("-" * 70)

for num in test_numbers:
    digits = clean_phone_number(num, 'digits')
    hyphen = clean_phone_number(num, 'hyphen')
    standard = clean_phone_number(num, 'standard')
    print(f"{num:<20} | {digits:<15} | {hyphen:<15} | {standard}")
