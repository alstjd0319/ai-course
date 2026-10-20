/**
 * 주차 요금 계산 로직 모듈
 */

/**
 * "HH:mm" 형식의 문자열을 총 분(minutes) 단위 정수로 변환합니다.
 * @param {string} timeStr - "09:30" 형태의 문자열
 * @returns {number} 총 분 단위
 * @throws {Error} 입력값이 비어있거나 형식이 올바르지 않은 경우
 */
export function timeToMinutes(timeStr) {
    if (!timeStr || timeStr.trim() === "") {
        throw new Error("시간을 입력해주세요.");
    }

    const timeRegex = /^([01]\d|2[0-3]):([0-5]\d)$/;
    if (!timeRegex.test(timeStr)) {
        throw new Error("올바른 시간 형식(HH:mm)이 아닙니다.");
    }

    const [hours, minutes] = timeStr.split(':').map(Number);
    return hours * 60 + minutes;
}

/**
 * 두 시각 사이의 주차 요금을 계산합니다.
 * @param {string} entryTimeStr - 입차 시각 "HH:mm"
 * @param {string} exitTimeStr - 출차 시각 "HH:mm"
 * @returns {{fee: number, duration: number}} {계산된 요금, 총 주차 시간(분)}
 * @throws {Error} 필수 입력 누락, 형식 오류, 또는 시간 범위 오류 시
 */
export function calculateParkingFee(entryTimeStr, exitTimeStr) {
    const entryMinutes = timeToMinutes(entryTimeStr);
    const exitMinutes = timeToMinutes(exitTimeStr);

    let actualExitMinutes = exitMinutes;
    
    // 자정 경과 처리: 출차 시각이 입차 시각보다 빠르면 다음날로 간주
    if (exitMinutes < entryMinutes) {
        actualExitMinutes += 1440; // 24시간(1440분) 추가
    }

    const duration = actualExitMinutes - entryMinutes;
    let fee = 0;

    if (duration > 30) {
        // 30분 초과 시, 초과된 시간에 대해 10분당 500원 (올림 처리)
        const taxableMinutes = duration - 30;
        const units = Math.ceil(taxableMinutes / 10);
        fee = units * 500;
    }

    // 하루 최대 요금 20,000원 적용
    fee = Math.min(fee, 20000);

    return {
        fee: fee,
        duration: duration
    };
}

/**
 * 분 단위를 "X시간 Y분" 형태로 변환합니다.
 * @param {number} totalMinutes 
 * @returns {string}
 */
export function formatDuration(totalMinutes) {
    const hours = Math.floor(totalMinutes / 60);
    const mins = totalMinutes % 60;
    
    if (hours === 0) return `${mins}분`;
    if (mins === 0) return `${hours}시간`;
    return `${hours}시간 ${mins}분`;
}

/**
 * 금액을 천 단위 쉼표가 포함된 문자열로 변환합니다.
 * @param {number} amount 
 * @returns {string}
 */
export function formatCurrency(amount) {
    return amount.toLocaleString('ko-KR');
}
