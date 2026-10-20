import { calculateParkingFee } from './parking-logic.js';

/**
 * 테스트 케이스 정의
 * T1: 무료 구간 확인 (30분)
 * T2: 무료 구간 직후 (31분)
 * T3: 일반 과금 확인 (60분)
 * T4: 단위 올림 확인 (45분)
 * T5: 최대 요금 제한 (720분)
 * T6: 시간 역전 오류 (에러 발생 기대)
 */
const testCases = [
    { id: 'T1', entry: '09:00', exit: '09:30', expectedFee: 0, desc: '30분까지 무료' },
    { id: 'T2', entry: '09:00', exit: '09:31', expectedFee: 500, desc: '31분 (1분 초과 시 10분 단위)' },
    { id: 'T3', entry: '10:00', exit: '11:00', expectedFee: 1500, desc: '60분 (30분 제외 30분 -> 3단위 * 500)' },
    { id: 'T4', entry: '13:00', exit: '13:45', expectedFee: 1000, desc: '45분 (30분 제외 15분 -> 2단위 * 500)' },
    { id: 'T5', entry: '08:00', exit: '20:00', expectedFee: 20000, desc: '최대 요금 20,000원 제한' },
    { id: 'T6', entry: '14:00', exit: '13:00', expectedFee: null, desc: '시간 역전 (에러 발생 기대)' },
];

let passedCount = 0;
let failedCount = 0;

console.log('==========================================');
console.log('🚀 주차 요금 계산기 테스트 시작');
console.log('==========================================\n');

for (const tc of testCases) {
    try {
        const result = calculateParkingFee(tc.entry, tc.exit);
        
        if (tc.expectedFee === null) {
            console.error(`❌ [${tc.id}] ${tc.desc}: 에러가 발생해야 하는데 발생하지 않았습니다.`);
            failedCount++;
        } else if (result.fee === tc.expectedFee) {
            console.log(`✅ [${tc.id}] ${tc.desc}: 성공 (요금: ${result.fee}원)`);
            passedCount++;
        } else {
            console.error(`❌ [${tc.id}] ${tc.desc}: 실패 (예상: ${tc.expectedFee}원, 실제: ${result.fee}원)`);
            failedCount++;
        }
    } catch (error) {
        if (tc.expectedFee === null) {
            console.log(`✅ [${tc.id}] ${tc.desc}: 성공 (예상된 에러 발생: ${error.message})`);
            passedCount++;
        } else {
            console.error(`❌ [${tc.id}] ${tc.desc}: 실패 (예상치 못한 에러: ${error.message})`);
            failedCount++;
        }
    }
}

console.log('\n==========================================');
console.log('📊 최종 테스트 결과');
console.log(`   통과: ${passedCount}`);
console.log(`   실패: ${failedCount}`);
console.log('==========================================');

if (failedCount > 0) {
    process.exit(1);
} else {
    process.exit(0);
}
