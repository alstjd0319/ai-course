import re

def clean_phone_number(phone):
    # 숫자가 아닌 모든 문자를 제거
    return re.sub(r'[^0-9]', '', phone)

# 테스트
test_numbers = ["010-1234-5678", "(02) 123-4567", "010.1234.5678", "010 1234 5678"]
for num in test_numbers:
    print(f"원본: {num} -> 결과: {clean_phone_number(num)}")
