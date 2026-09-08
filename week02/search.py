import ollama
import numpy as np

def emb(text):
    return np.array(ollama.embed(model="bge-m3", input=text).embeddings[0])

docs = [
    "은행 창구는 평일 오후 4시에 마감한다",
    "택배는 배송 시작 후 보통 이틀 안에 도착한다",
    "회의실 예약은 사내 시스템에서 선착순으로 받는다",
    "정기 건강검진은 입사 후 매년 1회 받아야 한다",
    "주민등록증 재발급은 가까운 주민센터에서 신청한다",
    "아파트 관리비는 매월 25일에 자동 이체된다",
    "반려동물 등록은 동물병원에서 대행 신청할 수 있다",
    "헬스장 회원권은 3개월 단위로 결제한다",
    "여권 갱신은 만료 6개월 전부터 신청 가능하다",
    "카페는 매주 월요일 정기 휴무다",
]
D = np.stack([emb(d) for d in docs])          # 문서 10개를 미리 벡터로 (10 x 1024)

def search(question, k=3):
    q = emb(question)
    sims = D @ q / (np.linalg.norm(D, axis=1) * np.linalg.norm(q))   # 문서 10개와의 코사인을 한 번에
    for i in np.argsort(-sims)[:k]:
        print(f"   {sims[i]:.3f}  {docs[i]}")

for question in ["회의실 예약 어떻게 해?", "은행은 언제 끝나?", " 헬스장 언제 결제해?"]:
    print("Q:", question)
    search(question)